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

from common.message import Message
from common.status import Status as StatusObj


class Status(Message):
    def __init__(self):
        super().__init__("slave.message.status")
        self.statusFull = StatusObj()


def main(slave_root):
    if not slave_root.pidFile.running():
        slave_root.logger.error(
            'pcmd.slave is not currently running'
        )
        return 1

    if slave_root.conf.get('local_port') == "random":
        if slave_root.conf.get('local_hostname') in ("127.0.0.1", "localhost"):
            (_, port) = slave_root.pidFile.read()
        else:
            slave_root.logger.error(
                "cannot determine port for {}".format(
                    slave_root.conf.get('local_hostname')
                )
            )
            return 1
    else:
        port = int(slave_root.conf.get('local_port'))

    msg = Status()
    response = msg.send(slave_root.conf.get('local_hostname'), port)

    if response.status == 0:
        slave_root.logger.info(response.statusFull)
    else:
        slave_root.logger.error(
            'getting status of the pcmd.slave failed - err (%s)', msg.status
        )
    return msg.status
