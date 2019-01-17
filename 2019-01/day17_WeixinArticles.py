from urllib.parse import urlencode

import requests
from requests.exceptions import ConnectionError
from pyquery import PyQuery as pq

key_word = 'NBA'
base_url = 'https://weixin.sogou.com/weixin?'

headers = {
    'Cookie': 'SUV=00B317881B17ED1B5B6908F93A1EF865; CXID=CFB60C2B607DA865459A24D17B3BA704; SUID=344EB76F3865860A5B724D730004C0D3; ad=S0qdtZllll2tR0RPlllllVZYUAklllllL7K5Vyllll9lllll9klll5@@@@@@@@@@; IPLOC=CN4201; ABTEST=0|1547686493|v1; SNUID=059D2DEE8187FE1D55214B9C82D0A452; weixinIndexVisited=1; sct=1; JSESSIONID=aaaXZjIPEBIf1ah3M0fDw; ppinf=5|1547687614|1548897214|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZTo4OmF1dGhldGljfGNydDoxMDoxNTQ3Njg3NjE0fHJlZm5pY2s6ODphdXRoZXRpY3x1c2VyaWQ6NDQ6bzl0Mmx1TUNxYTBlU3lGcnExbE92aHQ3WG1Gd0B3ZWl4aW4uc29odS5jb218; pprdig=F6i8W6bdOvzk9VdKyTzIFox6el6wdZk078qjFdwWjtixQ1EuBy0TMq4BNhVUCknvuAz-sAuMG1dRzkeBg18UkrFK-2VeEt7R9a_Oqkv-NPCrUNxTWuP9wJmIZpOw09e1mnqwgwpGVRWk2JsG39iVF-HBkYzlfGgSuXqCJnd5RWk; sgid=11-38791065-AVwic1r4FhVQCia9uN2ia5YYaU; ppmdig=1547687614000000f589025875b012ad279dd84bfe683c5d',
    'Host': 'weixin.sogou.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
}

proxy = None
proxy_pool_url = ''

max_count = 5

def get_proxy(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None

def get_html(url, count):
    global proxy
    if count == max_count:
        print('Try Too Many Count')
        return None
    try:
        print('Crawling', url)
        print('Trying count', count)
        if proxy:
            proxies = {
                'http': 'http://' + proxy
            }
            response = requests.get(url, headers=headers, proxies=proxies, allow_redirects=False)
        else:
            response = requests.get(url, headers=headers, allow_redirects=False)
        if response.status_code == 200:
            return response.text
        if response.status_code == 302:
            #Need Proxy
            print('302')
            proxy = get_proxy(proxy_pool_url)
            if proxy:
                print('Using Proxy', proxy)
                get_html(url, count)
            else:
                print('Get No Proxy')
                return None
    except ConnectionError as e:
        print(e.args)
        count += 1
        get_html(url, count)

def get_index_page(keyword, page):
    data = {
        'query': keyword,
        'type': '2',
        'page': page,
        'ie': 'utf8'
    }
    queries = urlencode(data)
    url = base_url + queries
    html = get_html(url, 1)
    return html

def parse_one_page(html):
    doc = pq(html)
    for item in doc('.news-list li').items():
        yield {
            'href': item('.txt-box h3 a').attr('href'),
            'name': item('.txt-box h3').text(),
        }

def parse_article_page(html):
    doc = pq(html)
    intros = doc('.profile_inner p').items()
    return {
        'weixin_name': doc('.profile_nickname').text(),
        'weixin_number': intros[0].text(),
        'function_intro': intros[1].text(),
    }

def save_to_mongo(content):
    pass

def main():
    for page in range(1, 100):
        html = get_index_page(key_word, page)
        for item in parse_one_page(html):
            try:
                response = requests.get(item['href'])
                one_page = dict(item, parse_article_page(response.text))
                save_to_mongo(one_page)
            except ConnectionError:
                print('Article page error')

if __name__ == '__main__':
    get_index_page('NBA', 1)