import requests
from requests.exceptions import ConnectionError

base_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
}

def get_page(url, **options):
    headers = dict(base_headers, **options)
    print('正在爬取页面', url)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print('爬取成功', url, response.status_code)
            return response.text
    except ConnectionError:
        print('爬取失败', url)
        return None