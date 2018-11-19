import functools

from django.conf import settings

import redis


@functools.lru_cache(maxsize=128)
def redis_client():  # pragma: no cover
    """
    Redis client wrapped into LRU cache.

    Example:
    >>> redis_client().set('foo', 'bar')
    >>> redis_client().get('foo')
    """
    return redis.StrictRedis.from_url(settings.REDIS_URL)


def redis_key(prefix, *args, delimiter=':') -> str:
    """
    Helper to build nested key names in Redis.

    :param prefix: str, required param because namespace is important
    :param args: any values
    :param delimiter: str, default `:`
    :return: str

    Example:
    >>> key = redis_key('user', 42, 'comments')
    >>> print(key)
    >>> 'user:42:comments'
    """
    components = (prefix, ) + args
    return delimiter.join(map(str, components))
