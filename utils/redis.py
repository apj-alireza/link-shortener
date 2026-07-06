import redis


def connect_redis() -> redis.Redis:
    r = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)
    return r
