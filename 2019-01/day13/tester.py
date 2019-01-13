from db import RedisClient
from settings import REDIS_KEY, MIN_SCORE, MAX_SCORE

redis = RedisClient()
proxies = redis.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)
if not proxies:
    print(None)
else:
    print(proxies)