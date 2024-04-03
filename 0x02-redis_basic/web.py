#!/usr/bin/env python3
"""Expiring web cache and tracker module"""
import requests
import redis
import time

# Initialize Redis connection
redis_client = redis.Redis()


def get_page(url: str) -> str:
    """Fetch the HTML content of a URL and
    cache the result with tracking.
    """
    # Track the number of times the URL is accessed
    count_key = f"count:{url}"
    redis_client.incr(count_key)

    # Check if the page content is cached
    cached_content = redis_client.get(url)
    if cached_content:
        # Return cached content if available
        return cached_content.decode('utf-8')

    # If not cached, fetch the HTML content using requests
    response = requests.get(url)
    html_content = response.text

    # Cache the HTML content with expiration time of 10 seconds
    redis_client.setex(url, 10, html_content)

    return html_content
