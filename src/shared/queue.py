from typing import Type

from redis import Redis
import json

from telegram import Chat, Message, User

from src.configs.settings import REDIS_HOST, REDIS_PORT
from src.shared.constants import INTEL_REQUEST
from src.shared.types import IntelResult


class Queue:
    def __init__(self):
        self.UTF_8 = 'utf-8'
        self.redis = Redis(host=REDIS_HOST, port=REDIS_PORT)

    def _rpush(self, name, data):
        return self.redis.rpush(name, data)

    def _lpop(self, name):
        value = self.redis.lpop(name)
        return value.decode(self.UTF_8) if value else value


class BotQueue(Queue):
    def send_request_intel(self, event_id, response_event_to, location, chat, message, user):
        data = {
            'event_id': event_id,
            'response_event_to': response_event_to,
            'location': location,
            'chat': chat,
            'message': message,
            'user': user,
        }
        return self._rpush(INTEL_REQUEST, json.dumps(data))

    def receive_response_intel(self, response_event_to):
        data = self._lpop(response_event_to)
        return json.loads(data) if data else data


class WorkerQueue(Queue):
    def receive_request_intel(self):
        data = self._lpop(INTEL_REQUEST)
        return json.loads(data) if data else data

    def send_response_intel(self, event_id: str, response_event_to: str, result: Type[IntelResult], chat: Chat,
                            message: Message, user: User):
        data = {
            'event_id': event_id,
            'result': {
                'success': result.success,
                'url': result.url,
                'address': result.address,
                'error_message': result.error_message,
                'timestamp': str(result.timestamp),
            },
            'chat': chat,
            'message': message,
            'user': user,
        }
        return self._rpush(response_event_to, json.dumps(data))
