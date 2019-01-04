'''
It's a long day, starting Chapter 3, lots of code.
2019 / 01 / 02
authetic Xu
'''

from urllib.request import urlopen
from urllib.parse import urlparse
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import re
import datetime
import random


def demo1(url):
    html = urlopen(url)
    bsobj = BeautifulSoup(html)
    for link in bsobj.find('div', {'id':'bodyContent'}).findAll(
                    'a', href=re.compile("^(/wiki/)((?!:).)*$")):
        if 'href' in link.attrs:
            print(link.attrs['href'])

pages = set()
def demo2(page_url):
    global pages
    html = urlopen("http://wikipedia.org" + page_url)
    bsobj = BeautifulSoup(html)
    try:
        print(bsobj.h1.get_text())
        print(bsobj.find(id="mw-content-text").findAll("p")[0])
    except AttributeError:
        print("Some message not found, don't worry!")

    for link in bsobj.findAll("a", href=re.compile("^(/wiki/)")):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                new_page = link.attrs['href']
                pages.add(new_page)
                print("---------------\n" + new_page)
                demo2(new_page)

random.seed(datetime.datetime.now())

class Demo3:
    def __init__(self):
        self.exLinks = 0
        self.inLinks = 0

    def getInternalLink(self, bsObj):
        internalLinks = []
        for link in bsObj.findAll("a", href=re.compile("^(/)((?!:).)*$")):
            if link.attrs['href'] is not None:
                if link.attrs['href'] not in internalLinks:
                    self.inLinks += 1
                    internalLinks.append(link.attrs['href'])
        return internalLinks

    def getExternalLink(self, bsObj, exclude_url):
        externalLinks = []
        for link in bsObj.findAll("a", href=
                re.compile("^(http|https|www)((?!" + exclude_url + ").)*$")):
            if link.attrs['href'] is not None:
                if link.attrs['href'] not in externalLinks:
                    self.exLinks += 1
                    externalLinks.append(link.attrs['href'])
        return externalLinks

    def getRandomExternalLink(self, startingPage):
        try:
            html = urlopen(startingPage)
        except (HTTPError, URLError) as e:
            print("Some error happened!")
            return None
        bsObj = BeautifulSoup(html, "html.parser")
        externalLinks = self.getExternalLink(bsObj, urlparse(startingPage).netloc)
        if len(externalLinks) == 0:
            print("There is no externalLink here, looking around the site for one.")
            internalLinks = self.getInternalLink(bsObj)
            return self.getRandomExternalLink(internalLinks[random.randint(0, len(internalLinks)-1)])
        else:
            return externalLinks[random.randint(0, len(externalLinks)-1)]

    def followExternalOnly(self, startingSite):
        externalLink = self.getRandomExternalLink(startingSite)
        if externalLink is None:
            print("Current internalLinks: " + str(self.inLinks))
            print("Current externalLinks: " + str(self.exLinks))
            return
        print("Random external link is: " + externalLink)
        self.followExternalOnly(externalLink)

def main():
    url = 'https://en.wikipedia.org/wiki/Kevin_Durant'
    #demo1(url)
    #demo2("/wiki/Kevin_Durant")

    test_demo = Demo3()
    test_demo.followExternalOnly("https://en.wikipedia.org/wiki/Kevin_Durant")

main()