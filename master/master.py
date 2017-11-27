import logging
import pickle

from common.const import mainServer
from common.pidfile import ServiceType, PidFile
import common.server
import common.util

import master.stop


class Master:
    def __init__(self, cli_args):
        self.logger = logging.getLogger('pcmd.master.Master')
        self.settings = get_settings(cli_args)

        self.pidFile = PidFile(ServiceType.MASTER)
        self.localServer = None
        self.slaveServer = None

        self.logger.debug('created instance of pcmd.master.Master')

    def loop(self):
        self.localServer = common.server.Server(
            "pcmd.master.localServer",
            "127.0.0.1",
            common.util.random_port(),
            self.local_handler,
        )

        self.slaveServer = common.server.Server(
            "pcmd.master.slaveServer",
            mainServer['HOST'],
            mainServer['PORT'],
            self.slave_handler,
        )

        if self.pidFile.running():
            self.logger.error(
                "pcmd.master is already running with pid %d",
                self.pidFile.runningPid,
            )
            return 1
        else:
            self.pidFile.create(self.localServer.port)

        self.logger.debug("starting pcmd.master with pid %d", self.pidFile.pid)

        try:
            self.localServer.thread.join()
            self.slaveServer.thread.join()
        except KeyboardInterrupt:
            return master.stop.main(self)

        return 0

    def local_handler(self, communication, address):
        request = communication.recv(4096)
        # TODO validate object
        request_obj = pickle.loads(request)

        self.logger.debug(
            'Received {} from {}'.format(request_obj.name, address)
        )

        if request_obj.name == 'master.message.stop':
            shutdown_status = self.shutdown()
            request_obj.status = shutdown_status
            request_obj.respond(communication)

        communication.close()

    def slave_handler(self, communication, address):
        request = communication.recv(4096)
        self.logger.debug('Received {} from {}'.format(request, address))

        msg = 'HELLO SLAVE!'
        communication.sendall(msg.encode('utf-8'))
        communication.close()

    def shutdown(self):
        local_status = self.localServer.shutdown()
        slave_status = self.slaveServer.shutdown()

        return local_status or slave_status


def get_settings(cli_args):
    settings = {}

    if cli_args['start']:
        settings['operation'] = 'start'
    elif cli_args['stop']:
        settings['operation'] = 'stop'

    if cli_args['--attach']:
        settings['attach'] = True
    else:
        settings['attach'] = False

    return settings
