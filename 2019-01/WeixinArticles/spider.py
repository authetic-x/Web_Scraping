from urllib.parse import urlencode

from requests import Session
from db_redis import RedisQueue
from request import WeixinRequest
from config import *
import requests
from requests.exceptions import ConnectionError, ReadTimeout
from pyquery import PyQuery as pq


class Spider():
    base_url = 'https://weixin.sogou.com/weixin'
    keyword = 'NBA'
    headers = {
        'Cookie': 'SUV = 00B317881B17ED1B5B6908F93A1EF865;CXID = CFB60C2B607DA865459A24D17B3BA704;SUID = 344EB76F3865860A5B724D730004C0D3;ABTEST = 0 | 1547686493 | v1;weixinIndexVisited = 1;ppinf = 5 | 1548046655 | 1549256255 | dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZTo4OmF1dGhldGljfGNydDoxMDoxNTQ4MDQ2NjU1fHJlZm5pY2s6ODphdXRoZXRpY3x1c2VyaWQ6NDQ6bzl0Mmx1TUNxYTBlU3lGcnExbE92aHQ3WG1Gd0B3ZWl4aW4uc29odS5jb218;pprdig = nfjiTQ62SluMVzhnMfzfgAECp - 10K12U8UYHC2eqYnJVPFubSIi041j - db4Tgv9yqfBiud8xlrNycXt7MXCYlucNOBpWcu1gu3Dn0Q8Lh7PPEBSYMvNTKTqTGx3x - l45Ndurz5 - 5Aq16RW8U - jenH5XD8vbJVnyHQP4ank0IJiA;sgid = 11 - 38791065 - AVxFUTibcPxuhorUqhoFwgzQ;SNUID = 925AC9C5DEDB5D85D39AAC46DE277CC1;IPLOC = CN4211;ppmdig = 15484905700000007acac90ac9b6a5f99ecab3769c06d166;JSESSIONID = aaaRpyLsVNeWx8b3_W5Hw;sct = 4',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        'Host': 'weixin.sogou.com'
    }
    session = Session()
    queue = RedisQueue()

    def start(self):
        self.session.headers.update(self.headers)
        start_url = self.base_url + '?' + urlencode({'query':self.keyword, 'type':2})
        first_request = WeixinRequest(url=start_url, callback=self.parse_index, need_proxy=True)
        self.queue.add(first_request)

    def get_proxy(self):
        try:
            response = requests.get(PROXY_POOL_URL)
            if response.status_code == 200:
                print('Get proxy', response.text)
                return response.text
            return None
        except ConnectionError as e:
            return None

    def parse_index(self, response):
        doc = pq(response.text)
        items = doc('.news-box .news-list .txt-box h3 a').items()
        for item in items:
            url = item.attr('href')
            weixin_request = WeixinRequest(url=url, callback=self.parse_detail, need_proxy=True)
            yield weixin_request
        next = doc('.sogou_next')
        if next:
            url = self.base_url + next.attr('href')
            yield WeixinRequest(url=url, callback=self.parse_index, need_proxy=True)

    def parse_detail(self, response):
        doc = pq(response.text)
        data = {
            'title': doc('.rich_media_title').text(),
            'content': doc('.rich_media_content').text(),
            'nickname': doc('.profile_nickname').text(),
            'wechat': doc('.profile_meta_value').text(),
            'date': doc('#publish_time').text()
        }
        yield data

    def request(self, weixin_request):
        try:
            if weixin_request.need_proxy:
                proxy = self.get_proxy()
                proxies = {
                    'http': 'http://' + proxy,
                    'https': 'https://' +proxy
                }
                return self.session.send(weixin_request.prepare(), proxies=proxies, timeout=
                                         weixin_request.timeout, allow_redirects=False)
            return self.session.send(weixin_request.prepare(), timeout=
                                     weixin_request.timeout, allow_redirects=False)
        except (ConnectionError, ReadTimeout) as e:
            print(e.args)
            return None

    def error(self, weixin_request):
        weixin_request.failed_time += 1
        print('Request failed', weixin_request.failed_time, 'Times', weixin_request.url)
        if weixin_request.failed_time < 5:
            self.queue.add(weixin_request)

    def schedule(self):
        while not self.queue.empty():
            weixin_request = self.queue.pop()
            callback = weixin_request.callback
            print('Schedule', weixin_request.url)
            response = self.request(weixin_request)
            if response and response.status_code == 200:
                results = list(callback(response))
                if results:
                    for result in results:
                        print('New result', type(result))
                        if isinstance(result, WeixinRequest):
                            self.queue.add(result)
                        if isinstance(result, dict):
                            # insert into mysql
                            print('Get an article')
                            print(result)
                else:
                    self.error(weixin_request)
            else:
                self.error(weixin_request)

    def run(self):
        self.start()
        self.schedule()


if __name__ == '__main__':
    spider = Spider()
    spider.start()
    spider.schedule()