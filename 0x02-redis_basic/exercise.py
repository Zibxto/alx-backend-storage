#!/usr/bin/env python3
"""Cache module"""
import redis
import uuid
from typing import Union


class Cache:
    """Cache class"""
    def __init__(self):
        """ Class constructor"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ takes a data argument and returns a string"""
        id = str(uuid.uuid1())
        self._redis.mset({"{}".format(id): data})
        return id

    def get(self, key: str, fn=None):
        """
        Retrieve data from Redis and convert
        it back to the desired format.
        """
        result = self._redis.get(key)
        if result is None:
            return None  # Key does not exist, conserving Redis.get behavior
        if fn is not None:
            return fn(result)  # Convert data using the provided callable
        else:
            return result

    def get_str(self, key: str) -> Union[str, None]:
        """Retrieve data from Redis and convert it to a string."""
        return self.get(key, lambda data: data.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """Retrieve data from Redis and convert it to an integer."""
        return self.get(key, lambda data: int(data))
