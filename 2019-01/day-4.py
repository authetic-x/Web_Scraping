'''
It's demo for Chapter 5 -- Data Persistence
Use os module and learn some Mysql
'''

import os
import csv
from urllib.request import urlretrieve
from urllib.request import urlopen
from bs4 import BeautifulSoup


downloadDirectory = 'downloaded'
baseUrl = 'http://pythonscraping.com'

def getAbsoluteUrl(baseUrl, source):
    if source.startswith("http://www."):
        url = 'http://' + source[11:]
    elif source.startswith("http://"):
        url = source
    elif source.startswith("www."):
        url = "http://" + source[4:]
    else:
        url = baseUrl + "/" + source
    if baseUrl not in url:
        return None
    return url

def getDownloadPath(baseUrl, absoluteUrl, downloadDirectory):
    path = absoluteUrl.replace('www.', "")
    path = path.replace(baseUrl, "")
    path = path.replace('/', "")
    path = downloadDirectory + "/" + path
    directory = os.path.dirname(path)

    if not os.path.exists(directory):
        os.makedirs(directory)

    return path

def csv_test(url):
    html = urlopen(url)
    bsObj = BeautifulSoup(html, 'html.parser')
    table = bsObj.findAll('table', {'class':'wikitable'})[0]
    rows = table.findAll('tr')

    csvFile = open('editors.csv', 'wt', newline='', encoding='utf-8')
    writer = csv.writer(csvFile)
    try:
        for row in rows:
            csvRow = []
            for cell in row.findAll(['td', 'th']):
                csvRow.append(cell.get_text())
            writer.writerow(csvRow)
    finally:
        csvFile.close()

def main():
    '''
    html = urlopen("http://www.pythonscraping.com/")
    bsObj = BeautifulSoup(html, 'html.parser')
    downloadList = bsObj.findAll(src=True)

    i = 0

    for download in downloadList:
        fileUrl = getAbsoluteUrl(baseUrl, download['src'])
        if fileUrl is not None:
            print(fileUrl)
            i += 1
            urlretrieve(fileUrl, "downloaded/" + str(i))
    '''
    csv_test('https://en.wikipedia.org/wiki/Comparison_of_text_editors')

import pymysql
conn = pymysql.connect(host='127.0.0.1',
                       user='root', passwd='123456', db='test')

cur = conn.cursor()
cur.execute('USE test')

cur.execute('INSERT INTO pages (id, title) VALUES (1, "test page")')
cur.execute('SELECT * FROM pages WHERE id = 1')
print(cur.fetchone())
cur.close()
conn.close()