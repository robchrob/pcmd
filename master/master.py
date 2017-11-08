import socket
import os
import threading
import logging
from multiprocessing import Process

from common.const import mainServer, localServer
import master.stop
import master.localsrv
import master.slavesrv

from common.pidfile import ServiceType, PidFile

class Master:
    def __init__(self, cliArgs):
        self.logger = logging.getLogger('pcmd.master.Master')

        self.cliArgs = cliArgs

        self.pidF = PidFile(ServiceType.MASTER)

        self.localServer = master.localsrv.LocalServer(self)
        self.slaveServer = master.slavesrv.SlaveServer(self)

        self.logger.debug('created instance of master.Master')

    def masterLoop(self):
        self.pidF.pid = os.getpid()
        if self.pidF.isRunning():
            self.logger.error(
                "pcmd master is already running with pid %d",
                self.pidF.runningPid,
            )
            return 1

        self.logger.debug("starting masterLoop with pid %d", self.pidF.pid)
        localThread = threading.Thread(
            target = self.localServer.localLoop,
        )
        localThread.name = "localThread"
        self.logger.debug("starting %s", localThread.getName())
        localThread.start()

        slaveThread = threading.Thread(
            target = self.slaveServer.slaveLoop,
        )
        slaveThread.name = "slaveThread"
        self.logger.debug("starting %s", slaveThread.getName())
        slaveThread.start()

        try:
            localThread.join()
            slaveThread.join()
        except KeyboardInterrupt as e:
            return master.stop.main(self)

        return 0

    def shutdown(self):
        self.localServer.shutdown()
        self.slaveServer.shutdown()

