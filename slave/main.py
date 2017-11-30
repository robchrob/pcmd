"""pcmd-slave

Usage:
    pcmd slave  [--version] [--help]
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

import slave.slave
import slave.slave
import slave.start
import slave.stop
import slave.status


class CommandType(enum.Enum):
    START = 0,
    STOP = 1,
    STATUS = 2,


def main(conf):
    slave_root = slave.slave.Slave(conf)
    if conf.command is CommandType.START:
        return slave.start.main(slave_root)

    elif conf.command is CommandType.STOP:
        return slave.stop.main(slave_root)

    elif conf.command is CommandType.STATUS:
        return slave.status.main(slave_root)
