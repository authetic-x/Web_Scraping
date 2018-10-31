
import requests
from bs4 import BeautifulSoup
import os
import re
import json


header = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}

filepath = 'images'

def get_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return None

def get_items(html):
    pats = re.findall(r'"keys":(.*?),"data"', html)
    items = json.loads(pats[0])
    return items

def get_image_url(items):
    images = []
    for hero_id in items.keys():
        for i in range(0, 10):
            num = str(i)
            if len(num) == 1:
                num = '00'+num
            if len(num) == 2:
                num = '0' + num
            num_url = hero_id+num
            url = 'http://ossweb-img.qq.com/images/lol/web201310/skin/big' \
                  + num_url + '.jpg'
            images.append(url)
    return images

def make_list_filepath(items):
    list_filepath = []
    for name in items.values():
        for i in range(0,10):
            num = str(i)
            path = filepath + '/' + name + num + '.jpg'
            list_filepath.append(path)
    return list_filepath

def save_images(url):
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    html = get_page(url)
    items = get_items(html)
    list_filepath = make_list_filepath(items)
    images = get_image_url(items)
    n = 0

    for image in images:

        # print(image)
        response = requests.get(image)
        n += 1

        if n == 20:
            break
        if response.status_code == 200:
            path = list_filepath[n]
            print('正在下载...' + path)
            with open(path, 'wb') as f:
                f.write(response.content)



def main():
    url = 'https://lol.qq.com/biz/hero/champion.js'
    save_images(url)

main()