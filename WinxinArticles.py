from urllib.parse import urlencode

import pymysql
import requests
from redis import StrictRedis
from requests import Request, Session
from requests.exceptions import ConnectionError, ReadTimeout
from pickle import dumps, loads
from ProxyPool.settings import *
from pyquery import PyQuery as pq

TIMEOUT = 10
VALID_STATUS = [200]
MAX_FAILED_TIME = 5

PROXY_POOL_URL = ''

class WeixinRequest(Request):
    def __init__(self, url, callback, method='GET', headers=None, need_proxy=False,
                 fail_time=0, timeout=TIMEOUT):
        Request.__init__(self, method, url, headers)
        self.callback = callback
        self.need_proxy = need_proxy
        self.fail_time = fail_time
        self.timeout = timeout

class RedisQueue():
    def __init__(self):
        self.db = StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)

    def add(self, request):
        if isinstance(request, WeixinRequest):
            return self.db.rpush(REDIS_KEY, dumps(request))
        return False

    def pop(self):
        if self.db.llen(REDIS_KEY):
            return loads(self.db.lpop(REDIS_KEY))
        else:
            return False

    def empty(self):
        return self.db.llen(REDIS_KEY) == 0

class Mysql():
    class MySQL():
        def __init__(self, host='MYSQL_HOST', username='MYSQL_USER', password='MYSQL_PASSWORD', port='MYSQL_PORT',
                     database='MYSQL_DATABASE'):
            """
            MySQL初始化
            :param host:
            :param username:
            :param password:
            :param port:
            :param database:
            """
            try:
                self.db = pymysql.connect(host, username, password, database, charset='utf8', port=port)
                self.cursor = self.db.cursor()
            except pymysql.MySQLError as e:
                print(e.args)

        def insert(self, table, data):
            """
            插入数据
            :param table:
            :param data:
            :return:
            """
            keys = ', '.join(data.keys())
            values = ', '.join(['%s'] * len(data))
            sql_query = 'insert into %s (%s) values (%s)' % (table, keys, values)
            try:
                self.cursor.execute(sql_query, tuple(data.values()))
                self.db.commit()
            except pymysql.MySQLError as e:
                print(e.args)
                self.db.rollback()

class Spider():
    base_url = ''
    key_word = 'NBA'
    headers = {
        'Cookie': 'SUV=00B317881B17ED1B5B6908F93A1EF865; CXID=CFB60C2B607DA865459A24D17B3BA704; SUID=344EB76F3865860A5B724D730004C0D3; ad=S0qdtZllll2tR0RPlllllVZYUAklllllL7K5Vyllll9lllll9klll5@@@@@@@@@@; IPLOC=CN4201; ABTEST=0|1547686493|v1; SNUID=059D2DEE8187FE1D55214B9C82D0A452; weixinIndexVisited=1; sct=1; JSESSIONID=aaaXZjIPEBIf1ah3M0fDw; ppinf=5|1547687614|1548897214|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZTo4OmF1dGhldGljfGNydDoxMDoxNTQ3Njg3NjE0fHJlZm5pY2s6ODphdXRoZXRpY3x1c2VyaWQ6NDQ6bzl0Mmx1TUNxYTBlU3lGcnExbE92aHQ3WG1Gd0B3ZWl4aW4uc29odS5jb218; pprdig=F6i8W6bdOvzk9VdKyTzIFox6el6wdZk078qjFdwWjtixQ1EuBy0TMq4BNhVUCknvuAz-sAuMG1dRzkeBg18UkrFK-2VeEt7R9a_Oqkv-NPCrUNxTWuP9wJmIZpOw09e1mnqwgwpGVRWk2JsG39iVF-HBkYzlfGgSuXqCJnd5RWk; sgid=11-38791065-AVwic1r4FhVQCia9uN2ia5YYaU; ppmdig=1547687614000000f589025875b012ad279dd84bfe683c5d',
        'Host': 'weixin.sogou.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    }
    session = Session()
    queue = RedisQueue()

    def start(self):
        self.session.headers.update(self.headers)
        start_url = self.base_url + urlencode({'query': self.key_word, 'type': 2})
        weixin_request = WeixinRequest(url=start_url, callback=self.parse_index, need_proxy=True)
        self.queue.add(weixin_request)

    def get_proxy(self):
        try:
            response = requests.get(PROXY_POOL_URL)
            if response.status_code == 200:
                return response.text
            return None
        except ConnectionError:
            return None

    def parse_index(self, response):
        doc = pq(response.text)
        items = doc('.news-box .news-list li .txt-box h3 a').items()
        for item in items:
            url = item.attr('href')
            weixin_request = WeixinRequest(url=url, callback=self.parse_detail)
            yield weixin_request
        next = doc('#sogou_next').attr('href')
        if next:
            url = self.base_url + str(next)
            yield WeixinRequest(url=url, callback=self.parse_index)

    def parse_detail(self, response):
        doc = pq(response.text)
        data = {
            'title': doc('.rich_media_title').text(),
            'content': doc('.rich_media_content').text(),
            'date': doc('#post-date').text(),
            'nickname': doc('#js_profile_qrcode > div > strong').text(),
            'wechat': doc('#js_profile_qrcode > div > p:nth-child(3) > span').text()
        }
        yield data

    def request(self, weixin_request):
        try:
            if weixin_request.need_proxy:
                proxy = self.get_proxy()
                if proxy:
                    proxies = {
                        'http': 'http://' + proxy
                    }
                    return self.session.send(weixin_request.prepare(), timeout=weixin_request.timeout,
                                      allow_redirects=False, proxies=proxies)
            return self.session.send(weixin_request.prepare(), timeout=weixin_request.timeout,
                              allow_redirects=False)
        except (ConnectionError, ReadTimeout) as e:
            print(e.args)
            return False

    def error(self, weixin_request):
        weixin_request.fail_time += 1
        print('Request failed', weixin_request.fail_time, 'Times', weixin_request.url)
        if weixin_request.fail_time < MAX_FAILED_TIME:
            self.queue.add(weixin_request)

    def schedule(self):
        while not self.queue.empty():
            weixin_request = self.queue.pop()
            callback = weixin_request.callback
            print('Schedule', weixin_request.url)
            response = self.request(weixin_request)
            if response and response.status_code in VALID_STATUS_CODES:
                results = list(callback(response))
                if results:
                    for result in results:
                        print('New result', result)
                        if isinstance(result, WeixinRequest):
                            self.queue.add(result)
                        if isinstance(result, dict):
                            self.error(weixin_request)
                else:
                    self.error(weixin_request)
            else:
                self.error(weixin_request)

    def run(self):
        self.start()
        self.schedule()

if __name__ == '__main__':
    spider = Spider()
    spider.run()