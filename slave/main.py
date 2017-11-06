#!/bin/python3

"""pcmd-slave

Usage:
    main.py slave (start|stop)
    main.py -h | --help
    main.py --version
"""

import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import docopt

from common.const import app

import slave.start
import slave.stop

def main(cliArgs):
    if cliArgs['start']:
        return slave.start.main(cliArgs)
    elif cliArgs['stop']:
        return slave.stop.main(cliArgs)
    else:
        raise Exception("Not Implemented")

if __name__ == '__main__':
    cliArgs = docopt.docopt(
        __doc__,
        version='{} {}'.format(app['NAME'],app['VERSION'])
    )
    exit(main(cliArgs))
