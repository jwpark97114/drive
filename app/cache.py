import json
from typing import Optional, Any
import redis

from . import config


_redis = None


def _get_client():
    global _redis
    if _redis is None:
        _redis = redis.from_url(config.REDIS_URL, decode_responses=True)
    return _redis


def cache_set_json(key: str, value: Any, ttl=90):
    _get_client().setex(key, ttl, json.dumps(value, default=str))


def cache_get_json(key: str):
    result = _get_client().get(key)
    return None if result is None else json.loads(result)


def cache_delete(key: str):
    _get_client().delete(key)
