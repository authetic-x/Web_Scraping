'''
Here are some mysql practice, use mysql
to store messages in WIKI with simple structure.
'''

import pymysql
import re
import datetime
import random
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError, URLError

conn = pymysql.connect(host='localhost', user='root', passwd='123456', db='test')
cur = conn.cursor()

'''
sql = "CREATE TABLE article (" \
      "id BIGINT(7) NOT NULL AUTO_INCREMENT, title VARCHAR (200)," \
      "content VARCHAR (10000), created TIMESTAMP DEFAULT CURRENT_TIMESTAMP ," \
      "PRIMARY KEY (id))"
'''

random.seed(datetime.datetime.now())

def store(title, content):
    cur.execute("INSERT INTO article (title, content) VALUES (\"%s\", \"%s\")", (title, content))
    cur.connection.commit()

def getLinks(articleUrl):
    try:
        html = urlopen("https://en.wikipedia.org" + articleUrl)
    except (HTTPError, URLError):
        print("Some error")
        return
    bsObj = BeautifulSoup(html, 'html.parser')
    title = bsObj.find("h1").get_text()
    content = bsObj.find("div", {'id':'mw-content-text'}).find('p').get_text()
    store(title, content)
    return bsObj.find('div', {'id':'bodyContent'}).findAll('a', href=re.compile("^(/wiki/)((?!:).)*$"))

def main():
    links = getLinks("/wiki/Main_Page")
    try:
        while len(links) > 0:
            newArticle = links[random.randint(0, len(links)-1)].attrs['href']
            print(newArticle)
            links = getLinks(newArticle)
    finally:
        cur.close()
        conn.close()

main()