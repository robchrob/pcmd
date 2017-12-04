import logging
import os

import common.server
import common.util
import slave.stop

from common.const import ModuleType
from common.pidfile import PidFile
from common.run import execute


class Slave:
    def __init__(self, conf):
        self.logger = logging.getLogger('pcmd.slave.Slave')
        self.local = False
        self.conf = conf

        self.pidFile = PidFile(ModuleType.SLAVE)
        self.localServer = None
        self.masterServer = None

        self.logger.debug('created instance of pcmd.slave.Slave')

    def loop(self):
        self.localServer = common.server.Server(
            "pcmd.slave.localServer",
            self.conf.get('local_hostname'),
            self.conf.get('local_port'),
            self.local_handler,
        )

        self.masterServer = common.server.Server(
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
            self.masterServer.thread.join()
        except KeyboardInterrupt:
            return slave.stop.main(self)

        return 0

    def local_handler(self, communication, address):
        request_obj = common.util.recvmsg(communication)

        self.logger.debug(
            'slave.localServer received {} from {}'.format(
                request_obj.name,
                address
            )
        )

        if request_obj.name == 'slave.message.stop':
            shutdown_status = self.shutdown()
            request_obj.status = shutdown_status
            if request_obj.status == 0:
                self.pidFile.remove()
            request_obj.send(communication)

        elif request_obj.name == 'slave.message.status':
            request_obj.statusFull = self.fill_status(request_obj.statusFull)
            request_obj.status = 0
            request_obj.send(communication)

        communication.close()

    def master_handler(self, communication, address):
        request_obj = common.util.recvmsg(communication)

        self.logger.debug(
            'slave.masterServer received {} from {}'.format(
                request_obj.name,
                address
            )
        )

        if request_obj.name == 'master.message.exec':
            self.logger.debug("executing {}".format(request_obj.cmd))
            out = execute(request_obj, communication)

            if out == 0:
                self.logger.debug("{} executed".format(request_obj.cmd))
            else:
                self.logger.debug("{} stopped".format(request_obj.cmd))

        elif request_obj.name == 'common.slave.ping':
            request_obj.env = dict(os.environ)
            request_obj.send(communication)

        communication.close()

    def shutdown(self):
        local_status = self.localServer.shutdown()
        slave_status = self.masterServer.shutdown()

        return local_status or slave_status

    def fill_status(self, obj):
        obj.name = "pcmd.slave"
        obj.hostname = self.masterServer.address
        obj.port = self.masterServer.port
        obj.lhostname = self.localServer.address
        obj.lport = self.localServer.port

        return obj
