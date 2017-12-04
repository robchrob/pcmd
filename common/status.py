import common.const


class Status:
    def __init__(self, module_type):
        self.module_type = module_type

        self.name = None
        self.hostname = None
        self.port = None
        self.lhostname = None
        self.lport = None

    def __str__(self):
        if self.module_type is common.const.ModuleType.MASTER:
            return "{} is running on {}:{}".format(
                self.name, self.lhostname, self.lport
            )

        elif self.module_type is common.const.ModuleType.SLAVE:
            return "{} is running on out: ({}:{}) local: ({}:{})".format(
                self.name, self.hostname, self.port, self.lhostname, self.lport
            )
