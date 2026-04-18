import time
from cache.redis_client import redis_client

RATE_LIMIT=5
TIME_WINDOW=60

def is_rate_limited(user_id: str) -> bool:
    key = f"rate_limit:{user_id}"

    current = redis_client.get(key)
    if current is None:
        redis_client.set(key, 1, ex=TIME_WINDOW)
        return False

    if int(current) >= RATE_LIMIT:
        return True

    redis_client.incr(key)
    return False