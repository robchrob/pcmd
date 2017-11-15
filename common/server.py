import socket
import os
import threading
import logging
from multiprocessing import Process

from common.const import mainServer

class Server:
    def __init__(self, name, address, port, handlerFunction):
        self.name = name
        self.logger = logging.getLogger(name)

        self.address = address

        if port == -1:
            self.port = self.getRandomPort()
        else:
            self.port = port

        self.serverSocket = None
        self.handlerFunction = handlerFunction
        self.running = False

    def getRandomPort(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("",0))
        port = sock.getsockname()[1]
        sock.close()

        return port

    def loop(self):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.serverSocket.bind((self.address,self.port))
        self.serverSocket.listen(5)

        self.logger.debug('{} started'.format(self.name))
        self.running = True
        while True:
            try:
                (commSocket, address) = self.serverSocket.accept()
            except Exception as e:
                if self.running is False:
                    break
                else:
                    self.logger.error("{} throws %s".format(self.name), e)
                    return 1

            localThread = threading.Thread(
                target=self.handlerFunction,
                args=(commSocket,address,)
            )
            localThread.start()

        self.logger.debug('{} stopped cleanly'.format(self.name))
        return 0

    def shutdown(self):
        self.running = False
        self.serverSocket.shutdown(socket.SHUT_RDWR)
        self.serverSocket.close()

        return 0
