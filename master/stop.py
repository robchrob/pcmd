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


class Stop(Message):
    def __init__(self):
        super().__init__("master.message.stop")


def main(master_root):
    if not master_root.pidFile.running():
        master_root.logger.error(
            'pcmd master is not currently running'
        )
        return 1

    if master_root.conf.get('local_port') == "random":
        if master_root.conf.get('local_hostname') in ("127.0.0.1", "localhost"):
            (_, port) = master_root.pidFile.read()
        elif master_root.local:
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

    msg = Stop()
    response = msg.send(master_root.conf.get('local_hostname'), port)

    if response.status == 0:
        master_root.pidFile.remove()
    else:
        master_root.logger.error(
            'stopping the pcmd.master failed - err (%s)', msg.status
        )
    return msg.status
