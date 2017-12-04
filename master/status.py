"""pcmd-master-status

Usage:
    pcmd master status  [--version] [--help]
                        [--hostname=ADDR] [--port=NUM]
                        [--verbose | --quiet]

Options:
    -h ADDR, --hostname=ADDR    Specify hostname of master local
    -p NUM, --port=NUM          Specify port of master local

    -v, --verbose               More detailed logs
    -q, --quiet                 Don't write to terminal

    --help                      Show this screen
    --version                   Show version

"""

from common.message import Message
from common.status import Status as StatusObj
from common.const import ModuleType
import common.connection


class Status(Message):
    def __init__(self, module_type):
        super().__init__("master.message.status")
        self.statusFull = StatusObj(module_type)


def main(master_root):
    try:
        host, port = common.connection.get(master_root)
    except common.connection.NotCurrentlyRunning:
        master_root.logger.error(
            'pcmd.master is not running'
        )
        return 1
    except common.connection.PortNotValid:
        master_root.logger.error(
            'cannot determine port for pcmd.master'
        )
        return 1

    msg = Status(ModuleType.MASTER)
    response = msg.send_get(host, port)

    if response.status == 0:
        master_root.logger.info(response.statusFull)
    else:
        master_root.logger.error(
            'getting status of the pcmd.master failed'
        )

    return response.status
