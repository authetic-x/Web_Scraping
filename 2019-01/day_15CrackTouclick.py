import time
from io import BytesIO

import requests
from hashlib import md5

from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class Chaojiying():
    def __init__(self, username, password, soft_id):
        self.username = username
        self.password = md5(password.encode('utf-8')).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def post_pic(self, im, codetype):
        params = {
            'codetypa':codetype,
        }
        params.update(self.base_params)
        files = {'userfile':('ccc.jpg', im)}
        r = requests.post('', data=params, files=files, headers=self.headers)
        return r.json()

    def report_error(self, im_id):
        params = {
            'id':im_id,
        }
        params.update(self.base_params)
        r = requests.post('', data=params, headers=self.headers)
        return r.json()

EMAIL = ''
PASSWORD = ''
CHAOJIYING_USERNAME = 'authetic'
CHAOJIYING_PASSWORD = ''
CHAOJIYING_SOFT_ID = ''
CHAOJIYING_KIID = 9102

class CrackTouClick():
    def __init__(self):
        self.url = ''
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 20)
        self.email = EMAIL
        self.password = PASSWORD
        self.chaojiying = Chaojiying(CHAOJIYING_USERNAME, CHAOJIYING_PASSWORD,
                                     CHAOJIYING_SOFT_ID)

    def open(self):
        self.browser.get(self.url)
        email = self.wait.until(EC.presence_of_element_located((By.ID, 'email')))
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'password')))
        email.send_keys(self.email)
        password.send_keys(self.password)

    def get_touclick_button(self):
        button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, '')))
        return button

    def get_touclick_element(self):
        element = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, '')))
        return element

    def get_position(self):
        element = self.get_touclick_element()
        time.sleep(2)
        location = element.location
        size = element.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], \
                                            location['x'] + size['width']
        return (top, bottom, left, right)

    def get_touclick_image(self, name='captcha.png'):
        top, bottom, left, right = self.get_position()
        print('验证码位置 ', top, bottom, left, right)
        screenshot = self.get_screenshot()
        captcha = screenshot.crop((left, bottom, left, right))
        captcha.save(name)
        return captcha

    def get_screenshot(self):
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot

    def get_points(self, captcha_result):
        groups = captcha_result.get('pic_str').split('|')
        locations = [[int(number) for number in group.split(',')] for group in groups]
        return locations

    def touch_click_word(self, locations):
        for location in locations:
            print(location)
            ActionChains(self.browser).move_to_element_with_offset(self.get_touclick_element(),
                                                                   locations[0], locations[1]).click().perform()
            time.sleep(1)
