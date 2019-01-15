import requests
from pyquery import PyQuery as pq

class Login():
    def __init__(self):
        self.headers = {
            'Referer':'https://github.com/',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/70.0.3538.77 Safari/537.36',
            'Host':'github.com'
        }
        self.login_url = 'https://github.com/login'
        self.post_url = 'https://github.com/session'
        self.logined_url = 'https://github.com/settings/profile'
        self.session = requests.Session()

    def token(self):
        response = self.session.get(self.login_url, headers=self.headers)
        doc = pq(response.text)
        input = doc('#login > form > input[type="hidden"]:nth-child(2)')
        return input.attr('value')

    def login(self, email, password):
        post_data = {
            'commit': 'Sign in',
            'utf8': '✓',
            'authenticity_token': self.token(),
            'login': email,
            'password': password
        }
        response = self.session.post(self.post_url, data=post_data,
                                    headers = self.headers)
        if response.status_code == 200:
            self.dynamics(response.text)
        else:
            print('some error happened', response.status_code)

        response = self.session.get(self.logined_url, headers = self.headers)
        if response.status_code == 200:
            self.dynamics(response.text)
        else:
            print('some error happened', response.status_code)

    def dynamics(self, html):
        doc = pq(html)
        news = doc('.dashboard > .news > .watch_started').items()
        for new in news:
            title = new('.d-flex.flex-items-baseline')
            print(title.text())

    def profile(self, html):
        pass

if __name__ == '__main__':
    login = Login()
    login.login(email='username', password='password')