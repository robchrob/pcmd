"""pcmd-master-exec

Usage:
    pcmd master exec    [--version] [--help]
                        [--hostname=ADDR] [--port=NUM]
                        [--verbose | --quiet]
                        <cmd>

Options:
    -h ADDR, --hostname=ADDR    Specify hostname of master
    -p NUM, --port=NUM          Specify port of master

    -v, --verbose               More detailed logs
    -q, --quiet                 Don't write to terminal

    --help                      Show this screen
    --version                   Show version

"""

import socket

from common.run import DataType
from common.message import Message
import common


class Exec(Message):
    def __init__(self, cmd):
        super().__init__("master.message.exec")
        self.cmd = cmd
        self.stdout = ""


def main(master_root):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((
            master_root.conf.get('hostname'),
            int(master_root.conf.get('port')),
        ))

        msg = Exec(master_root.conf.args['<cmd>'])
        msg.send_just(sock)

        while True:
            response = common.util.recvmsg(sock)

            if response.type == DataType.LINE:
                master_root.logger.info(response.obj)
                Message("master.exec.line.get").send_just(sock)
            elif response.type == DataType.MSG:
                break

    except KeyboardInterrupt:
        return 1
    finally:
        response = common.util.recvmsg(sock)
        sock.close()

    return response.obj.status
