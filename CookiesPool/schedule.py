import time
from multiprocessing import process
from CookiesPool.config import *
from CookiesPool.api import app
from CookiesPool.tester import *

class Scheduler():
    @staticmethod
    def valid_cookie(cycle=5):
        while True:
            print('Cookies检测进程开始运行')
            pass

    @staticmethod
    def generator_cookie(cycle):
        print('Cookies生成进程开始运行')
        pass

    @staticmethod
    def api():
        print('API接口开始运行')
        pass

    def run(self):
        pass