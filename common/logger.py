import logging


def get_logger(name, verbose):
    logger = logging.getLogger(name)
    formatter = logging.Formatter(
        "[%(filename)s:%(lineno)s %(funcName)s()] - %(levelname)s - %(message)s"
    )

    if verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    fh = logging.FileHandler('pcmd.log')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    logger.addHandler(sh)
