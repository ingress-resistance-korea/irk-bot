import sys
import logging
from src.configs.settings import ENV, LOG_DIR

PRODUCTION = 'production'


def getLogger(name):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    if ENV == PRODUCTION:
        try:
            handler = logging.FileHandler('%s/%s.log' % (LOG_DIR, name))
        except FileNotFoundError:
            f = open('%s/%s.log' % (LOG_DIR, name), 'w')
            f.close()
            handler = logging.FileHandler('%s/%s.log' % (LOG_DIR, name))
        except Exception as e:
            raise e
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
    else:
        handler = logging.StreamHandler(sys.stdout)

    if not logger.handlers:
        logger.addHandler(handler)
    return logger

