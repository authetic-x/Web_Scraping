# coding: utf8

import requests
import re
import json
import time



def get_one_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }
    html = requests.get(url, headers=headers)
    if html.status_code == 200:
        return html.text
    else:
        return None


def parse_one_page(html):
    if html == None:
        print('none')
        return
    pattern = re.compile('<dd.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)"'
                         '.*?name.*?<a.*?>(.*?)</a>.*?star.*?>(.*?)</p>'
                         '.*?releasetime.*?>(.*?)</p>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2].strip(),
            'actor': item[3].strip()[3:],
            'time': item[4].strip()[5:]
        }


def write_to_file(content):
    with open('result.txt', 'a', encoding='utf8') as f:
        print(type(json.dumps(content)))
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


if __name__ == '__main__':
    for i in range(10):
        main(offset=i * 10)
        time.sleep(1)
