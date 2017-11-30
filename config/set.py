"""pcmd-config-set

Usage:
    pcmd config set    [--version] [--help]
                       <section>.<key> <value> [-v|-q]

Options:
    -v, --verbose   More detailed logs
    -q, --quiet     Don't write to terminal
    --help          Show this screen
    --version       Show version

"""


def main(conf):
    section, key = conf.args['<section>.<key>'].split('.')
    value = conf.args['<value>']

    import config.configuration
    try:
        conf.set(section, key, value)
    except config.configuration.UserConfigNotFound:
        conf.logger.error("user config file not found")
        return 1

    return 0
