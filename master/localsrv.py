import socket
import os
import threading
import logging
from multiprocessing import Process

from common.const import mainServer, localServer

class LocalServer:
    def __init__(self, masterObj):
        self.logger = logging.getLogger('pcmd.master.localServer')

        self.masterObj = masterObj
        self.running = True
        self.localSocket = None

    def localLoop(self):
        self.localSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.localSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.localSocket.bind(("localhost",0))
        self.localSocket.listen(5)

        self.masterObj.pidF.create(self.localSocket.getsockname()[1])
        self.logger.debug('localLoop started')
        while True:
            try:
                (commSocket, address) = self.localSocket.accept()
            except Exception as e:
                if self.running is False:
                    break
                else:
                    self.logger.debug("localSocket throws %s", e)

            localThread = threading.Thread(
                target=self.localHandler,
                args=(commSocket,address,)
            )
            localThread.daemon = True
            localThread.start()

        self.logger.debug('localLoop stopped')
        return 0

    def localHandler(self, commSocket, address):
        request = commSocket.recv(4096)
        self.logger.debug('Received {} from {}'.format(request, address))

        if request == b'stop':
            self.logger.debug("stopping pcmd")
            self.masterObj.shutdown()

        commSocket.close()

    def shutdown(self):
        self.running = False
        self.localSocket.shutdown(socket.SHUT_RDWR)
        self.localSocket.close()
