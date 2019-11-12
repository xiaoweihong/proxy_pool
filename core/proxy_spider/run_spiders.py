#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/11/11 下午7:01
# @Author : xiaowei
# @Site : 
# @File : run_spiders.py
# @Software: PyCharm

import importlib
import schedule
from gevent import monkey

monkey.patch_all()
from gevent.pool import Pool

from settings import PROXY_SPIDERS
from core.proxy_validator.httpbin_validator import check_proxy
from utils.log import logger
from core.db.mongo_pool import MongoPool
from settings import RUN_SPIDERS_INTERVAL


class RunSpider(object):

    def __init__(self):
        self.mongo_pool = MongoPool()
        self.corutine_pool = Pool()

    def get_spider_from_settings(self):
        # 遍历配置文件，获取信息
        for spider in PROXY_SPIDERS:
            # 获取模块名 类名
            module_name, class_name = spider.rsplit('.', maxsplit=1)
            # 根据模块名导入类名
            module = importlib.import_module(module_name)
            # 根据类名，从模块中获取类
            cls = getattr(module, class_name)
            # 创建对象
            spider = cls()
            yield spider

    def run(self):
        spiders = self.get_spider_from_settings()
        for spider in spiders:
            # 通过协程池异步执行
            self.corutine_pool.apply_async(self.__execute_one_spider, args=(spider,))
        self.corutine_pool.join()

    # 处理一个爬虫的
    def __execute_one_spider(self, spider):
        try:
            for proxy in spider.get_proxies():
                proxy = check_proxy(proxy)
                if proxy.speed != -1:
                    self.mongo_pool.insert_one(proxy)

        except Exception as e:
            logger.error(e)

    @classmethod
    def start(self):
        rs = RunSpider()
        rs.run()
        schedule.every(RUN_SPIDERS_INTERVAL).hours.do(rs.run())
        while True:
            schedule.run_pending()


if __name__ == '__main__':
    RunSpider.start()
    # def test():
    #     print("hello")
    # schedule.every(5).seconds.do(test)
    # while True:
    #     schedule.run_pending()
