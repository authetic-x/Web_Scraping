# coding: utf8

from pyquery import PyQuery as pq
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 '              ''
                  '(KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}


def test1(url):
    try:
        html = requests.get(url, headers=headers).text
        doc = pq(html)
        items = doc('.explore-tab .feed-item').items()
        for item in items:
            question = item.find('h2').text()
            author = item.find('.author-link').text()
            answer = pq(item.find('.content')).text()
            with open('explore.txt', 'a+', encoding='utf-8') as file:
                print(question)
                file.write('\n'.join([question, author, answer]))
                file.write('\n' + '=' * 50 + '\n')
                file.close()
    except:
        print('Fail')

test1('https://www.zhihu.com/explore')