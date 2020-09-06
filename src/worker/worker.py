import json

from src.shared.constants import IntelRequestType
from src.worker.chromedriver import ChromeDriver
from src.worker.intel_crawler import Crawler
from src.shared.logger import getLogger
from src.shared.queue import WorkerQueue
from src.worker.parser import intel_result_to_dict


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
                request_type = request['request_type']
                data = request['data']
                if request_type == IntelRequestType.POSITION.value:
                    latitude, longitude = request['position']['latitude'], request['position']['longitude']
                    result = self.crawler.get_intel_screenshot_by_position(latitude=latitude, longitude=longitude)
                elif request_type == IntelRequestType.LOCATION.value:
                    location = request['location']
                    result = self.crawler.get_intel_screenshot(location=location)
                else:
                    raise ValueError
                intel_response = json.dumps({
                    'request': request,
                    'result': intel_result_to_dict(result),
                })
                self.logger.info(intel_response)
                self.queue.send_response_intel(event_id, response_event_to, result, data)
