#!/bin/python3

"""pcmd-master-start

Usage:
    start.py
    start.py -h | --help
    start.py --version
"""

import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import docopt
import socket
import threading

from common.const import app, server

import master.main
import master.stop

def clientHandler(clientSocket):
    request = clientSocket.recv(4096)
    print('Received {}'.format(request))

    msg = 'HELLO CLIENT!'
    clientSocket.sendall(msg.encode('utf-8'))
    clientSocket.close()

def main(cliArgs):
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((server['HOST'],server['PORT']))
    serverSocket.listen(5)

    while True:
        (clientSocket, address) = serverSocket.accept()

        clientThread = threading.Thread(
            target=clientHandler,
            args=(clientSocket,)
        )
        clientThread.start()

    return master.stop.main(cliArgs)

if __name__ == '__main__':
    cliArgs = docopt.docopt(
        __doc__,
        version='{} {}'.format(app['NAME'],app['VERSION'])
    )
    exit(main(cliArgs))
