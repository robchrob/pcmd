#!/bin/python3

"""pcmd-master

Usage:
    main.py start [--attach] [--verbose]
    main.py stop [--verbose]

    main.py -h | --help
    main.py --version

Options:
    --verbose   More detailed logs.

    -h --help   Show this screen.
    --version   Show version.
"""

import sys, os
if os.path.basename(sys.path[0]) is not 'pcmd':
    sys.path.insert(0, os.path.join(sys.path[0], '..'))

import docopt
import logging

from common.const import app

import master.master
import master.start
import master.stop

def main(masterObj):
    if masterObj.cliArgs['start']:
        return master.start.main(masterObj)
    elif masterObj.cliArgs['stop']:
        return master.stop.main(masterObj)
    else:
        raise Exception("Not Implemented")

if __name__ == '__main__':
    cliArgs = docopt.docopt(
        __doc__,
        version='pcmd-master {}'.format(app['VERSION'])
    )

    masterObj = master.master.Master(cliArgs)
    sys.exit(main(masterObj))
