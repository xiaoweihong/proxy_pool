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
TIMEOUT=10

# mongo
MONGO_URL="mongodb://192.168.2.189:27017"