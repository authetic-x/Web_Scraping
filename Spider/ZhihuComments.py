
import requests
from bs4 import BeautifulSoup
import re


def get_page(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    return 'wrong'

def main():
    url = 'https://zhuanlan.zhihu.com/p/45471645'
    html = get_page(url)
    bp = BeautifulSoup(html, 'html.parser')
    comment_lists = re.findall('<div.*?class="RichText ztext CommentItem-content".*?</div>',
                               html, re.S)
    print(comment_lists)

main()