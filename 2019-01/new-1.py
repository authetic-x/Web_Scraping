from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup

import requests
import os


def get_title(url):
    try:
        html = urlopen(url)
    except (HTTPError, URLError) as e:
        return None

    try:
        bsobj = BeautifulSoup(html.read())
        title = bsobj.body.h1
    except AttributeError as e:
        return None

def child_tag(url):
    bsobj = BeautifulSoup(urlopen(url).read())

    #print(bsobj.find("table", {"id":"giftList"}))
    for child in bsobj.find("table", {"id":"giftList"}).children:
        print(child)

def main():
    '''
    title = get_title("http://www.baidu.com")
    if title == None:
        print("Title could not be found.")
    else:
        print(title)
    '''

    #child_tag("http://www.pythonscraping.com/pages/page3.html")

    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                     'AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
                     '/70.0.3538.77 Safari/537.36',
        'Cookie':'JSESSIONID=07FB7F79C16365D7C3E1EA50ABB7B420; UM_dis'
                 'tinctid=166c507dac2ee-0e64734c8cc5cd-9393265-e1000-1'
                 '66c507dac7116; BIGipServerxg=592488640.20480.0000'
    }
    url = 'http://xssw.ccnu.edu.cn/xgxt/xsxx_xsgl.do?method=showPhoto&amp;xh=2016211073'

    response = requests.get(url, headers = headers)
    file = open('test.gif', 'wb')
    file.write(response.content)
    print(response.content)

main()