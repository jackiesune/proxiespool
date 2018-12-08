TESTER_CYCLE=20
GETTER_CYCLE=60
TESTER_ENABLED=True
GETTER_ENABLED=False
API_ENABLED=True
API_HOST = '0.0.0.0'
API_PORT = 5555

import time
from multiprocessing import Process
from flaskp import app
from runget import Getter
from  aiohttptest import Tester

class Scheduler():
    def schedule_tester(self,cycle=TESTER_CYCLE):
        '''定时测试代理'''
        tester=Tester()
        while True:
            print('测试器开始工作')
            tester.run()
            print('测试结束')
            time.sleep(cycle)


    def schedule_getter(self,cycle=GETTER_CYCLE):
        getter=Getter()
        while True:
            print('开始抓取代理')
            getter.run()
            print('代理抓取结束')
            time.sleep(cycle)


    def schedule_api(self):
        '''开启api'''
    
        app.run(API_HOST,API_PORT)

    def run(self):
        print('代理池开始运行')
        if TESTER_ENABLED:
            tester_process=Process(target=self.schedule_tester)
            tester_process.start()
        if GETTER_ENABLED:
            getter_process=Process(target=self.schedule_getter)
            getter_process.start()

        if API_ENABLED:
            api_process=Process(target=self.schedule_api)
            api_process.start()

