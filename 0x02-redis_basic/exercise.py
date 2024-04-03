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
