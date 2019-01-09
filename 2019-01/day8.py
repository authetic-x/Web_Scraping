'''
Here we'll learn how to handle the test from picture
'''

from PIL import Image
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

'''
#   对于一些有线条或不清晰的图片
#   可以先进行转灰度和二值化处理
image = Image.open("CheckCode.jpg")
#   转灰度
image = image.convert('L')
table = []
threshold = 127

for i in range(0, 256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)
image = image.point(table, '1')
image.show()
'''

EMAIL = '1019892846@qq.com'
PASSWORD = ''

class CrackGeetest():
    def __init__(self):
        self.email = EMAIL
        self.password = PASSWORD
        self.url = ''
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 20)

    def get_button(self):
        button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, '')))
        return button

    def get_position(self):
        pass