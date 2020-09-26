from typing import Type

from slack import WebClient

from src.bot_slack.constants import CMD_INTEL, INTEL_HELP_MESSAGE_SLACK
from src.bot_slack.utils import slack_message_to_dict
from src.shared.constants import INTEL_RESPONSE_SLACK
from src.shared.parser import parse_intel_result
from src.shared.queue import BotQueue
from src.bot_slack.type import SlackMessage


def request_intel_screenshot(web_client: WebClient, queue: BotQueue, message: Type[SlackMessage]):
    if message.text == CMD_INTEL:
        web_client.chat_postMessage(channel=message.channel, text=INTEL_HELP_MESSAGE_SLACK)
        return
    location = message.text.split(CMD_INTEL + ' ')[1]
    queue.send_request_intel(
        event_id=message.client_msg_id,
        response_event_to=INTEL_RESPONSE_SLACK,
        location=location,
        extra=slack_message_to_dict(message),
    )
    web_client.chat_postMessage(channel=message.channel, text='잠시만 기다려주세요')


def response_intel_screenshot(web_client: WebClient, response):
    channel = response['extra']['slack_channel']
    result = parse_intel_result(response['result'])
    if result.success:
        text = '%s\n`%s`\n%s' % (result.address, result.timestamp, result.intel_url)
        web_client.files_upload(channels=channel, file=result.file_path, initial_comment=text)
        # web_client.chat_postMessage(channel=channel, text=text)
    else:
        web_client.chat_postMessage(channel=channel, text=result.error_message)
