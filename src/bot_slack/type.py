from dataclasses import dataclass


@dataclass
class SlackMessage:
    client_msg_id: str
    suppress_notification: bool
    text: str
    user: str
    team: str
    blocks: []
    source_team: str
    user_team: str
    channel: str
    event_ts: str
    ts: str
