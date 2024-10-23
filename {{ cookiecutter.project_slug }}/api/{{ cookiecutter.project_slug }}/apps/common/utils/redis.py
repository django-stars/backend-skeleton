import functools

import redis

from redis import Redis

from django.conf import settings


@functools.lru_cache(maxsize=128)
def redis_client(redis_connection_url: str = settings.REDIS_URL) -> Redis:
    """
    Redis client wrapped into LRU cache.
    Example:
    >>> redis_client().set('foo', 'bar')
    >>> redis_client().get('foo')
    """
    return redis.StrictRedis.from_url(redis_connection_url)
