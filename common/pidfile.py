import os
import tempfile
import logging

from enum import Enum

class ServiceType(Enum):
    MASTER = 0,
    SLAVE = 1

class PidFile:
    def __init__(self, serviceType):
        self.logger = logging.getLogger('pcmd.common.PidFile')

        self.type = serviceType
        self.pid = -1
        self.runningPid = -1
        self.localPort = -1

        if self.type is ServiceType.MASTER:
            pidFileName = "pcmd_master.pid"
        elif self.type is ServiceType.SLAVE:
            pidFileName = "pcmd_slave.pid"
        tempDir = tempfile.gettempdir()

        self.pidFilePath = os.path.join(
            tempDir,
            pidFileName,
        )

    def isRunning(self):
        if os.path.exists(self.pidFilePath):
            self.logger.debug("pidFile %s already exists", self.pidFilePath)

            out = None
            with open(self.pidFilePath, 'r') as pidFileFD:
                content = pidFileFD.readline().split(":")
                pid = int(content[0])
                if self.pidExists(pid):
                    self.logger.debug(
                        "process with pid %d already exists",
                        pid,
                    )
                    self.runningPid = pid
                    out = True
                else:
                    self.logger.debug(
                        "pidFile %s still exists, but process with pid %d doesn't, removing",
                        self.pidFilePath,
                        pid,
                    )
                    out = False

            if out is False:
                os.remove(self.pidFilePath)

            return out

        else:
            self.logger.debug("pidFile %s doesn't exists", self.pidFilePath)
            return False

    def create(self, portNumber):
        with open(self.pidFilePath, 'w') as pidFileFD:
            pidFileFD.write("{}:{}".format(self.pid, portNumber))

        self.logger.debug(
            "pidFile %s created with pid %d and port %d",
            self.pidFilePath,
            self.pid,
            portNumber,
        )

        return True

    def read(self):
        with open(self.pidFilePath, 'r') as pidFileFD:
            content = pidFileFD.readline().split(":")
            return (int(content[0]), int(content[1]))

    def pidExists(self, pid):
        if pid < 0:
            return False
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return False
        except PermissionError:
            return True
        else:
            return True
