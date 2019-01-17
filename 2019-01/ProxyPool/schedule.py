import time

from tester import Tester
from getter import Getter
from api import app
from settings import *
from multiprocessing import Process

class Schedule():
    def schedule_tester(self, cycle=TESTER_CYCLE):
        tester = Tester()
        while True:
            print('测试器开始运行')
            tester.run()
            time.sleep(cycle)

    def schedule_getter(self, cycle=GETTER_CYCLE):
        getter = Getter()
        while True:
            print('开始获取代理')
            getter.run()
            time.sleep(cycle)

    def schedule_api(self):
        app.run(API_HOST, API_PORT)

    def run(self):
        print('代理池开始运行')
        if TESTER_ENABLE:
            tester_process = Process(target=self.schedule_tester)
            tester_process.start()

        if GETTER_ENABLE:
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()

        if API_ENABLE:
            api_process = Process(target=self.schedule_api)
            api_process.start()