import socket
import pickle
import struct

import common.util


class Message:
    def __init__(self, name):
        self.name = name
        self.err = None
        self.status = -1

    def send_get(self, hostname, port):
        serialized = pickle.dumps(self)
        serialized = struct.pack('>I', len(serialized)) + serialized

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((hostname, port))
            sock.sendall(serialized)
            response = common.util.recvmsg(sock)
        finally:
            sock.close()

        return response

    def send(self, sock):
        to_send = pickle.dumps(self)
        to_send = struct.pack('>I', len(to_send)) + to_send
        sock.sendall(to_send)

    def send_to(self, hostname, port):
        to_send = pickle.dumps(self)
        to_send = struct.pack('>I', len(to_send)) + to_send
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((hostname, port))
        sock.sendall(to_send)

        return sock
