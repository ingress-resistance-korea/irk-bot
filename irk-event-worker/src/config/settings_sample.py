import os

# Server
ENV = os.environ['ENV']
SERVER_URL = 'http://127.0.0.1:5784'
LOG_DIR = os.path.dirname(os.path.realpath(__file__)) + '/../../logs'
SCREENSHOT_DIR = os.path.dirname(os.path.realpath(__file__)) + '/../../screenshots'
CHROMEDRIVER_PATH = os.path.dirname(os.path.realpath(__file__)) + '/' + '../../binaries/chromedriver'

# Ingress
GOOGLE_EMAIL = 'XXXXXXX'
GOOGLE_PASSWORD = 'XXXXXXX'
INGRESS_AGENT_NAME = 'XXXXXXX'
GOOGLE_MAP_KEY = 'XXXXXXX'
MAX_LOAD_TIME = 300

# Redis
REDIS_HOST = 'locahost'
REDIS_PORT = 6379
REDIS_PASSWORD = 'password'

# Giphy
GIPHY_KEY = 'XXXXXXX'
