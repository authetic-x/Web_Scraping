'''
Here we'll try to use Selenium
'''

from selenium import webdriver
import time
import pickle

'''
driver = webdriver.Chrome()
driver.get("http://www.pythonscraping.com/pages/javascript/ajaxDemo.html")
time.sleep(3)
print(driver.find_element_by_id('content').text)
driver.close()
'''

def get_cookies(url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(30)
    driver.switch_to.window(driver.window_handles[1])
    pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
    driver.close()

def test_login(url):
    driver = webdriver.Chrome()
    cookies = pickle.load(open("cookies.pkl", "rb"))
    driver.get(url)
    for cookie in cookies:
        cookie_dict = {
            'domain': cookie.get('domain'),
            'httpOnly': cookie.get('httpOnly'),
            'name': cookie.get('name'),
            'path': cookie.get('path'),
            'secure': cookie.get('secure'),
            'value': cookie.get('value')
        }
        print(cookie_dict)
        driver.add_cookie(cookie_dict)
    driver.get(url)

def main():
    get_cookies("http://one.ccnu.edu.cn")
    test_login("http://xssw.ccnu.edu.cn/xgxt/stuPage.jsp")

main()