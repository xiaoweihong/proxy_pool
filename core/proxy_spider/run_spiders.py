#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/11/11 下午7:01
# @Author : xiaowei
# @Site : 
# @File : run_spiders.py
# @Software: PyCharm

import importlib

from settings import PROXY_SPIDERS
from core.proxy_validator.httpbin_validator import check_proxy
from utils.log import logger


class RunSpider(object):

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
            for proxy in spider.get_proxies():
                s = check_proxy(proxy)
                if s.speed != -1:
                    logger.info(s)


if __name__ == '__main__':
    RunSpider().run()
