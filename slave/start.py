"""pcmd-slave-start

Usage:
    pcmd slave start    [--version] [--help]
                        [--attach]
                        [--hostname=ADDR] [--port=NUM]
                        [--lhostname=ADDR] [--lport=NUM]
                        [--verbose | --quiet]

Options:
    -a, --attach                Attach to the terminal

    -h ADDR, --hostname=ADDR    Specify hostname
    -p NUM, --port=NUM          Specify port

    --lhostname=ADDR            Hostname for local communication
    --lport=NUM                 Port for local communication

    -v, --verbose               More detailed logs
    -q, --quiet                 Don't write to terminal

    --help                      Show this screen
    --version                   Show version

"""

import os
import multiprocessing


def main(slave_root):
    if slave_root.conf.get('attach').lower() == 'true':
        slave_root.logger.info("server in attached mode")
        return slave_root.loop()
    else:
        p = multiprocessing.Process(
            target=slave_root.loop,
        )
        p.start()

        os._exit(0)
