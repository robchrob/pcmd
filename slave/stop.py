"""pcmd-slave-stop

Usage:
    pcmd slave stop [--version] [--shelp]
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

from common.message import Message
import common.connection


class Stop(Message):
    def __init__(self):
        super().__init__("slave.message.stop")


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

    response = Stop().send_get(host, port)
    if response.status == 0:
        slave_root.logger.debug(
            'stopping the pcmd.slave'
        )
    else:
        slave_root.logger.error(
            'stopping the pcmd.slave failed'
        )

    return response.status
