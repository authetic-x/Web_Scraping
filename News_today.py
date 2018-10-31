import requests
from urllib.parse import urlencode
import os


def get_page(offset):
    params = {
        'offset':offset,
        'format':'json',
        'keyword':'游戏',
        'autoload':'true',
        'count':'20',
        'cur_tab':'1',
        'from':'search_tab'
    }
    url = 'https://www.toutiao.com/search_content/?' + urlencode(params)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError:
        return None

def get_images(json):
    if json.get('data'):
        for item in json.get('data'):
            if item.get('open_url'):
                title = item.get('title')
                image = item.get('large_image_url')
                yield {
                    'image_url':image,
                    'title':title
                }

def save_image(item):
    if not (os.path.exists('images')):
        os.mkdir('images')
    try:
        response = requests.get(item.get('image_url'))
        if response.status_code == 200:
            filepath = 'images/{0}.jpg'.format(item.get('title'))
            with open(filepath, 'wb') as f:
                f.write(response.content)
    except requests.ConnectionError:
        print('Fail to save image.')

def main():
    for i in range(0,1):
        json = get_page(i*20)
        for item in get_images(json):
            save_image(item)



if __name__ == '__main__':
    main()

