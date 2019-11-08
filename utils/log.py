#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/11/8 上午10:08
# @Author : xiaowei
# @Site : 
# @File : log.py
# @Software: PyCharm

import sys
import logging

from settings import LOG_FMT, LOG_DATEFMT, LOG_FILENAME, LOG_LEVEL


class Logger(object):
    def __init__(self):
        # 获取一个logger对象
        self._logger = logging.getLogger()
        # 设置format对象
        self.formatter = logging.Formatter(fmt=LOG_FMT, datefmt=LOG_DATEFMT)
        # 设置日志输出
        # 文件日志模式
        self._logger.addHandler(self._get_file_handler(LOG_FILENAME))
        # 设置终端日志模式
        self._logger.addHandler(self._get_console_handler())
        # 设置日志等级
        self._logger.setLevel(LOG_LEVEL)

    def _get_file_handler(self, filename):
        """
        返回一个文件日志handler
        :param filename:
        :return:
        """
        filehandler = logging.FileHandler(filename=filename, encoding='utf-8')

        filehandler.setFormatter(self.formatter)
        return filehandler

    def _get_console_handler(self):
        """
        返回一个输出到终端日志handler
        :return:
        """
        # 1. 获取一个输出到终端日志handler
        console_handler = logging.StreamHandler(sys.stdout)
        # 2. 设置日志格式
        console_handler.setFormatter(self.formatter)
        # 3. 返回handler
        return console_handler

    @property
    def logger(self):
        return self._logger
logger = Logger().logger

if __name__ == '__main__':


    logger.debug("wqeq")
    logger.error("error")
