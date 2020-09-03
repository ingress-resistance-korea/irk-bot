from typing import Type

from slack import WebClient

from src.bot_slack.constants import CMD_INTEL
from src.bot_slack.utils import slack_message_to_dict
from src.shared.constants import INTEL_RESPONSE_SLACK
from src.shared.parser import parse_intel_result
from src.shared.queue import BotQueue
from src.bot_slack.type import SlackMessage


def request_intel_screenshot(web_client: WebClient, queue: BotQueue, message: Type[SlackMessage]):
    location = message.text.split(CMD_INTEL)[1]
    queue.send_request_intel(
        event_id=message.client_msg_id,
        response_event_to=INTEL_RESPONSE_SLACK,
        location=location,
        data=slack_message_to_dict(message),
    )
    web_client.chat_postMessage(channel=message.channel, text='잠시만 기다려주세요')


def response_intel_screenshot(web_client: WebClient, response):
    channel = response['data']['channel']
    result = parse_intel_result(response['result'])
    if result.success:
        text = '%s\n`%s`\n%s' % (result.address, result.timestamp, result.url)
        web_client.chat_postMessage(channel=channel, text=text)
    else:
        web_client.chat_postMessage(channel=channel, text=result.error_message)
