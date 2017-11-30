"""
[core]
    verbose = false
    quiet = false

[master]
    hostname = 0.0.0.0
    port = 1337
    local_hostname = 127.0.0.1
    local_port = random
    attach = false

[slave]
    hostname = 0.0.0.0
    port = 1338
    local_hostname = 127.0.0.1
    local_port = random
    attach = false
"""

import docopt
import logging
import configparser

import config.util
import common

from common.const import ModuleType

from master.main import CommandType as MasterCommand
from config.main import CommandType as ConfigCommand


class Configuration:
    def __init__(self, cli_args, module_=None, command=None):
        self.logger = logging.getLogger('pcmd.config.Configuration')

        if module_ is None:
            self.module = get_module(cli_args)
        else:
            self.module = module_

        if command is None:
            self.command = get_command(self.module, cli_args)
        else:
            self.command = command

        self.args = get_cli(self.module, self.command, cli_args)
        self.user_conf = config.util.get_userconf()
        self.conf = self.read_all(self.args)

    def get(self, key, section=None):
        if section is None:
            section = self.module.name.lower()
        return self.conf.get(section, key)

    def set(self, section, key, value):
        if self.user_conf:
            try:
                self.user_conf.set(section, key, value)
            except configparser.NoSectionError:
                self.user_conf.add_section(section)
            finally:
                self.user_conf.set(section, key, value)

            with open(config.util.get_userconf_path(), 'w') as conf:
                self.user_conf.write(conf)
        else:
            raise UserConfigNotFound

    def remove(self, section, key):
        if self.user_conf:
            try:
                out_remove = self.user_conf.remove_option(section, key)
            except configparser.NoSectionError as e:
                raise e

            if out_remove:
                with open(config.util.get_userconf_path(), 'w') as f:
                    self.user_conf.write(f)
                return out_remove
            else:
                raise ValueNotFound
        else:
            raise UserConfigNotFound

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
        conf = self.add_userconf(conf)
        conf = self.add_params(conf, cli_args)
        return conf

    def read_default(self):
        conf = configparser.ConfigParser()
        conf.read_string(__doc__)
        self.logger.debug("default configuration loaded")
        return conf

    def add_userconf(self, default_conf):
        user_conf = config.util.get_userconf()

        if user_conf:
            default_conf.read_dict(user_conf)
            self.logger.debug("user configuration merged with defaults")

        return default_conf

    def add_params(self, conf, cli_args):
        if cli_args['--verbose']:
            conf.set('core', 'verbose', 'true')
        elif cli_args['--quiet']:
            conf.set('core', 'quiet', 'true')

        if self.module is ModuleType.MASTER:
            if self.command is MasterCommand.START:
                if cli_args['--attach']:
                    conf.set('master', 'attach', 'true')

                if cli_args['--hostname']:
                    conf.set('master', 'hostname', cli_args['--hostname'])
                if cli_args['--port']:
                    conf.set('master', 'port', cli_args['--port'])

                if cli_args['--lhostname']:
                    conf.set(
                        'master',
                        'local_hostname',
                        cli_args['--lhostname']
                    )
                if cli_args['--lport']:
                    conf.set(
                        'master',
                        'local_port',
                        cli_args['--lport']
                    )

            elif self.command is MasterCommand.STOP:
                if cli_args['--hostname']:
                    conf.set('master', 'local_hostname', cli_args['--hostname'])
                if cli_args['--port']:
                    conf.set('master', 'local_port', cli_args['--port'])

            elif self.command is MasterCommand.STATUS:
                pass

        elif self.module is ModuleType.CONFIG:
            if self.command is ConfigCommand.GET:
                pass

            elif self.command is ConfigCommand.SET:
                pass

            elif self.command is ConfigCommand.REMOVE:
                pass

        return conf


def get_command_cli(module_type, command_type, module_cli):
    if module_type is ModuleType.MASTER:
        if command_type is MasterCommand.START:
            import master.start
            func = master.start
        elif command_type is MasterCommand.STOP:
            import master.stop
            func = master.stop
        elif command_type is MasterCommand.STATUS:
            import master.status
            func = master.status
        else:
            raise Exception(
                'command {} not implemented'.format(command_type.name)
            )

    elif module_type is ModuleType.SLAVE:
        raise Exception('Not Implemented')

    elif module_type is ModuleType.CONFIG:
        if command_type is ConfigCommand.SET:
            import config.set
            func = config.set
        elif command_type is ConfigCommand.GET:
            import config.get
            func = config.get
        elif command_type is ConfigCommand.REMOVE:
            import config.remove
            func = config.remove
        else:
            raise Exception(
                'command {} not implemented'.format(command_type.name)
            )

    else:
        raise Exception('module {} not implemented'.format(module_type.name))

    argv = [module_type.name.lower()] + \
           [command_type.name.lower()] + module_cli['<args>']

    return docopt.docopt(
        func.__doc__,
        version=common.const.version,
        argv=argv,
    )


def get_module(cli_args):
    try:
        module_ = ModuleType[cli_args['<module>'].upper()]
    except KeyError:
        raise ModuleNotFound(
            "cannot find module {}".format(cli_args['<module>'])
        )

    return module_


def get_command(module_type, cli_args):
    module_cli = get_module_cli(module_type, cli_args)
    if module_type is ModuleType.MASTER:
        try:
            command = MasterCommand[module_cli['<command>'].upper()]
        except KeyError:
            import master.main
            return docopt.docopt(
                master.main.__doc__,
                argv='--help'
            )

    elif module_type is ModuleType.SLAVE:
        raise Exception('Not Implemented')

    elif module_type is ModuleType.CONFIG:
        try:
            command = ConfigCommand[module_cli['<command>'].upper()]
        except KeyError:
            import config.main
            return docopt.docopt(
                config.main.__doc__,
                argv='--help'
            )

    else:
        raise Exception('module {} not implemented'.format(module_type.name))

    return command


def get_module_cli(module_type, root_cli):
    if module_type is ModuleType.MASTER:
        import master.main
        func = master.main
    elif module_type is ModuleType.SLAVE:
        import slave.main
        func = slave.main
    elif module_type is ModuleType.CONFIG:
        import config.main
        func = config.main
    else:
        raise Exception('Not Implemented')

    argv = [module_type.name.lower()] + root_cli['<args>']

    return docopt.docopt(
        func.__doc__,
        version=common.const.version,
        argv=argv,
        options_first=True
    )


def get_cli(module_type, command_type, cli_args):
    module_cli = get_module_cli(module_type, cli_args)
    command_cli = get_command_cli(module_type, command_type, module_cli)

    return command_cli


class ModuleNotFound(Exception):
    pass


class UserConfigNotFound(Exception):
    pass


class ValueNotFound(Exception):
    pass
