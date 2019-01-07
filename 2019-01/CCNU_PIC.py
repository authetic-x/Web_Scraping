'''
Try to get everyone's pic in CCNU official website
'''

from urllib.request import urlopen
from urllib.error import HTTPError, URLError
import os


def download(picUrl):
    try:
        with open("", 'w') as file:
            file.write("")
    except:
        print("Some error happened when download.")

