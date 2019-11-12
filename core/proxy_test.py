#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/11/12 下午1:11
# @Author : xiaowei
# @Site : 
# @File : proxy_test.py
# @Software: PyCharm

from gevent import monkey

monkey.patch_all()
from gevent.pool import Pool
from queue import Queue
import schedule
from core.db.mongo_pool import MongoPool
from core.proxy_validator.httpbin_validator import check_proxy

from settings import TEST_PROXY_ASYNC_COUNT, MAX_SCORE, TEST_PROXY_INTERVAL


class ProxyTester(object):
    def __init__(self):
        self.mongo_pool = MongoPool()
        self.coroutine_pool = Pool()
        self.queue = Queue()

    def __check_callback(self, temp):
        self.coroutine_pool.apply_async(self.__check_one_proxy, callback=self.__check_callback)

    def run(self):
        # 获取所有代理ip
        proxies = self.mongo_pool.find_all()
        for proxy in proxies:
            # 把要检测的代理放到队列中
            self.queue.put(proxy)
        for i in range(TEST_PROXY_ASYNC_COUNT):
            self.coroutine_pool.apply_async(self.__check_one_proxy, callback=self.__check_callback)

        # 当前线程等待队列的完成
        self.queue.join()

    def __check_one_proxy(self):
        # 检查代理的可用性
        proxy = self.queue.get()
        proxy = check_proxy(proxy)
        if proxy.speed == -1:
            proxy.score -= 1
            if proxy.score == 0:
                self.mongo_pool.delete_one(proxy)
            else:
                self.mongo_pool.update_one(proxy)
        else:
            proxy.score = MAX_SCORE
            self.mongo_pool.update_one(proxy)
        self.queue.task_done()

    @classmethod
    def start(cls):
        proxy_tester = cls()
        proxy_tester.run()
        schedule.every(TEST_PROXY_INTERVAL).minutes.do(proxy_tester.run)
        while True:
            schedule.run_pending()


if __name__ == '__main__':
    ProxyTester.start()
