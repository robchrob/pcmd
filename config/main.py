import enum


class CommandType(enum.Enum):
    SET = 0,
    GET = 1,
    REMOVE = 2


def main(conf):
    if conf.command is CommandType.SET:
        # return master.start.main(master_root)
        pass
    elif conf.command is CommandType.GET:
        # return master.stop.main(master_root)
        pass
    elif conf.command is CommandType.REMOVE:
        # return master.status.main(master_root)
        pass
    else:
        raise Exception("Not Implemented")
