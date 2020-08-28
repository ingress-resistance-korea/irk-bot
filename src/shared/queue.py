from redis import Redis
import json
from src.configs.settings import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD
from src.shared.constants import INTEL_REQUEST


class Queue:
    def __init__(self):
        self.UTF_8 = 'utf-8'
        self.redis = Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)

    def _rpush(self, name, data):
        return self.redis.rpush(name, data)

    def _lpop(self, name):
        value = self.redis.lpop(name)
        return value.decode(self.UTF_8) if value else value

    def request_intel(self, event_id, client_type, location_name, chat_data):
        data = {
            'client_type': client_type,
            'location_name': location_name,
            'event_id': event_id,
            'chat_data': chat_data,
        }
        return self._rpush(INTEL_REQUEST, json.dumps(data))
