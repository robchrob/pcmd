import socket
import os
import threading
import logging
from multiprocessing import Process

from common.const import mainServer
import common.server

import master.stop

from common.pidfile import ServiceType, PidFile

class Master:
    def __init__(self, cliArgs):
        self.logger = logging.getLogger('pcmd.master.Master')

        self.cliArgs = cliArgs

        self.pidF = PidFile(ServiceType.MASTER)

        self.localServer = common.server.Server(
            "pcmd.master.localServer",
            "127.0.0.1",
            -1,
            self.localHandler,
        )

        self.slaveServer = common.server.Server(
            "pcmd.master.slaveServer",
            mainServer['HOST'],
            mainServer['PORT'],
            self.slaveHandler,
        )

        self.logger.debug('created instance of master.Master')

    def masterLoop(self):
        self.pidF.pid = os.getpid()
        if self.pidF.isRunning():
            self.logger.error(
                "pcmd master is already running with pid %d",
                self.pidF.runningPid,
            )
            return 1

        self.pidF.create(self.localServer.port)

        self.logger.debug("starting masterLoop with pid %d", self.pidF.pid)
        localThread = threading.Thread(
            target = self.localServer.loop,
        )
        localThread.name = "master.localThread"
        self.logger.debug("starting %s", localThread.getName())
        localThread.start()

        slaveThread = threading.Thread(
            target = self.slaveServer.loop,
        )
        slaveThread.name = "master.slaveThread"
        self.logger.debug("starting %s", slaveThread.getName())
        slaveThread.start()

        try:
            localThread.join()
            slaveThread.join()
        except KeyboardInterrupt as e:
            return master.stop.main(self)

        return 0

    def localHandler(self, commSocket, address):
        request = commSocket.recv(4096)
        self.logger.debug('Received {} from {}'.format(request, address))

        if request == b'stop':
            self.logger.debug("stopping pcmd")

            outShutdown = self.shutdown()

            if outShutdown == 0:
                self.logger.debug("sending ok to master-stop")
                commSocket.sendall(bytes('ok', 'utf-8'))
            else:
                self.logger.debug("sending 1 to master-stop")
                commSocket.sendall(bytes('1', 'utf-8'))

        commSocket.close()

    def slaveHandler(self, slaveSocket, address):
        request = slaveSocket.recv(4096)
        self.logger.debug('Received {} from {}'.format(request, address))

        msg = 'HELLO SLAVE!'
        slaveSocket.sendall(msg.encode('utf-8'))
        slaveSocket.close()

    def shutdown(self):
        outLocal = self.localServer.shutdown()
        outSlave = self.slaveServer.shutdown()

        return outLocal or outSlave
