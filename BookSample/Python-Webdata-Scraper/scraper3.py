from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import random
import datetime

URL = 'http://en.wikipedia.org'

random.seed(datetime.datetime.now())

def getLinks(articleUrl):
    html = urlopen("http://en.wikipedia.org" + articleUrl)
    bsObj = BeautifulSoup(html, "html.parser")
    return bsObj.find("div", {"id":"bodyContent"}).findAll("a",
                            href=re.compile("^(/wiki/)((?!:).)*$"))

# 不重复遍历网页的网址链接
class test1:
    def __init__(self):
        pages = set()

    def getLinks(self, pageUrl):
        html = urlopen(URL + pageUrl)
        bsObj = BeautifulSoup(html)
        for link in bsObj.findAll("a", href=re.compile("^(/wiki/)")):
            if 'href' in links.attrs:
                if link.attrs['href'] not in self.pages:
                    newPage = link.attrs['href']
                    print(newPage)
                    self.pages.add(newPage)
                    getLinks(newPage)

# 打印网页部分信息
class test2:
    def __init__(self):
        pages = set()

    def getLinks(self, pageUrl):
        html = urlopen(URL + pageUrl)
        bsObj = BeautifulSoup(html)
        try:
            print(bsObj.h1.get_text())
            print(bsObj.find(id='mw-content-text').findAll('p')[0])
            print(bsObj.find(id='ca-edit').find('span').find('a').attrs['href'])
        except AttributeError:
            print("This Page lost some data, but it doesn't matter!")

        for link in bsObj.findAll('a', href=re.compile("^(/wiki/)")):
            if 'href' in link.attrs:
                if link.attrs['href'] not in self.pages:
                    newPage = link.attrs['href']
                    print("---------------\n" + newPage)
                    self.pages.add(newPage)
                    getLinks(newPage)



if __name__ == "__main__":
    links = getLinks("/wiki/Kevin_Bacon")
    while len(links) > 0:
        newArticle = links[random.randint(0, len(links) - 1)].attrs["href"]
        print(newArticle)
        links = getLinks(newArticle)