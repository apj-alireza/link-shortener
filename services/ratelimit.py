import time
from redis import Redis


class SlidingWindow:
    def __init__(self, window_size: int, max_request: int, redis: Redis):
        self.window_size = window_size
        self.max_request = max_request
        self.redis = redis

    def allow_request(self, slug: str) -> bool:

        key = f"rate_limite.{slug}"
        now = time.time()
        window_start = now - self.window_size

        while True:
            oldest_request = self.redis.lindex(key, 0)
            if oldest_request is None:
                break
            if float(oldest_request) > window_start:
                break
            self.redis.lpop(key)

        if self.redis.llen(key) < self.max_request:
            self.redis.rpush(key, now)
            self.redis.expire(key, self.window_size)
            return True

        return False
