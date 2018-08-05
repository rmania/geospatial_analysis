import logging


def logger():
    """
    Setup basic logging for console.
    """
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S')
    logger = logging.getLogger(__name__)
    return logger