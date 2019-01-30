'''
Get the hottest news title on baidu page,
then save these data into mysql
'''
import datetime

import pymysql
from pyquery import PyQuery as pq
import requests
from requests.exceptions import ConnectionError

URL = 'https://www.baidu.com/s?wd=%E7%83%AD%E7%82%B9'
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    'Upgrade-Insecure-Requests': '1'
}

def get_html(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError as e:
        print(e.args)
        return None

def parse_html(html):
    doc = pq(html)
    trs = doc('.FYB_RD table.c-table tr').items()
    for tr in trs:
        index = tr('td:nth-child(1) span.c-index').text()
        title = tr('td:nth-child(1) span a').text()
        hot = tr('td:nth-child(2)').text().strip('"')
        yield {
            'index':index,
            'title':title,
            'hot':hot
        }

def save_to_mysql(items):
    try:
        db = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456',
                             db='crawls', charset='utf8')
        cursor = db.cursor()
        cursor.execute('use crawls;')
        cursor.execute('CREATE TABLE IF NOT EXISTS baiduNews('
                       'id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,'
                       'ranking VARCHAR(30),'
                       'title VARCHAR(60),'
                       'datetime TIMESTAMP,'
                       'hot VARCHAR(30));')
        try:
            for item in items:
                print(item)
                now = datetime.datetime.now()
                now = now.strftime('%Y-%m-%d %H:%M:%S')
                sql_query = 'INSERT INTO baiduNews(ranking, title, datetime, hot) VALUES ("%s", "%s", "%s", "%s")' % (
                            item['index'], item['title'], now, item['hot'])
                cursor.execute(sql_query)
                print('Save into mysql')
            db.commit()
        except pymysql.MySQLError as e:
            db.rollback()
            print(e.args)
            return
    except pymysql.MySQLError as e:
        print(e.args)
        return

def check_mysql():
    try:
        db = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456',
                             db='crawls', charset='utf8')
        cursor = db.cursor()
        cursor.execute('use crawls;')
        sql_query = 'SELECT * FROM baiduNews'
        results = cursor.execute(sql_query)
        print(results)
    except pymysql.MySQLError as e:
        print(e.args)

def main():
    html = get_html(URL)
    items = parse_html(html)
    save_to_mysql(items)
    #check_mysql()

if __name__ == '__main__':
    main()