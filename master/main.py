#!/bin/python3

"""pcmd-master

Usage:
    main.py (start|stop) [--verbose=<level>]
    main.py -h | --help
    main.py --version

Options:
    --verbose=<level> Level of log detail, 1-3 [default: 1].

    -h --help     Show this screen.
    --version     Show version.
"""

import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import docopt

from common.const import app

import master.start
import master.stop

def main(cliArgs):
    if cliArgs['start']:
        return master.start.main(cliArgs)
    elif cliArgs['stop']:
        return master.stop.main(cliArgs)
    else:
        raise Exception("Not Implemented")

if __name__ == '__main__':
    cliArgs = docopt.docopt(
        __doc__,
        version='{} {}'.format(app['NAME'],app['VERSION'])
    )
    sys.exit(main(cliArgs))
