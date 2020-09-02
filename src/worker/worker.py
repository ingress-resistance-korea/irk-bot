import json

from src.worker.chromedriver import ChromeDriver
from src.worker.intel_crawler import Crawler
from src.shared.logger import getLogger
from src.shared.queue import WorkerQueue


class Worker:
    def __init__(self):
        self.logger = getLogger('worker')
        self.chromedriver = ChromeDriver(self.logger)
        self.queue = WorkerQueue()
        self.crawler = Crawler(self.chromedriver)

    def run(self):
        while True:
            request = self.queue.receive_request_intel()
            if request:
                event_id = request['event_id']
                response_event_to = request['response_event_to']
                location = request['location']
                data = request['data']
                result = self.crawler.get_intel_screenshot(location=location)
                intel_response = json.dumps({
                    'request': request,
                    'result': result
                })
                self.logger.info(intel_response)
                self.queue.send_response_intel(event_id, response_event_to, result, data)
