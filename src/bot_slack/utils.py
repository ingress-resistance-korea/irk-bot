from typing import Type

from src.bot_slack.type import SlackMessage


def parse_slack_message(data: dict) -> Type[SlackMessage]:
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


def slack_message_to_dict(message: Type[SlackMessage]) -> dict:
    return {
        'slack_channel': message.channel,
        'slack_text': message.text,
        'slack_user': message.user,
        'slack_client_msg_id': message.client_msg_id,
        'slack_event_ts': message.event_ts,
        'slack_source_team': message.source_team,
        'slack_suppress_notification': message.suppress_notification,
        'slack_team': message.team,
        'slack_ts': message.ts,
        'slack_user_team': message.user_team,
    }