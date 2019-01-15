import requests


class Login():
    def __init__(self):
        self.headers = {
            'Host': 'account.ccnu.edu.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/70.0.3538.77 Safari/537.36',
            'Referer': 'https://account.ccnu.edu.cn/cas/login?service=http%3A%2F%2Fone.ccnu.edu.cn%2Fcas%2Flogin_portal'
        }
        self.post_url = 'https://account.ccnu.edu.cn/' \
                        'cas/login?service=http%3A%2F%2Fone.ccnu.edu.cn%2Fcas%2Flogin_portal'
        self.login_url = ''
        self.session = requests.Session()

    def login(self):
        post_data = {
            'username': 'username',
            'password': 'password',
            'lt': 'LT - 302644 - NeBq0fgp46HeWSlqaDGA6bYnPMCAhB - account.ccnu.edu.cn',
            'execution': 'e6s1',
            '_eventId': 'submit',
            'submit': '登录',
        }
        response = self.session.post(self.post_url, data=post_data, headers=self.headers)
        if response.status_code == 200:
            print(response.text)
        else:
            print('error')

if __name__ == '__main__':
    url = 'http://xssw.ccnu.edu.cn/xgxt/xsxx_xsgl.do?method=showPhoto&xh=2016211044'
    headers = {
        'Host': 'xssw.ccnu.edu.cn',
        'Referer': 'http: // xssw.ccnu.edu.cn / xgxt / loginatz.jsp',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                     'AppleWebKit/537.36 (KHTML, like Gecko) '
                     'Chrome/70.0.3538.77 Safari/537.36',
        'Cookie':'JSESSIONID=558DF7563368D87F1A5F336CF48972D4; '
                 'UM_distinctid=166c507dac2ee-0e64734c8cc5cd-9393265-e1000-166c507dac7116; '
                 'BIGipServerxg=592488640.20480.0000'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open('test.jpg', 'wb') as f:
            f.write(response.content)
            f.close()