'''
Scraping simple messages of University Rank of CS from 'https://www.dxsbb.com/news/1797.html'
Using requests + pyquery + mysql
'''
import sys

import pymysql
import requests
from requests.exceptions import ConnectionError
from pyquery import PyQuery as pq

URL = 'https://www.dxsbb.com/news/1797.html'

def get_html(url):
    try:
        response = requests.get(url)
        response.encoding = 'GBK'
        if response.status_code == 200:
            print('Scraping successfully', url)
            return response.text
        return None
    except ConnectionError as e:
        print('Scraping failed', e.args)
        return None

def parge_html(html):
    doc = pq(html)
    trs = doc('.b table tr:gt(0)').items()
    for tr in trs:
        rank = tr('td:nth-child(1)').text()
        name = tr('td:nth-child(2)').text()
        score = tr('td:nth-child(3)').text()
        yield {
            'rank':rank,
            'name':name,
            'score':score
        }

def save_to_mysql(content):
    try:
        db = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456',
                             db='crawls', charset='utf8')
        cursor = db.cursor()
        # rank为mysql保留字，建表报错
        '''
        CREATE TABLE csrank(
            id int primary key auto_increment,
            rankpos varchar(30),
            college varchar(30),
            score varchar(30));
        '''
        try:
            for item in content:
                sql_query = 'insert into csrank(rankpos, college, score) values ("%s", "%s", "%s")' % (
                    item['rank'], item['name'], item['score']
                )
                cursor.execute(sql_query)
                print('Store successfully')
        except pymysql.MySQLError as e:
            db.rollback()
            print(e.args)
    except pymysql.MySQLError as e:
        print(e.args)

def main():
    html = get_html(URL)
    content = parge_html(html)
    save_to_mysql(content)

if __name__ == '__main__':
    main()