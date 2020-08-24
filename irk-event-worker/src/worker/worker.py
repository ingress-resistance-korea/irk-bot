import json

from src.worker.chromedriver import ChromeDriver
from src.worker.constants import INTEL_REQUEST, INTEL_RESPONSE
from src.worker.intel_crawler import get_intel_screenshot
from src.utils.logger import getLogger
from src.utils.queue import Queue


class Worker:
    def __init__(self):
        self.logger = getLogger()
        self.chromedriver = ChromeDriver(self.logger)
        self.queue = Queue()

    def run(self):
        self.queue.rpush(INTEL_REQUEST, json.dumps({"user": "SinerDJ", "value": "올림픽공원"}))  # sample test
        while True:
            request_str = self.queue.lpop(INTEL_REQUEST)
            if request_str:
                request = json.loads(request_str)
                search_key = request['value']
                is_success, text = get_intel_screenshot(self.chromedriver, search_key=search_key)
                request['is_success'] = is_success
                request['text'] = text
                self.queue.rpush(INTEL_RESPONSE, json.dumps(request))
