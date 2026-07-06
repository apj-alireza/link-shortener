import redis
from utils.configs import REDIS_HOST, REDIS_PORT


def connect_redis() -> redis.Redis:
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    return r
