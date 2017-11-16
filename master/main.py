import master.start
import master.stop


def main(master_root):
    if master_root.settings['operation'] is 'start':
        return master.start.main(master_root)
    elif master_root.settings['operation'] is 'stop':
        return master.stop.main(master_root)
    else:
        raise Exception("Not Implemented")
