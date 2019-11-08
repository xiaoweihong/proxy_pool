#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/11/8 上午9:59
# @Author : xiaowei
# @Site : 
# @File : domain.py
# @Software: PyCharm

from settings import MAX_SCORE


class Proxy(object):

    def __init__(self, ip=None, port=None, protocl=-1, nick_type=-1, speed=-1, area=None, score=MAX_SCORE,
                 disable_domains=[]):
        """

        :param ip:              ip地址
        :param port:            端口
        :param protocl:         协议 http 0,https 1 http/https 2
        :param nick_type:       代理IP的匿名程度 高匿 0，匿名 1，透明 2
        :param speed:           连接速度
        :param area:            区域
        :param score:           代理ip的评分
        :param disable_domains: 不可用域名列表，某些ip在某些域名下不可用
        """
        self.ip = ip
        self.port = port
        self.protocl = protocl
        self.nick_type = nick_type
        self.speed = speed
        self.area = area
        self.score = score
        self.disable_domains = disable_domains

    # 重写返回数据字符串
    def __str__(self):
        return str(self.__dict__)
