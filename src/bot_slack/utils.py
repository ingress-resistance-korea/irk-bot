from typing import Type
from src.bot_slack.types import SlackMessage


def parse_message(data) -> Type[SlackMessage]:
    message = SlackMessage

    message.channel = data['channel']
    message.text = data['text']
    message.user = data['user']
    message.client_msg_id = data['client_msg_id']
    message.event_ts = data['event_ts']
    message.source_team = data['source_team']
    message.suppress_notification = data['suppress_notification']
    message.team = data['team']
    message.ts = data['ts']
    message.user_team = data['user_team']
    return message
