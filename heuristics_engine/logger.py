import logging
import sys

FORMATTER = logging.Formatter('[%(name)s] %(asctime)s %(levelname)-8s'
                              + ' %(filename)s:%(lineno)d: %(message)s', 
                              '%H:%M:%S')


def get_logger(name):
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    logger.addHandler(console_handler)
    # with this pattern, it's rarely necessary to propagate an error up to parent
    logger.propagate = False
    return logger
