#!/bin/python3

"""pcmd-master-stop

Usage:
    start.py
    start.py -h | --help
    start.py --version
"""

import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import docopt

from common.const import app

def main(cliArgs):
    return 0

if __name__ == '__main__':
    cliArgs = docopt.docopt(
        __doc__,
        version='{} {}'.format(app['NAME'],app['VERSION'])
    )
    sys.exit(main(cliArgs))
