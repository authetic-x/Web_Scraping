'''
Here we'll show how to clean the dirty data.
'''

import re
import string
from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections import OrderedDict


def cleanInput(input):
    input = re.sub('\n+', " ", input)
    input = re.sub('\[[0-9]*\]', '', input)
    input = re.sub(' +', ' ', input)
    input = bytes(input, 'UTF-8')
    input = input.decode("ascii", "ignore")
    cleanInput  = []
    input = input.split(' ')
    for item in input:
        item = item.strip(string.punctuation)
        if len(item) > 1 or (item.lower() == 'a' or item.lower() == 'i'):
            cleanInput.append(item)
    return cleanInput

def ngrams(input, n):
    input = cleanInput(input)
    output = []
    for i in range(len(input) - n+1):
        output.append(input[i : i+n])
    return output

def main():
    html = urlopen("https://en.wikipedia.org/wiki/Sorry_(Meg_Myers_album)")
    bsObj = BeautifulSoup(html, 'html.parser')
    input = bsObj.find('div', {'id':'mw-content-text'}).get_text()
    ngram = ngrams(input, 2)
    #ngram = OrderedDict(sorted(ngram.items(), key=lambda t : t[1], reverse=True))
    print(ngram)

if __name__ == '__main__':
    main()