import logging
import pickle

import common.server
import common.util
import master.stop

from common.const import ModuleType
from common.pidfile import PidFile
from common.status import Status


class Master:
    def __init__(self, conf):
        self.logger = logging.getLogger('pcmd.master.Master')
        self.local = False
        self.conf = conf

        self.pidFile = PidFile(ModuleType.MASTER)
        self.localServer = None
        self.slaveServer = None

        self.logger.debug('created instance of pcmd.master.Master')

    def loop(self):
        self.localServer = common.server.Server(
            "pcmd.master.localServer",
            self.conf.get('local_hostname'),
            self.conf.get('local_port'),
            self.local_handler,
        )

        self.slaveServer = common.server.Server(
            "pcmd.master.slaveSever",
            self.conf.get('hostname'),
            self.conf.get('port'),
            self.slave_handler,
        )

        if self.pidFile.running():
            self.logger.error(
                "pcmd.master is already running with pid %d",
                self.pidFile.runningPid,
            )
            return 1
        else:
            self.pidFile.create(self.localServer.port)
            self.local = True

        self.logger.debug("starting pcmd.master with pid %d", self.pidFile.pid)

        try:
            self.localServer.thread.join()
            self.slaveServer.thread.join()
        except KeyboardInterrupt:
            return master.stop.main(self)

        return 0

    def local_handler(self, communication, address):
        request = communication.recv(4096)
        request_obj = pickle.loads(request)

        self.logger.debug(
            'Received {} from {}'.format(request_obj.name, address)
        )

        if request_obj.name == 'master.message.stop':
            shutdown_status = self.shutdown()
            request_obj.status = shutdown_status
            request_obj.respond(communication)
        elif request_obj.name == 'master.message.status':
            out = self.get_status()
            request_obj.statusFull = out
            request_obj.status = 0
            request_obj.respond(communication)

        communication.close()

    def slave_handler(self, communication, address):
        request = communication.recv(4096)
        self.logger.debug('Received {} from {}'.format(request, address))

        msg = 'HELLO SLAVE!'
        communication.sendall(msg.encode('utf-8'))
        communication.close()

    def shutdown(self):
        local_status = self.localServer.shutdown()
        slave_status = self.slaveServer.shutdown()

        return local_status or slave_status

    def get_status(self):
        out = Status()
        out.name = "pcmd.master"
        out.hostname = self.slaveServer.address
        out.port = self.slaveServer.port
        out.lhostname = self.localServer.address
        out.lport = self.localServer.port

        return out
