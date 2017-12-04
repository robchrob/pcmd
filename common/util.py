import os
import socket
import threading
import logging
import struct
import pickle

import common

logger = logging.getLogger('pcmd.common.Util')


def process_exist(pid):
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


def spawn_thread(name, func):
    thread = threading.Thread(
        target=func,
    )
    thread.name = name
    logger.debug("thread %s created", thread.getName())

    return thread


def random_port():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("", 0))
    port = sock.getsockname()[1]
    sock.close()

    logger.debug("random port %s is open", port)

    return port


def recvall(sock, n):
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data


def recvmsg(sock):
    raw_len = common.util.recvall(sock, 4)

    if not raw_len:
        return None

    msg_len = struct.unpack('>I', raw_len)[0]
    raw_obj = common.util.recvall(sock, msg_len)

    if raw_obj is None:
        return None

    return pickle.loads(raw_obj)


def read_file(path):
    with open(path, 'r') as f:
        return f.read()
