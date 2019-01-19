import time

from db import RedisClient
from settings import VALID_STATUS_CODE, TEST_URL, BATCH_TEST_SIZE
from crawler import Crawler
import aiohttp
import asyncio
try:
    from aiohttp import ClientError
except:
    from aiohttp import ClientProxyConnectionError as ProxyConnectionError
from asyncio import TimeoutError

class Tester():
    def __init__(self):
        self.redis = RedisClient()

    async def test_single_proxy(self, proxy):
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://' + proxy
                print('正在测试', proxy)
                async with session.get(url=TEST_URL, proxy=real_proxy,
                                       timeout=5) as response:
                    if response.status in VALID_STATUS_CODE:
                        self.redis.max(proxy)
                        print('代理可用', proxy)
                    else:
                        self.redis.decrease(proxy)
                        print('请求响应码不合法', proxy)
            except (ClientError, TimeoutError, AttributeError) as e:
                print(e.args)
                self.redis.decrease(proxy)
                print('代理请求失败', proxy)

    def run(self):
        print('测试器开始运行')
        try:
            count = self.redis.count()
            print('当前代理剩余个数', count)
            loop = asyncio.get_event_loop()
            for i in range(0, count, BATCH_TEST_SIZE):
                start = i
                stop = min(count, i+BATCH_TEST_SIZE)
                test_proxies = self.redis.batch(start, stop)
                print('正在测试', start+1, '-', stop, '个代理')
                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                time.sleep(2)
        except Exception as e:
            print('测试器发生错误', e.args)

if __name__ == '__main__':
    tester = Tester()
    tester.run()