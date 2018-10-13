from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError, URLError


def gettitle(url):
    try:
        html = urlopen(url)
    except (HTTPError, URLError) as e:
        return None
    try:
        bsObj = BeautifulSoup(html.read())
        title = bsObj
    except AttributeError as e:
        return None
    return title

title = gettitle("http://www.pythonscraping.com/pages/page1.html")
if title == None:
    print("Title could not be found")
else:
    print(title)