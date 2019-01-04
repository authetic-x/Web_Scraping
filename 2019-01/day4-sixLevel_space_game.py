'''
Here is a interesting trial call 'Six level space game
in mysql'. Search pages which can be reached less than
six links from one page, start from the page of Stephan
Curry.
'''

import pymysql
import datetime
import re
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup

'''
table1 = "CREATE TABLE pages(" \
         "id INT NOT NULL AUTO_INCREMENT," \
         "url varchar (255) NOT NULL," \
         "created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ," \
         "PRIMARY KEY (id))"

table2 = "CREATE TABLE links(" \
         "id INT NOT NULL AUTO_INCREMENT," \
         "fromPageId INT NULL," \
         "toPageId INT NULL ," \
         "created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ," \
         "PRIMARY KEY (id))"

conn = pymysql.connect(host='localhost', user='root', passwd='123456',
                       db='wikipedia')

try:
    with conn.cursor() as cursor:
        cursor.execute(table1)
        cursor.execute(table2)
    conn.commit()
    print('Database initialized.')
finally:
    conn.close()
'''

conn = pymysql.connect(host='localhost', user='root', passwd='123456',
                       db='wikipedia')
cursor = conn.cursor()
pages = set()
links_reached = 0

def getPageId(url):
    cursor.execute("SELECT * FROM pages WHERE url = %s", (url))
    if cursor.rowcount == 0:
        cursor.execute("INSERT INTO pages (url) VALUES (%s)", (url))
        conn.commit()
        return cursor.lastrowid
    else:
        return cursor.fetchone()[0]

def insertLink(fromPageId, toPageId):
    cursor.execute("SELECT * FROM links WHERE fromPageId = %s AND toPageId = %s",
                   (int(fromPageId), int(toPageId)))
    if cursor.rowcount == 0:
        cursor.execute("INSERT INTO links (fromPageId, toPageId) VALUES (%s, %s)",
                       (int(fromPageId), int(toPageId)))
        conn.commit()

def getLinks(pageUrl, recursion):
    global pages
    global links_reached
    if recursion >= 4:
        return
    try:
        html = urlopen('https://en.wikipedia.org' + pageUrl)
    except (HTTPError, URLError):
        print('Some error!')
        return
    bsObj = BeautifulSoup(html, 'html.parser')
    pageId = getPageId(pageUrl)
    for link in bsObj.findAll('a', href=re.compile("^(/wiki/)((?!:).)*$")):
        insertLink(pageId, getPageId(link.attrs['href']))
        if link.attrs['href'] not in pages:
            if links_reached > 100:
                return
            links_reached += 1
            newPage = link.attrs['href']
            pages.add(newPage)
            getLinks(newPage, recursion+1)

def main():
    global pages
    getLinks('/wiki/Stephen_Curry', 1)
    for link in pages:
        print(link)
    cursor.close()
    conn.close()

main()