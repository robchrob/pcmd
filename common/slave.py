import socket

import common


class Ping(common.message.Message):
    def __init__(self, slave):
        super().__init__("common.slave.ping")
        self.slave = slave


class Slave:
    def __init__(self, name, hostname, port):
        self.name = name
        self.hostname = hostname
        self.port = port

        self.env = None

    def __eq__(self, other):
        return self.name == other.name

    def ping(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((
                self.hostname,
                int(self.port),
            ))

            Ping(self).send(sock)

            response = common.util.recvmsg(sock)
            self.env = response.env
        finally:
            sock.close()


class SlaveExists(Exception):
    pass


class SlaveNotFound(Exception):
    pass


class EnvNotFound(Exception):
    pass
