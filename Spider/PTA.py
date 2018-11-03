#coding: utf-8

import requests

'''
    爬取拼题A上题目集的名字，该网站用js动态加载，比较方便
    url: https://pintia.cn/problem-sets
'''


def get_response(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def get_problemSets(json):

    for item in json.get('problemSets'):
        yield item.get('name')

def main():
    url = 'https://pintia.cn/api/problem-sets?category=&limit=20&keyword=&need_category=false&page=&organization=&organization_id='
    response = get_response(url)
    for problem in get_problemSets(response):
        print(problem)

if __name__ == '__main__':
    main()