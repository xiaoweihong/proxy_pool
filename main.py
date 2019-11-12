#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/11/8 上午9:59
# @Author : xiaowei
# @Site : 
# @File : main.py
# @Software: PyCharm

from multiprocessing import Process

from core.proxy_spider.run_spiders import RunSpider
from core.proxy_test import ProxyTester
from core.proxy_api import ProxyApi


def run():
    # 定义一个列表用于存储要启动的进程
    process_list = []
    # 创建启动爬虫
    process_list.append(Process(target=RunSpider.start))
    process_list.append(Process(target=ProxyTester.start))
    process_list.append(Process(target=ProxyApi.start))

    for process in process_list:
        process.daemon = True
        process.start()

    for process in process_list:
        process.join()


if __name__ == '__main__':
    run()
