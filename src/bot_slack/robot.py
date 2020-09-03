import asyncio
from concurrent import futures
from time import sleep

from slack import RTMClient, WebClient

from src.bot_slack.apps.intel import request_intel_screenshot, response_intel_screenshot
from src.bot_slack.constants import CMD_INTEL, CMD_PREFIX
from src.bot_slack.utils import parse_slack_message
from src.configs.settings import SLACK_TOKEN
from src.shared.constants import INTEL_RESPONSE_SLACK
from src.shared.logger import getLogger

from src.shared.queue import BotQueue


class Robot(object):
    def __init__(self):
        self.logger = getLogger('bot_slack')
        self.web_client: WebClient = WebClient(token=SLACK_TOKEN)
        self.queue = BotQueue()

    async def run(self):
        loop = asyncio.get_event_loop()
        rtm_client: RTMClient = RTMClient(token=SLACK_TOKEN, run_async=True, loop=loop)
        rtm_client.run_on(event='message')(self._rtm_event_handler)
        executor = futures.ThreadPoolExecutor(max_workers=1)
        await asyncio.gather(
            loop.run_in_executor(executor, self.sync_loop),
            rtm_client.start()
        )

    def sync_loop(self):
        while True:
            self.receive_events()
            sleep(0.3)

    def receive_events(self):
        response = self.queue.receive_response_intel(INTEL_RESPONSE_SLACK)
        if response:
            response_intel_screenshot(self.web_client, response)

    async def _rtm_event_handler(self, data, **payload):
        if data['text'].startswith(CMD_PREFIX):
            message = parse_slack_message(data)
            if message.text.startswith(CMD_INTEL):
                request_intel_screenshot(self.web_client, self.queue, message)
