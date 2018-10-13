#coding: utf8

import os
import requests
from urllib.parse import urlencode
from hashlib import md5

def get_one_page(offset):
    params = {
        'offset': offset,
        'format': 'json',
        'keyword': '街拍',
        'autoload': 'true',
        'count': '20',
        'cur_tab': '1'
    }
    url = 'https://www.toutiao.com/search_content/?' + urlencode(params)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print('yeah')
            return response.json()
    except requests.ConnectionError:
        print('error')
        return None

def get_images(json):
    if json.get('data'):
        for item in json.get('data'):
           if item.get('title'):
               title = item.get('title')
               images = item.get('image_list')
               for image in images:
                   print('4')
                   yield {
                       'title': title,
                       'image_url': 'http:'+image.get('url')
                   }

def save_image(item):
    if not os.path.exists('result\\'+item.get('title')):
        os.makedirs('result\\'+item.get('title'))
    try:
        response = requests.get(item.get('image_url'))
        if response.status_code == 200:
            file_path = 'result\\{0}/{1}.{2}'.format(item.get('title'), md5(response.content).hexdigest(), 'jpg')
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.write(response.content)
            else:
                print('Already Downloaded', file_path)
    except requests.ConnectionError:
        print('Failed to save image!')

from multiprocessing.pool import Pool

def main(offset):
    json = get_one_page(offset)
    for item in get_images(json):
        print(item)
        save_image(item)

GROUP_START = 1
GROUP_END = 5

if __name__ == '__main__':
    pool = Pool()
    groups = ([x * 20 for x in range(GROUP_START, GROUP_END+1)])
    pool.map(main, groups)
    pool.close()
    pool.join()
