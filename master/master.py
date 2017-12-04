import logging

import common.server
import common.util
import master.stop

from common.const import ModuleType
from common.pidfile import PidFile
from common.slave import SlaveNotFound, SlaveExists, EnvNotFound
from common.run import DataType
from common.message import Message


class Master:
    def __init__(self, conf):
        self.logger = logging.getLogger('pcmd.master.Master')
        self.local = False
        self.conf = conf

        self.pidFile = PidFile(ModuleType.MASTER)
        self.localServer = None

        self.slaves = []

        self.logger.debug('created instance of pcmd.master.Master')

    def loop(self):
        self.localServer = common.server.Server(
            "pcmd.master.localServer",
            self.conf.get('local_hostname'),
            self.conf.get('local_port'),
            self.local_handler,
        )

        if self.pidFile.running():
            self.logger.error(
                "pcmd.master is already running with pid %d",
                self.pidFile.runningPid,
            )
            return 1
        else:
            self.pidFile.create(self.localServer.port)
            self.local = True

        self.logger.debug("starting pcmd.master with pid %d", self.pidFile.pid)

        try:
            self.localServer.thread.join()
        except KeyboardInterrupt:
            return master.stop.main(self)

        return 0

    def local_handler(self, communication, address):
        request_obj = common.util.recvmsg(communication)

        self.logger.debug(
            'master.localServer received {} from {}'.format(
                request_obj.name,
                address
            )
        )

        if request_obj.name == 'master.message.stop':
            request_obj.status = self.shutdown()
            if request_obj.status == 0:
                self.pidFile.remove()
            request_obj.send(communication)

        elif request_obj.name == 'master.message.status':
            request_obj.statusFull = self.fill_status(request_obj.statusFull)
            request_obj.status = 0
            request_obj.send(communication)

        elif request_obj.name == 'master.message.add':
            try:
                request_obj.status = self.add_slave(request_obj)
            except ConnectionRefusedError as e:
                request_obj.status = 1
                request_obj.err = e

            request_obj.send(communication)

        elif request_obj.name == 'master.message.exec':
            slave = self.get_slave(request_obj.slave_name)

            if slave is not None:
                try:
                    slave.ping()
                except Exception as e:
                    request_obj.status = 1
                    request_obj.err = e
                    request_obj.send(communication)
                    communication.close()
                    return

                sock = request_obj.send_to(
                    slave.hostname,
                    int(slave.port),
                )
                try:
                    while True:
                        response = common.util.recvmsg(sock)
                        response.send(communication)

                        if response.type == DataType.LINE:
                            Message("master.exec.line.get").send(sock)
                        elif response.type == DataType.MSG:
                            break

                        client_response = common.util.recvmsg(communication)
                        if client_response.name == "master.exec.interrupt":
                            break
                finally:
                    sock.close()
            else:
                request_obj.err = SlaveNotFound
                request_obj.status = 1
                request_obj.send(communication)

        elif request_obj.name == 'master.message.remove':
            request_obj.status = self.remove_slave(request_obj)
            request_obj.send(communication)

        elif request_obj.name == 'master.message.list':
            request_obj.slaves = self.slaves
            request_obj.status = 0
            request_obj.send(communication)

        elif request_obj.name == 'master.message.env':
            try:
                env_val = self.get_env(
                    request_obj.slave_name,
                    request_obj.env_name
                )
                request_obj.env_val = env_val
                request_obj.status = 0
            except EnvNotFound as e:
                request_obj.err = e
                request_obj.status = 1
            except SlaveNotFound as e:
                request_obj.err = e
                request_obj.status = 1

            request_obj.send(communication)

        communication.close()

    def shutdown(self):
        local_status = self.localServer.shutdown()

        return local_status

    def fill_status(self, obj):
        obj.name = "pcmd.master"
        obj.lhostname = self.localServer.address
        obj.lport = self.localServer.port

        return obj

    def get_slave(self, name):
        for slave in self.slaves:
            if slave.name == name:
                return slave
        return None

    def add_slave(self, obj):
        for slave in self.slaves:
            if slave.name == obj.slave.name:
                if not (slave.hostname == obj.slave.hostname
                        and slave.port == obj.slave.port):
                    obj.err = SlaveExists(
                        "{} is already added".format(
                            obj.slave.name)
                    )
                    return 1
                else:
                    try:
                        obj.slave.ping()
                    except Exception as e:
                        obj.err = e
                        raise e
                    return 0

        try:
            obj.slave.ping()
        except Exception as e:
            obj.err = SlaveExists
            raise e

        self.slaves.append(obj.slave)
        return 0

    def get_env(self, slave_name, env_name):
        for slave in self.slaves:
            if slave.name == slave_name:
                try:
                    return slave.env[env_name]
                except KeyError:
                    raise EnvNotFound
        raise SlaveNotFound

    def remove_slave(self, obj):
        if obj.remove_all:
            self.slaves.clear()
        else:
            for idx, slave in enumerate(self.slaves):
                if slave.name == obj.slave_name:
                    self.slaves.pop(idx)

        return 0
