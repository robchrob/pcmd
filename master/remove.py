"""pcmd-master-remove

Usage:
    pcmd master remove  [--version] [--help]
                        [--verbose | --quiet]
                        [--hostname=ADDR] [--port=NUM]
                        (all | <slave_name>)

Options:
    -h ADDR, --hostname=ADDR    Specify hostname of master local
    -p NUM, --port=NUM          Specify port of master local

    -v, --verbose               More detailed logs
    -q, --quiet                 Don't write to terminal

    --help                      Show this screen
    --version                   Show version

"""

from common.message import Message


class Remove(Message):
    def __init__(self, remove_all=False, slave_name=None):
        super().__init__("master.message.remove")
        self.slave_name = slave_name
        self.remove_all = remove_all


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

    if master_root.conf.get_arg('all'):
        msg = Remove(
            True,
            None,
        )
    else:
        msg = Remove(
            False,
            master_root.conf.get_arg('<slave_name>'),
        )

    response = msg.send_get(
        master_root.conf.get('local_hostname'),
        port
    )

    if response.status != 0:
        raise response.err
    else:
        master_root.logger.info(
            'slave {} removed'.format(
                response.slave_name,
            )
        )

    return response.status
