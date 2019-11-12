#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/11/8 上午9:59
# @Author : xiaowei
# @Site : 
# @File : settings.py
# @Software: PyCharm
import logging

MAX_SCORE = 50

# 日志的配置信息
LOG_LEVEL = logging.INFO
LOG_FMT = '%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s: %(message)s'
LOG_DATEFMT = '%Y-%m-%d %H:%M:%S'
LOG_FILENAME = 'log.log'

# 超时时间
TIMEOUT = 5

# mongo
MONGO_URL = "mongodb://192.168.2.189:27017"

# 爬虫信息
PROXY_SPIDERS = {
    'core.proxy_spider.proxy_spiders.A66IpProxy',
    'core.proxy_spider.proxy_spiders.IP3366Spider',
    'core.proxy_spider.proxy_spiders.KuaiDailiProxy',
    'core.proxy_spider.proxy_spiders.ProxyListPlusProxy',
    'core.proxy_spider.proxy_spiders.XiCiSpider',
}
# 定时任务运行间隔
RUN_SPIDERS_INTERVAL = 2

# 检测代理异步任务的数量
TEST_PROXY_ASYNC_COUNT = 10

# 检测代理定时任务运行间隔
TEST_PROXY_INTERVAL = 2

# 获取的代理ip最大数量，值越小可用性越高
PROXIES_MAX_COUNT = 50
