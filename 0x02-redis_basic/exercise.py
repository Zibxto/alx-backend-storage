#!/usr/bin/env python3
"""Cache module"""
import redis
import uuid
from typing import Union
import functools


def call_history(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = f"{method.__qualname__}:inputs"  # Input list key
        output_key = f"{method.__qualname__}:outputs"  # Output list key

        # Append input arguments to the input list in Redis
        self._redis.rpush(input_key, str(args))

        # Execute the wrapped function to retrieve the output
        output = method(self, *args, **kwargs)

        # Append the output to the output list in Redis
        self._redis.rpush(output_key, output)

        return output  # Return the output obtained from the wrapped function

    return wrapper


def count_calls(method):
    """ counts how many times methods of the Cache class are called"""
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        # Get the qualified name of the method
        key = method.__qualname__
        # Generate the key for \storing the call count
        count_key = "{}_calls".format(key)
        self._redis.incr(count_key)  # Increment the call count
        # Call the original method and return its result
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    """Cache class"""
    def __init__(self):
        """ Class constructor"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
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
