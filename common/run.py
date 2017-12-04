import subprocess
import enum

import common


class DataType(enum.Enum):
    LINE = 0,
    MSG = 1,


class Data(common.message.Message):
    def __init__(self, type_, obj):
        super().__init__("common.run.data")
        self.type = type_
        self.obj = obj


def execute(msg, comm):
    proc = subprocess.Popen(
        msg.cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    for line in proc.stdout:
        line_str = line.decode('utf-8').strip('\n')

        Data(DataType.LINE, line_str).send(comm)
        response = common.util.recvmsg(comm)

        if response is None or response.name != "master.exec.line.get":
            proc.kill()
            return 1

    proc.wait()
    msg.status = proc.returncode
    Data(DataType.MSG, msg).send(comm)

    return 0
