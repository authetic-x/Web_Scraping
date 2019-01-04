from selenium import webdriver
import time

browser = webdriver.Chrome()
browser.get('https://www.taobao.com/')
browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
browser.execute_script('alert("easy")')