"""pcmd-config-remove

Usage:
    pcmd config remove  [--version] [--help]
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

    import config.configuration
    try:
        return conf.remove(section, key)
    except (configparser.NoSectionError, config.configuration.ValueNotFound):
        conf.logger.error("cannot find section-value pair")
        return 1
    except config.configuration.UserConfigNotFound:
        conf.logger.error("user config file not found")
        return 1
