"""
[core]
    verbose = false
    quiet = false

[master]
    hostname = 0.0.0.0
    port = 1337
    attach = false

[slave]
    port = 1338
"""

import logging
import configparser

import config.util

from common.const import ModuleType
from master.main import CommandType as MasterCommand
from config.main import CommandType as ConfigCommand


class Configuration:
    def __init__(self, cli_args):
        self.logger = logging.getLogger('pcmd.config.Configuration')

        self.module = get_module(cli_args)
        self.command = get_command(self.module, cli_args)

        self.conf = self.read_all(cli_args)

        self.logger.debug(self)

    def get(self, key, section=None):
        if section is None:
            section = self.module.name.lower()
        return self.conf.get(section, key)

    def __str__(self):
        out = "\n"
        for section in self.conf.sections():
            out += "[{}]\n".format(section)
            for (key, val) in self.conf.items(section):
                out += "\t{} = {}\n".format(key, val)
            out += "\n"
        return out

    def read_all(self, cli_args):
        conf = self.read_default()
        conf = self.add_userconf(conf, cli_args)
        conf = add_params(conf, cli_args)
        return conf

    def read_default(self):
        conf = configparser.ConfigParser()
        conf.read_string(__doc__)
        self.logger.debug("default configuration loaded")
        return conf

    def add_userconf(self, default_conf, cli_args):
        user_conf = config.util.get_userconf(cli_args)

        if user_conf:
            default_conf.read_dict(user_conf)
            self.logger.debug("user configuration merged with defaults")

        return default_conf


def get_module(cli_args):
    if cli_args['master']:
        return ModuleType.MASTER
    elif cli_args['slave']:
        return ModuleType.SLAVE
    elif cli_args['config']:
        return ModuleType.CONFIG
    else:
        raise Exception('unknown module type')


def get_command(module_type, cli_args):
    if module_type is ModuleType.MASTER:
        if cli_args['start']:
            return MasterCommand.START
        elif cli_args['stop']:
            return MasterCommand.STOP
        elif cli_args['status']:
            return MasterCommand.STATUS
        elif cli_args['exec']:
            return MasterCommand.EXEC
        else:
            raise Exception('unknown master command type')

    elif module_type is ModuleType.SLAVE:
        raise Exception('Not Implemented')

    elif module_type is ModuleType.CONFIG:
        if cli_args['set']:
            return ConfigCommand.SET
        elif cli_args['get']:
            return ConfigCommand.GET
        elif cli_args['remove']:
            return ConfigCommand.REMOVE
        else:
            raise Exception('unknown master command type')

    else:
        raise Exception('unknown module type')


def add_params(conf, cli_args):
    if cli_args['--verbose']:
        conf.set('core', 'verbose', 'true')
    elif cli_args['--quiet']:
        conf.set('core', 'quiet', 'true')

    if cli_args['master']:
        if cli_args['--hostname']:
            conf.set('master', 'hostname', cli_args['--hostname'])
        if cli_args['--port']:
            conf.set('master', 'port', cli_args['--port'])
        if cli_args['--attach']:
            conf.set('master', 'attach', 'true')

    elif cli_args['slave']:
        pass

    return conf
