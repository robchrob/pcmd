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


class Status(Message):
    def __init__(self):
        super().__init__("master.message.status")
        self.statusFull = StatusObj()


def main(master_root):
    if not master_root.pidFile.running():
        master_root.logger.error(
            'pcmd.master is not currently running'
        )
        return 1

    if master_root.conf.get('local_port') == "random":
        if master_root.conf.get('local_hostname') in ("127.0.0.1", "localhost"):
            (_, port) = master_root.pidFile.read()
        else:
            master_root.logger.error(
                "cannot determine port for {}".format(
                    master_root.conf.get('local_hostname')
                )
            )
            return 1
    else:
        port = int(master_root.conf.get('local_port'))

    msg = Status()
    response = msg.send(master_root.conf.get('local_hostname'), port)

    if response.status == 0:
        master_root.logger.info(response.statusFull)
    else:
        master_root.logger.error(
            'getting status of the pcmd.master failed - err (%s)', msg.status
        )
    return msg.status
