"""pcmd-config-get

Usage:
    pcmd config get    [--version] [--help]
                       <section>.<key> [-v|-q]

Options:
    -v, --verbose   More detailed logs
    -q, --quiet     Don't write to terminal
    --help          Show this screen
    --version       Show version

"""

import configparser


def main(conf):
    section, key = conf.args['<section>.<key>'].split('.')
    try:
        out = conf.get(key, section)
    except configparser.NoOptionError:
        conf.logger.error("option {} doesn't exists".format(key))
        return 1
    except configparser.NoSectionError:
        conf.logger.error("section {} doesn't exists".format(section))
        return 1

    conf.logger.info(out)

    return 0
