import json
import sys
import logging
from datetime import datetime

from src.configs.settings import ENV, LOG_DIR, LOGSTASH_URL, ELASTICSEARCH_INDEX_REQUEST, ELASTICSEARCH_INDEX_RESPONSE, \
    ELASTICSEARCH_INDEX_CHAT
import requests

from src.shared.utils.datetime import get_timestamp

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


class LogstashLogger:
    headers = {
        'Content-Type': 'application/json'
    }

    def __init__(self, application_type):
        self.application_type = application_type

    def irk_request(self, json_data):
        data = {'index': ELASTICSEARCH_INDEX_REQUEST, 'data': json_data, 'application_type': self.application_type, 'timestamp': get_timestamp()}
        requests.post(LOGSTASH_URL, data=json.dumps(data), headers=self.headers)

    def irk_response(self, json_data):
        data = {'index': ELASTICSEARCH_INDEX_RESPONSE, 'data': json_data, 'application_type': self.application_type, 'timestamp': get_timestamp()}
        requests.post(LOGSTASH_URL, data=json.dumps(data), headers=self.headers)

    def irk_chat(self, json_data):
        data = {'index': ELASTICSEARCH_INDEX_CHAT, 'data': json_data, 'application_type': self.application_type, 'timestamp': get_timestamp()}
        requests.post(LOGSTASH_URL, data=json.dumps(data), headers=self.headers)
