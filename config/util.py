import configparser
import logging
from pathlib import Path
import os

logger = logging.getLogger('pcmd.config.util')


def get_userconf():
    location = get_userconf_path()
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


def get_userconf_path():
    if not os.environ.get('PCMDRC') and not os.environ.get('PCMDCONF'):
        home_dir = str(Path.home())
        conf_location = os.path.join(home_dir, ".pcmdconf")
    else:
        if os.environ.get('PCMDRC'):
            conf_location = os.environ.get('PCMDRC')
        else:
            conf_location = os.environ.get('PCMDCONF')

    return conf_location

