#!/bin/python3

"""pcmd-master-stop

Usage:
    stop.py [--verbose]
    stop.py -h | --help
    stop.py --version

Options:
    --verbose   More detailed logs.

    -h --help   Show this screen.
    --version   Show version.
"""

import sys, os
if os.path.basename(sys.path[0]) is not 'pcmd':
    sys.path.insert(0, os.path.join(sys.path[0], '..'))

import docopt
import socket

from common.const import app, localServer

import master.master

def main(masterObj):
    if not masterObj.pidF.isRunning():
        masterObj.logger.error(
            "pcmd master is not currently running"
        )
        return 1
    else:
        (pid, port) = masterObj.pidF.read()

    localSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        localSocket.connect(("localhost",port))
        localSocket.sendall(bytes('stop', 'utf-8'))
    finally:
        localSocket.close()

    return 0

if __name__ == '__main__':
    cliArgs = docopt.docopt(
        __doc__,
        version='pcmd-master-stop {}'.format(app['VERSION'])
    )

    masterObj = master.master.Master(cliArgs)
    sys.exit(main(masterObj))
