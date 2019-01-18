import aiohttp
from crawler import Crawler
import requests

url = 'http://www.baidu.com'

def test(proxy):
    try:
        if isinstance(proxy, bytes):
            proxy = proxy.decode('utf-8')
        proxies = {
            'http': 'http://' + proxy,
            'https': 'https://' + proxy,
        }
        response = requests.get(url=url, proxies=proxies, timeout=5)
        if response.status_code == 200:
            print('代理可用', proxy)
    except (Exception) as e:
        print('Error', e.args)

def main():
    crawler = Crawler()
    proxies = crawler.crawl_data5u()
    for proxy in proxies:
        test(proxy)

if __name__ == '__main__':
    main()