'''
Get someone's head portrait on CCNU website
'''

import os
import requests
from requests.exceptions import RequestException

class GetPortrait():
    def __init__(self):
        self.headers = {
            'Host': 'xssw.ccnu.edu.cn',
            'Referer': 'http: // xssw.ccnu.edu.cn / xgxt / loginatz.jsp',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/70.0.3538.77 Safari/537.36',
            'Cookie': 'JSESSIONID=FBEDA0CA9ABC9DF2B7E237EA27AF92C1; '
                      'UM_distinctid=166c507dac2ee-0e64734c8cc5cd-9393265-e1000-166c507dac7116; '
                      'BIGipServerxg=592488640.20480.0000'
        }
        self.base_url = 'http://xssw.ccnu.edu.cn/xgxt/xsxx_xsgl.do?method=showPhoto&xh='

    def download(self, content, number):
        if not os.path.exists('d:\\HeadPortrait'):
            os.makedirs('d:\\HeadPortrait')
        with open('d:\\HeadPortrait\\%s.jpg' % number, 'wb') as f:
            print('成功写入头像', number)
            f.write(content)
            f.close()

    def get_content(self, number):
        try:
            response = requests.get(self.base_url + number, headers=self.headers)
            self.download(response.content, number)
        except RequestException:
            print('获取图片错误')

    def get_it(self):
        for i in range(0, 100):
            number = '2016211' + str(i).zfill(3)
            self.get_content(number)

if __name__ == '__main__':
    test = GetPortrait()
    test.get_it()