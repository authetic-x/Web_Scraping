'''
Here we'll try to take some unittests.
'''

from urllib.request import urlopen
from bs4 import BeautifulSoup
import unittest
import re
import datetime
import random

random.seed(datetime.datetime.now())

class TestWikipedia(unittest.TestCase):
    bsObj = None
    url = None
    
    def test_PageProperty(self):
        global bsObj
        global url
        
        url = 'https://en.wikipedia.org/wiki/Python_(programming_language)'
        for i in range(0, 20):
            bsObj = BeautifulSoup(urlopen(url), 'html.parser')
            titles = self.titleMatchUrl()
            self.assertEqual(titles[0], titles[1])
            self.assertTrue(self.contentExist())
            url = self.getNextLink()
    
    def titleMatchUrl(self):    
        global bsObj
        global url
        pageTitle = bsObj.find('h1').get_text()
        urlTitle = url[(url.index("/wiki/")+6):]
        urlTitle = urlTitle.replace("_", " ")
        return [pageTitle.lower(), urlTitle.lower()]
    
    def contentExist(self):
        global bsObj
        content = bsObj.find("div", {'id':'mw-content-text'})
        if content is not None:
            return True
        return False
    
    def getNextLink(self):
        links = []
        for link in bsObj.findAll('a', href=re.compile('^(/wiki/)((?!:).)*$')):
            if link.attrs['href'] is not None:
                links.append('https://en.wikipedia.org' + link.attrs['href'])
        return links[random.randint(0, len(links))]

if __name__ == '__main__':
    #unittest.main()
    import this
    print(this)