"""pcmd-master-env

Usage:
    pcmd master env  [--version] [--help]
                     [--verbose | --quiet]
                     [--hostname=ADDR] [--port=NUM]
                     <slave_name> <env>

Options:
    -h ADDR, --hostname=ADDR    Specify hostname of master local
    -p NUM, --port=NUM          Specify port of master local

    -v, --verbose               More detailed logs
    -q, --quiet                 Don't write to terminal

    --help                      Show this screen
    --version                   Show version

"""

from common.message import Message

from common.slave import SlaveNotFound, EnvNotFound


class Env(Message):
    def __init__(self, slave_name, env_name):
        super().__init__("master.message.env")
        self.slave_name = slave_name
        self.env_name = env_name
        self.env_val = None


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

    msg = Env(
        master_root.conf.get_arg('<slave_name>'),
        master_root.conf.get_arg('<env>'),
    )

    response = msg.send_get(
        master_root.conf.get('local_hostname'),
        port
    )

    if response.status != 0:
        try:
            raise response.err
        except SlaveNotFound:
            master_root.logger.error(
                'no slave named {}'.format(response.slave_name)
            )
            return 1
        except EnvNotFound:
            master_root.logger.error(
                'no environment variable {} found for {}'.format(
                    response.env_name,
                    response.slave_name,
                )
            )
            return 1
    else:
        master_root.logger.info(
            "{}".format(response.env_val)
        )

    return response.status
