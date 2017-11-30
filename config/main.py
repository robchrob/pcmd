"""pcmd-config

Usage:
    pcmd config [--version] [--help]
                <command> [<args>...]

Commands:
    set
    get
    remove

Options:
    --help      Show this screen
    --version   Show version

"""

import enum

import config.get
import config.set
import config.remove


class CommandType(enum.Enum):
    SET = 0,
    GET = 1,
    REMOVE = 2


def main(conf):
    if conf.command is CommandType.SET:
        return config.set.main(conf)
    elif conf.command is CommandType.GET:
        return config.get.main(conf)
    elif conf.command is CommandType.REMOVE:
        return config.remove.main(conf)
