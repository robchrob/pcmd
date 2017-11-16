import enum
import getpass
import logging
import os
import tempfile

from common.util import process_exist


class ServiceType(enum.Enum):
    MASTER = 0,
    SLAVE = 1


class PidFile:
    def __init__(self, service_type):
        self.logger = logging.getLogger('pcmd.common.PidFile')

        if service_type is ServiceType.MASTER:
            filename = 'pcmd_master_{}.pid'.format(getpass.getuser())
        elif service_type is ServiceType.SLAVE:
            filename = 'pcmd_slave_{}.pid'.format(getpass.getuser())
        else:
            raise Exception('unknown service type')

        self.pidFilePath = os.path.join(
            tempfile.gettempdir(),
            filename,
        )

        self.pid = -1
        self.runningPid = -1
        self.localPort = -1

    def create(self, local_port):
        with open(self.pidFilePath, 'w') as pidFileFD:
            pidFileFD.write("{}:{}".format(self.pid, local_port))

        self.logger.debug(
            'pidFile %s created with pid %d and port %d',
            self.pidFilePath,
            self.pid,
            local_port,
        )

        return True

    def remove(self):
        os.remove(self.pidFilePath)
        self.logger.debug(
            "pidFile %s removed", self.pidFilePath
        )

    def read(self):
        with open(self.pidFilePath, 'r') as pidFileFD:
            content = pidFileFD.readline().split(":")

        return int(content[0]), int(content[1])

    def running(self):
        self.pid = os.getpid()

        if os.path.exists(self.pidFilePath):
            with open(self.pidFilePath, 'r') as pidFileFD:
                content = pidFileFD.readline().split(":")
                pid = int(content[0])

            if process_exist(pid):
                self.logger.debug(
                    'process with pid %d already exists',
                    pid,
                )
                self.runningPid = pid
                return True
            else:
                self.logger.debug(
                    'pidFile %s  exists, but process %d does not, removing',
                    self.pidFilePath,
                    pid,
                )
                os.remove(self.pidFilePath)
                return False
        else:
            self.logger.debug('pidFile %s does not exists', self.pidFilePath)
            return False
