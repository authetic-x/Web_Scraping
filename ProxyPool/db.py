import redis
from random import choice

from ProxyPool.settings import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, INITIAL_SCORE, \
                                REDIS_KEY, MAX_SCORE, MIN_SCORE
from ProxyPool.error import PoolEmptyError

class RedisClient(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        '''
        Initialize
        :param host: redis host
        :param port: redis port
        :param password: redis password
        '''
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)

    def add(self, proxy, score=INITIAL_SCORE):
        '''
        Add a proxy
        :param proxy:
        :param score:
        :return: result
        '''
        if not self.db.zscore(REDIS_KEY, proxy):
            return self.db.zadd(REDIS_KEY, score, proxy)

    def random(self):
        '''
        Get a random proxy from the ProxyPool
        :return: proxy
        '''
        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            result = self.db.zrevrange(REDIS_KEY, 0, 100)
            if len(result):
                return choice(result)
            else:
                raise PoolEmptyError

    def decrease(self, proxy):
        '''
        Find a invalid proxy, erase or -1
        :param proxy: proxy
        :return: result
        '''
        score = self.db.zscore(REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            print('代理', proxy, '当前分数', score, '减1')
            return self.db.zincrby(REDIS_KEY, proxy, -1)
        else:
            print('代理', proxy, '当前分数', score, '移除')
            return self.db.zrem(REDIS_KEY, proxy)

    def exist(self, proxy):
        return not self.db.zscore(REDIS_KEY, proxy) == None

    def max(self, proxy):
        print('代理', proxy, '可用, 设置为', MAX_SCORE)
        return self.db.zadd(REDIS_KEY, MAX_SCORE, proxy)

    def count(self):
        return self.db.zcard(REDIS_KEY)

    def all(self):
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)
