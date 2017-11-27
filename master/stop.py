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

    (_, port) = master_root.pidFile.read()

    msg = Stop()
    response = msg.send('127.0.0.1', port)

    if response.status == 0:
        master_root.pidFile.remove()
    else:
        master_root.logger.error(
            'stopping the pcmd.master failed - err (%s)', msg.status
        )
    return msg.status
