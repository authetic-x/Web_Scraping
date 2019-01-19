import time

import aiohttp
from crawler import Crawler
import requests
import aiohttp
import asyncio
from db import RedisClient
from settings import *

TEST_URL = 'http://www.baidu.com'

def test(proxy):
    try:
        if isinstance(proxy, bytes):
            proxy = proxy.decode('utf-8')
        proxies = {
            'http': 'http://' + proxy,
            'https': 'https://' + proxy,
        }
        response = requests.get(url=TEST_URL, proxies=proxies, timeout=5)
        if response.status_code == 200:
            print('代理可用', proxy)
    except (Exception) as e:
        print('Error', e.args)

async def test_aiohttp(proxy):
    async with aiohttp.ClientSession() as session:
        try:
            if isinstance(proxy, bytes):
                proxy = proxy.decode('utf-8')
            real_proxy = 'http://' + proxy
            async with session.get(url=TEST_URL, proxy=real_proxy, timeout=5) as response:
                if response.status == 200:
                    print('代理有效', proxy)
                else:
                    print('代理无效', proxy, '状态码', response.status)
        except Exception as e:
            print('Error', e.args)

class My_Tester():
    def __init__(self):
        self.redis = RedisClient()

    async def test_single_proxy(self, proxy):
        async with aiohttp.ClientSession() as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://' + proxy
                async with session.get(url=TEST_URL, proxy=real_proxy, timeout=5) as response:
                    if response.status == 200:
                        print('代理有效', proxy)
                        print('当前代理数', self.redis.count())
                        self.redis.max(proxy)
                    else:
                        print('代理无效', proxy, '状态码', response.status)
                        #self.redis.decrease(proxy)
            except Exception as e:
                print('Error', e.args)
                #self.redis.decrease(proxy)

    def run(self):
        print('测试器开始运行')
        proxies = []
        crawler = Crawler()
        for proxy in crawler.crawl_ip3366():
            proxies.append(proxy)
        for proxy in crawler.crawl_xicidaili():
            proxies.append(proxy)
        loop = asyncio.get_event_loop()
        try:
            for i in range(0, len(proxies), 10):
                tasks = [self.test_single_proxy(proxy) for proxy in proxies[i:i + 10]]
                loop.run_until_complete(asyncio.wait(tasks))
                time.sleep(2)
            loop.close()
        except Exception as e:
            print('测试错误', e.args)


def main():
    my_tester = My_Tester()
    my_tester.run()

if __name__ == '__main__':
    main()