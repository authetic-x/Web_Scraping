# coding: utf8

import requests
from urllib import parse
from bs4 import BeautifulSoup

def get_one_page(url):
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/68.0.3440.106 Safari/537.36'
    }
    response=  requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    return None

def main():
    url = 'https://www.douban.com/'
    html = get_one_page(url)
    bsObj = BeautifulSoup(html, "html.parser")
    movie_part = bsObj.find('div', {'class':'movie-list list'})
    result = parse.urlparse(url)
    #print(movie_part)
    print(type(result), result)

main()
