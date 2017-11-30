import enum


class ModuleType(enum.Enum):
    MASTER = 0,
    SLAVE = 1,
    CONFIG = 2


app = dict(
    VERSION="0.1",
)
version = "pcmd {}".format(app['VERSION'])
