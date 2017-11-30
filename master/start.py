"""pcmd-master-start

Usage:
    pcmd master start [--version] [--help]
                      [--attach] [--hostname] [--port=NUM] [-v|-q]

Options:
    -a, --attach            Attach to the terminal
    -h, --hostname          Specify different hostname
    -p NUM, --port=NUM      Specify different port
    -v, --verbose           More detailed logs
    -q, --quiet             Don't write to terminal
    --help                  Show this screen
    --version               Show version

"""

import os
import multiprocessing


def main(master_root):
    if master_root.conf.get('attach').lower() == 'true':
        master_root.logger.info("server in attached mode")
        return master_root.loop()
    else:
        p = multiprocessing.Process(
            target=master_root.loop,
        )
        p.start()

        os._exit(0)
