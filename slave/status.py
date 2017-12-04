"""pcmd-slave-status

Usage:
    pcmd slave status   [--version] [--help]
                        [--hostname=ADDR] [--port=NUM]
                        [--verbose | --quiet]

Options:
    -h ADDR, --hostname=ADDR    Specify hostname of slave local
    -p NUM, --port=NUM          Specify port of slave local

    -v, --verbose               More detailed logs
    -q, --quiet                 Don't write to terminal

    --help                      Show this screen
    --version                   Show version

"""
from common.const import ModuleType
from common.message import Message
from common.status import Status as StatusObj
import common.connection


class Status(Message):
    def __init__(self, module_type):
        super().__init__("slave.message.status")
        self.statusFull = StatusObj(module_type)


def main(slave_root):
    try:
        host, port = common.connection.get(slave_root)
    except common.connection.NotCurrentlyRunning:
        slave_root.logger.error(
            'pcmd.slave is not running'
        )
        return 1
    except common.connection.PortNotValid:
        slave_root.logger.error(
            'cannot determine port for pcmd.slave'
        )
        return 1

    response = Status(ModuleType.SLAVE).send_get(host, port)

    if response.status == 0:
        slave_root.logger.info(response.statusFull)
    else:
        slave_root.logger.error(
            'getting status of the pcmd.slave failed'
        )

    return response.status
