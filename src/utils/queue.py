from redis import Redis

from src.config.settings import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD


class Queue:
    def __init__(self):
        self.UTF_8 = 'utf-8'
        self.redis = Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)

    def rpush(self, name, value):
        return self.redis.rpush(name, value)

    def lpop(self, name):
        value = self.redis.lpop(name)
        return value.decode(self.UTF_8) if value else value
