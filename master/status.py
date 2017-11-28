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

    (_, port) = master_root.pidFile.read()

    msg = Status()
    response = msg.send('127.0.0.1', port)

    if response.status == 0:
        master_root.logger.info(response.statusFull)
    else:
        master_root.logger.error(
            'getting status of the pcmd.master failed - err (%s)', msg.status
        )
    return msg.status
