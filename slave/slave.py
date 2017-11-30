import logging
import pickle

import common.server
import common.util
import slave.stop

from common.const import ModuleType
from common.pidfile import PidFile
from common.status import Status
from common.run import execute


class Slave:
    def __init__(self, conf):
        self.logger = logging.getLogger('pcmd.slave.Slave')
        self.local = False
        self.conf = conf

        self.pidFile = PidFile(ModuleType.SLAVE)
        self.localServer = None
        self.slaveServer = None

        self.logger.debug('created instance of pcmd.slave.Slave')

    def loop(self):
        self.localServer = common.server.Server(
            "pcmd.slave.localServer",
            self.conf.get('local_hostname'),
            self.conf.get('local_port'),
            self.local_handler,
        )

        self.slaveServer = common.server.Server(
            "pcmd.slave.masterServer",
            self.conf.get('hostname'),
            self.conf.get('port'),
            self.master_handler,
        )

        if self.pidFile.running():
            self.logger.error(
                "pcmd.slave is already running with pid %d",
                self.pidFile.runningPid,
            )
            return 1
        else:
            self.pidFile.create(self.localServer.port)
            self.local = True

        self.logger.debug("starting pcmd.slave with pid %d", self.pidFile.pid)

        try:
            self.localServer.thread.join()
            self.slaveServer.thread.join()
        except KeyboardInterrupt:
            return slave.stop.main(self)

        return 0

    def local_handler(self, communication, address):
        request = communication.recv(4096)
        request_obj = pickle.loads(request)

        self.logger.debug(
            'Received {} from {}'.format(request_obj.name, address)
        )

        if request_obj.name == 'slave.message.stop':
            shutdown_status = self.shutdown()
            request_obj.status = shutdown_status
            if request_obj.status == 0:
                self.pidFile.remove()
            request_obj.respond(communication)
        elif request_obj.name == 'slave.message.status':
            out = self.get_status()
            request_obj.statusFull = out
            request_obj.status = 0
            request_obj.respond(communication)

        communication.close()

    def master_handler(self, communication, address):
        request_obj = common.util.recvmsg(communication)

        self.logger.debug(
            'Received {} from {}'.format(request_obj.name, address)
        )

        if request_obj.name == 'master.message.exec':
            self.logger.debug("executing {}".format(request_obj.cmd))
            execute(request_obj, communication)

        communication.close()

    def shutdown(self):
        local_status = self.localServer.shutdown()
        slave_status = self.slaveServer.shutdown()

        return local_status or slave_status

    def get_status(self):
        out = Status()
        out.name = "pcmd.slave"
        out.hostname = self.slaveServer.address
        out.port = self.slaveServer.port
        out.lhostname = self.localServer.address
        out.lport = self.localServer.port

        return out
