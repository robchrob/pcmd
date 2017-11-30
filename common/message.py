import socket
import pickle
import struct


class Message:
    def __init__(self, name):
        if name != "":
            self.name = name
        else:
            self.name = "master.message"

        self.status = -1

    def send(self, hostname, port):
        serialized = pickle.dumps(self)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((hostname, port))
            sock.sendall(serialized)
            response = sock.recv(4096)
        finally:
            sock.close()

        response_obj = pickle.loads(response)

        return response_obj

    def send_just(self, sock):
        to_send = pickle.dumps(self)
        to_send = struct.pack('>I', len(to_send)) + to_send
        sock.sendall(to_send)

    def respond(self, sock):
        serialized = pickle.dumps(self)
        sock.sendall(serialized)
