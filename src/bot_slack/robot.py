from time import sleep

from slack import RTMClient, WebClient

from src.bot_slack.constants import CMD_INTEL
from src.bot_slack.utils import parse_message
from src.configs.settings import SLACK_TOKEN
from src.shared.constants import INTEL_RESPONSE_SLACK
from src.shared.logger import getLogger

from src.shared.queue import BotQueue


@RTMClient.run_on(event='message')
def wow(data, **payload):
    message = parse_message(data)
    if message.text.startswith(CMD_INTEL):
        # find app
        pass


class Robot(object):
    def __init__(self):
        self.logger = getLogger('bot_slack')
        self.rtm_client: RTMClient = RTMClient(token=SLACK_TOKEN)
        self.web_client: WebClient = WebClient(token=SLACK_TOKEN)
        self.queue = BotQueue()

    def run(self):
        self.rtm_client.start()
        while True:
            self.receive_events()
            sleep(0.3)

    def receive_events(self):
        response = self.queue.receive_response_intel(INTEL_RESPONSE_SLACK)
        if response:
            self.send_intel_response(response)
        pass

    def send_intel_response(self, response):
        pass
