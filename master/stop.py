"""pcmd-master-stop

Usage:
    pcmd master stop    [--version] [--help]
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
import common.connection


class Stop(Message):
    def __init__(self):
        super().__init__("master.message.stop")


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

    response = Stop().send_get(host, port)

    if response.status == 0:
        master_root.logger.debug(
            'stopping the pcmd.master'
        )
    else:
        master_root.logger.error(
            'stopping the pcmd.master failed'
        )

    return response.status
