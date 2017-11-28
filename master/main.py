import enum

import master.start
import master.stop
import master.status


class CommandType(enum.Enum):
    START = 0,
    STOP = 1,
    STATUS = 2,
    EXEC = 3


def main(master_root):
    if master_root.conf.command is CommandType.START:
        return master.start.main(master_root)

    elif master_root.conf.command is CommandType.STOP:
        return master.stop.main(master_root)

    elif master_root.conf.command is CommandType.STATUS:
        return master.status.main(master_root)

    elif master_root.conf.command is CommandType.EXEC:
        return master.status.main(master_root)

    else:
        raise Exception("Not Implemented")
