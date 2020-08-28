import json

from src.worker.chromedriver import ChromeDriver
from src.shared.constants import INTEL_REQUEST, INTEL_RESPONSE
from src.worker.intel_crawler import Crawler
from src.shared.logger import getLogger
from src.shared.queue import Queue


class Worker:
    def __init__(self):
        self.logger = getLogger('worker')
        self.chromedriver = ChromeDriver(self.logger)
        self.queue = Queue()
        self.crawler = Crawler(self.chromedriver)

    def run(self):
        while True:
            request_str = self.queue._lpop(INTEL_REQUEST)
            if request_str:
                request = json.loads(request_str)
                location_name = request['location_name']
                success, text = self.crawler.get_intel_screenshot(location_name=location_name)
                request['success'] = success
                request['text'] = text
                intel_response = json.dumps(request)
                self.logger.info(intel_response)
                self.queue._rpush(INTEL_RESPONSE, intel_response)