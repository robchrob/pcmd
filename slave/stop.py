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


class Stop(Message):
    def __init__(self):
        super().__init__("slave.message.stop")


def main(slave_root):
    # TODO stop remotely
    if not slave_root.pidFile.running():
        slave_root.logger.error(
            'pcmd slave is not currently running'
        )
        return 1

    if slave_root.conf.get('local_port') == "random":
        if slave_root.conf.get('local_hostname') in ("127.0.0.1", "localhost"):
            (_, port) = slave_root.pidFile.read()
        elif slave_root.local:
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

    msg = Stop()
    response = msg.send(slave_root.conf.get('local_hostname'), port)

    if response.status == 0:
        slave_root.pidFile.remove()
    else:
        slave_root.logger.error(
            'stopping the pcmd.slave failed - err (%s)', msg.status
        )
    return msg.status
