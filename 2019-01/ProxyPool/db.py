import re

import redis
from settings import REDIS_HOST, REDIS_PASSWORD, REDIS_PORT, REDIS_KEY, \
                        INITIAL_SCORE, MAX_SCORE, MIN_SCORE
from random import choice
from error import PoolEmptyError

class RedisClient():
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, db=REDIS_PASSWORD):
        self.db = redis.StrictRedis(host=host, port=port, password=REDIS_PASSWORD,
                                     decode_responses=True)

    def add(self, proxy, score=INITIAL_SCORE):
        if not re.match('\d+\.\d+\.\d+\.\d+\:\d+', proxy):
            print('代理不符合规范', proxy)
            return
        if not self.db.zscore(REDIS_KEY, proxy):
            self.db.zadd(REDIS_KEY, {proxy:score})

    def random(self):
        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            result = self.db.zrevrange(REDIS_KEY, 0, 100)
            if len(result):
                return result[0]
            else:
                raise PoolEmptyError

    def max(self, proxy):
        self.db.zadd(REDIS_KEY, MAX_SCORE, proxy)

    def decrease(self, proxy):
        score = self.db.zscore(REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            print('代理', proxy, '当前分数', score, '减1')
            self.db.zincrby(REDIS_KEY, -1, proxy)
        else:
            print('代理', proxy, '当前分数', score, '移除')
            self.db.zrem(REDIS_KEY, proxy)

    def exist(self, proxy):
        return not self.db.zscore(REDIS_KEY, proxy) == None

    def count(self):
        return self.db.zcard(REDIS_KEY)

    def all(self):
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)