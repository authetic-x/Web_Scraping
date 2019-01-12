'''
Get ariana's pics in JinRiTouTiao, some problems can't
be solved, weird! Try to use MongoDB, and download pics.
'''
import json
from urllib.parse import urlencode

import requests
from requests.exceptions import RequestException
import pymongo
import os
from hashlib import md5
from multiprocessing import Pool
from json.decoder import JSONDecodeError

MONGO_URL = 'localhost'
MONGO_DB = 'toutiao'
MONGO_TABLE = 'toutiao'

GROUP_START = 0
GROUP_END = 20

client = pymongo.MongoClient(MONGO_URL, connect=False)
db = client[MONGO_DB]


def get_one_page(offset, keyword):
    data = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': 20,
        'cur_tab': 1,
        'from': 'search_tab',
        'pd': 'synthesis'
    }
    url = 'https://www.toutiao.com/search_content/?' + urlencode(data)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('Request error.')
        return None

def parse_one_page(html):
    try:
        data = json.loads(html)
        if data and 'data' in data.keys():
            for item in data.get('data'):
                if item.get('title') is not None:
                    yield {
                        'title': item.get('title'),
                        'url': item.get('article')
                    }
    except JSONDecodeError:
        pass

def save_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print('Insert succeed')
        return True
    return False

def download_img(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            save_img(response.content)
        return None
    except RequestException:
        print('Request error.')
        return None

def save_img(content):
    file_path = "{0}/{1}.{2}".format(os.getcwd(), md5(content).hexdigest(),
                                     'jpg')
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(content)
            f.close()

def main(offset):
    html = get_one_page(offset, 'ariana')
    for item in parse_one_page(html):
        print(item['title'], item['url'])
        save_to_mongo(item)

if __name__ == '__main__':
    pool = Pool()
    groups = [x*20 for x in range(GROUP_START, GROUP_END)]
    pool.map(main, groups)