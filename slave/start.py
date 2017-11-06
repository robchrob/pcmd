#!/bin/python3

"""pcmd-slave-start

Usage:
    start.py
    start.py -h | --help
    start.py --version
"""

import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import docopt
import socket

from common.const import app, server

import slave.main
import slave.stop

def main(cliArgs):
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((server['HOST'],server['PORT']))

    msg = 'HELLO SERVER!'
    clientSocket.sendall(msg.encode('utf-8'))

    response = clientSocket.recv(4096)
    print('Received {}'.format(response))

    return slave.stop.main(cliArgs)

if __name__ == '__main__':
    cliArgs = docopt.docopt(
        __doc__,
        version='{} {}'.format(app['NAME'],app['VERSION'])
    )
    exit(main(cliArgs))
