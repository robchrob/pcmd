"""pcmd-master-exec

Usage:
    pcmd master exec    [--version] [--help]
                        [--verbose | --quiet]
                        <slave_name> (cmd|file) <arg>

Options:
    -v, --verbose               More detailed logs
    -q, --quiet                 Don't write to terminal

    --help                      Show this screen
    --version                   Show version

"""

from common.run import DataType
from common.message import Message

import common
import common.util
from common.slave import SlaveNotFound


class Exec(Message):
    def __init__(self, cmd, name):
        super().__init__("master.message.exec")
        self.slave_name = name
        self.cmd = cmd


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

    if master_root.conf.args['file']:
        cmd = common.util.read_file(master_root.conf.args['<arg>'])
    else:
        cmd = master_root.conf.args['<arg>']

    msg = Exec(
        cmd,
        master_root.conf.args['<slave_name>'],
    )

    sock = msg.send_to(
        master_root.conf.get('local_hostname'),
        port
    )
    try:
        while True:
            response = common.util.recvmsg(sock)

            if response.err is not None:
                raise response.err

            if response.type == DataType.LINE:
                master_root.logger.info(response.obj)
                Message("master.exec.line.get").send(sock)
            elif response.type == DataType.MSG:
                break
    except KeyboardInterrupt:
        Message("master.exec.interrupt").send(sock)
        return 1
    except SlaveNotFound:
        master_root.logger.error("slave not found")
        return 1
    except ConnectionRefusedError:
        master_root.logger.error(
            'cannot connect to slave {}'.format(
                master_root.conf.get_arg('<slave_name>')
            )
        )
        return 1
    finally:
        sock.close()

    return response.status
