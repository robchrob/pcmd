import os
import multiprocessing


def main(master_root):
    if master_root.conf.get('attach'):
        master_root.logger.info("server in attached mode")
        return master_root.loop()
    else:
        p = multiprocessing.Process(
            target=master_root.loop,
        )
        p.start()

        os._exit(0)
