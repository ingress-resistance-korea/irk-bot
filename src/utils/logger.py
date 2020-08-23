import sys
import logging
from src.config.settings import ENV, LOG_DIR

PRODUCTION = 'production'


def getLogger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    if ENV == PRODUCTION:
        handler = logging.FileHandler('%s/worker.log' % LOG_DIR)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
    else:
        handler = logging.StreamHandler(sys.stdout)

    if not logger.handlers:
        logger.addHandler(handler)
    return logger

