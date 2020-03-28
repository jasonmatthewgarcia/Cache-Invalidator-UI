from . import redis_client


class Cache:

    def __init__(self):
        pass

    def get(self)

    def delete(self, key):
        return redis_client.delete(key)