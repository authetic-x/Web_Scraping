'''
It's third day, long day still, to finish Chapter 4 --  API USE
There is some example in book here
This is real crawler!
'''

import json
import datetime
import re
import random
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

random.seed(datetime.datetime.now())

def getCountry(ipAdress):
    try:
        response = urlopen("http://api.ipstack.com/" + ipAdress + "?access_key=892d4292e7da3d7fdc8ff4d59ddce5e7") \
            .read().decode('utf-8')
    except HTTPError:
        return None
    responseJson = json.loads(response)
    return responseJson.get("country_code")

def getLinks(acticleUrl):
    html = urlopen("https://en.wikipedia.org" + acticleUrl)
    bsObj = BeautifulSoup(html, "html.parser")
    return bsObj.find('div', {"id":"bodyContent"}).\
                findAll("a", href=re.compile("^(/wiki/)((?!:).)*$"))

def getHistoryIPs(pageUrl):
    pageUrl = pageUrl.replace("/wiki/", "")
    historyUrl = "https://en.wikipedia.org/w/index.php?title=" + pageUrl + "&action=history"
    print("history url is: " + historyUrl)
    html = urlopen(historyUrl)
    bsObj = BeautifulSoup(html, "html.parser")
    ipAddresses = bsObj.findAll("a", {"class":"mw-userlink mw-anonuserlink"})
    addressList = set()
    for ipAddress in ipAddresses:
        addressList.add(ipAddress.get_text())
    return addressList

def main():
    links = getLinks("/wiki/Python_(programming_language)")

    while len(links) > 0:
        for link in links:
            print("---------------")
            historyIPs = getHistoryIPs(link.attrs['href'])
            for historyIP in historyIPs:
                country = getCountry(historyIP)
                if country is not None:
                    print(historyIP + " is from " + country)

        newLink = links[random.randint(0, len(links) - 1)].attrs['href']
        links = getLinks(newLink)


main()