import os

# Server
ENV = os.environ['ENV']
SERVER_URL = 'http://127.0.0.1:5784'
BASE_DIR = os.path.dirname(os.path.realpath(__file__)) + '/../../../'
LOG_DIR = BASE_DIR + '/data/logs'
SCREENSHOT_DIR = BASE_DIR + '/data/screenshots'
CHROMEDRIVER_PATH = BASE_DIR + '/irk-event-worker/binaries/chromedriver'

# Ingress
GOOGLE_EMAIL = 'XXXXXXX'
GOOGLE_PASSWORD = 'XXXXXXX'
INGRESS_AGENT_NAME = 'XXXXXXX'
GOOGLE_MAP_KEY = 'XXXXXXX'
MAX_LOAD_TIME = 300

# Redis
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = 'password'

# Giphy
GIPHY_KEY = 'XXXXXXX'
