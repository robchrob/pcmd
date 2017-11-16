import logging
import socket
import threading

from common import util


class Server:
    def __init__(self, name, address, port, handler_function):
        self.name = name
        self.logger = logging.getLogger(name)

        self.address = address
        self.port = port

        self.serverSocket = None
        self.handlerFunction = handler_function
        self.running = False

        self.thread = util.spawn_thread(self.name, self.loop)

    def loop(self):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.serverSocket.bind((self.address, self.port))
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

            handler_thread = threading.Thread(
                target=self.handlerFunction,
                args=(commSocket, address,)
            )
            handler_thread.start()

        self.logger.debug('{} stopped cleanly'.format(self.name))
        return 0

    def start(self):
        self.logger.debug("thread for server %s started", self.name)
        self.thread.start()

    def shutdown(self):
        self.running = False
        self.serverSocket.shutdown(socket.SHUT_RDWR)
        self.serverSocket.close()

        return 0
