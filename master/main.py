"""pcmd-master

Usage:
    pcmd master [--version] [--help]
                <command> [<args>...]

Commands:
    start
    stop
    status

Options:
    --help      Show this screen
    --version   Show version

"""

import enum

import master.master
import master.start
import master.stop
import master.status


class CommandType(enum.Enum):
    START = 0,
    STOP = 1,
    STATUS = 2,


def main(conf):
    master_root = master.master.Master(conf)
    if conf.command is CommandType.START:
        return master.start.main(master_root)

    elif conf.command is CommandType.STOP:
        return master.stop.main(master_root)

    elif conf.command is CommandType.STATUS:
        return master.status.main(master_root)
