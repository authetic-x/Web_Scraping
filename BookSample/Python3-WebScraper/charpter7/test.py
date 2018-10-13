#coding: utf8

from selenium import webdriver

browser = webdriver.Chrome()
browser.get('http://baidu.com')
print(browser.page_source)
browser.close()