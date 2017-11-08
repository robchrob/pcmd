import socket
import os
import threading
import logging
from multiprocessing import Process

from common.const import mainServer, localServer

class SlaveServer:
    def __init__(self, masterObj):
        self.logger = logging.getLogger('pcmd.master.SlaveServer')

        self.masterObj = masterObj
        self.running = True
        self.slaveSocket = None

    def slaveLoop(self):
        self.slaveSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.slaveSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.slaveSocket.bind((socket.gethostname(),mainServer['PORT']))
        self.slaveSocket.listen(5)

        self.logger.debug('slaveLoop started')
        while self.running:
            try:
                (slaveSocket, address) = self.slaveSocket.accept()
            except Exception as e:
                if self.running is False:
                    break
                else:
                    self.logger.debug("slaveSocket throws %s", e)

            slaveHandlerThread = threading.Thread(
                target=self.slaveHandler,
                args=(slaveSocket,address,)
            )
            slaveHandlerThread.daemon = True
            slaveHandlerThread.start()

        self.logger.debug('slaveLoop stopped')
        return 0

    def slaveHandler(self, slaveSocket, address):
        request = slaveSocket.recv(4096)
        self.logger.debug('Received {} from {}'.format(request, address))

        msg = 'HELLO SLAVE!'
        slaveSocket.sendall(msg.encode('utf-8'))
        slaveSocket.close()

    def shutdown(self):
        self.running = False
        self.slaveSocket.shutdown(socket.SHUT_RDWR)
        self.slaveSocket.close()
