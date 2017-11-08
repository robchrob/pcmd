#!/bin/python3

"""pcmd-master-start

Usage:
    start.py [--attach] [--verbose]
    start.py -h | --help
    start.py --version

Options:
    --verbose   More detailed logs.

    -h --help   Show this screen.
    --version   Show version.
"""

import sys, os
if os.path.basename(sys.path[0]) is not 'pcmd':
    sys.path.insert(0, os.path.join(sys.path[0], '..'))

import docopt
from multiprocessing import Process

from common.const import app

import master.master

def main(masterObj):
    if masterObj.cliArgs['--attach']:
        masterObj.logger.info("Running server in attached mode")
        return masterObj.masterLoop()
    else:
        p = Process(
            target=masterObj.masterLoop,
        )
        p.start()

        os._exit(0)

if __name__ == '__main__':
    cliArgs = docopt.docopt(
        __doc__,
        version='pcmd-master-start {}'.format(app['VERSION'])
    )

    masterObj = master.master.Master(cliArgs)
    sys.exit(main(masterObj))
