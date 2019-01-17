from settings import POOL_UPPER_THRESHOLD
from db import RedisClient
from crawler import Crawler
from settings import *


class Getter():
    def __init__(self):
        self.redis = RedisClient()
        self.crawler = Crawler()

    def is_over_threshold(self):
        if self.redis.count() >= POOL_UPPER_THRESHOLD:
            return True
        return False

    def run(self):
        print('获取器开始执行')
        if not self.is_over_threshold():
            for proxy in self.crawler.get_proxies():
                self.redis.add(proxy)

if __name__ == '__main__':
    getter = Getter()
    getter.run()
    for proxy in getter.redis.all():
        getter.redis.decrease(proxy)
        print(proxy, getter.redis.db.zscore(REDIS_KEY, proxy))