import configparser
import logging
from pathlib import Path
import os.path

logger = logging.getLogger('pcmd.config.util')


def get_userconf(cli_args):
    location = get_userconf_path(cli_args)
    return read_userconf(location)


def read_userconf(conf_location):
    if os.path.exists(conf_location):
        try:
            config = configparser.ConfigParser()
            config.read(conf_location)
        except configparser.Error as e:
            logger.error("error loading configuration file {} - {}".format(
                conf_location,
                e.message
            ))
            return None
    else:
        logger.debug("local configuration file {} not found".format(
            conf_location)
        )

        return None

    logger.debug("local configuration file {} loaded".format(
        conf_location)
    )
    return config


def get_userconf_path(cli_args):
    if '--conf' not in cli_args or cli_args['--conf'] is None:
        home_dir = str(Path.home())
        conf_location = os.path.join(home_dir, ".pcmdconf")
    else:
        conf_location = cli_args['--conf']

    return conf_location

