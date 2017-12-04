"""pcmd-master-list

Usage:
    pcmd master list [--version] [--help]
                     [--verbose | --quiet]
                     [--hostname=ADDR] [--port=NUM]

Options:
    -h ADDR, --hostname=ADDR    Specify hostname of master local
    -p NUM, --port=NUM          Specify port of master local

    -v, --verbose               More detailed logs
    -q, --quiet                 Don't write to terminal

    --help                      Show this screen
    --version                   Show version

"""

from common.message import Message


class List(Message):
    def __init__(self):
        super().__init__("master.message.list")
        self.slaves = None


def main(master_root):
    if (
            master_root.conf.get('local_hostname') in
            ("127.0.0.1", "localhost") or
            master_root.local
    ):
        if not master_root.pidFile.running():
            master_root.logger.error(
                'pcmd master is not currently running'
            )
            return 1
        else:
            (_, port) = master_root.pidFile.read()
    else:
        if master_root.conf.get('local_port') == "random":
            master_root.logger.error(
                "cannot determine port for {}".format(
                    master_root.conf.get('local_hostname')
                )
            )
            return 1
        else:
            port = int(master_root.conf.get('local_port'))

    msg = List()

    response = msg.send_get(
        master_root.conf.get('local_hostname'),
        port
    )

    if response.status != 0:
        try:
            raise response.err
        except Exception as e:
            raise e
    else:
        for slave in response.slaves:
            if not master_root.conf.get_arg('--verbose'):
                master_root.logger.info(
                    "{}".format(slave.name)
                )
            else:
                master_root.logger.info(
                    "{} - {}:{}".format(slave.name, slave.hostname, slave.port)
                )

    return response.status
