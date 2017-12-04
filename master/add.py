"""pcmd-master-add

Usage:
    pcmd master add [--version] [--help]
                    [--verbose | --quiet]
                    [--hostname=ADDR] [--port=NUM]
                    <name> <hostname> <port>

Options:
    -h ADDR, --hostname=ADDR    Specify hostname of master local
    -p NUM, --port=NUM          Specify port of master local

    -v, --verbose               More detailed logs
    -q, --quiet                 Don't write to terminal

    --help                      Show this screen
    --version                   Show version

"""

from common.message import Message
from common.slave import Slave
from common.slave import SlaveExists


class Add(Message):
    def __init__(self, name, hostname, port):
        super().__init__("master.message.add")
        self.slave = Slave(name, hostname, port)


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

    if master_root.conf.get_arg('<name>') == 'all':
        master_root.logger.error(
            'all is reserved name'
            )
        return 1

    msg = Add(
        master_root.conf.get_arg('<name>'),
        master_root.conf.get_arg('<hostname>'),
        master_root.conf.get_arg('<port>'),
    )

    response = msg.send_get(
        master_root.conf.get('local_hostname'),
        port
    )

    if response.status != 0:
        try:
            raise response.err
        except SlaveExists as e:
            master_root.logger.error(
                '{}'.format(e)
            )
            return 1
        except ConnectionRefusedError:
            master_root.logger.error(
                'cannot connect to slave {}'.format(
                    master_root.conf.get_arg('<name>')
                )
            )
            return 1
    else:
        master_root.logger.info(
            'slave {} ({}:{}) added'.format(
                response.slave.name,
                response.slave.hostname,
                response.slave.port,
            )
        )

    return response.status
