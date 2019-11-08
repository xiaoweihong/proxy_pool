#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/11/8 下午2:19
# @Author : xiaowei
# @Site : 
# @File : mongo_pool.py
# @Software: PyCharm

import pymongo
import random
from pymongo import MongoClient

from settings import MONGO_URL
from utils.log import logger
from domain import Proxy


class MongoPool(object):

    def __init__(self):
        # 建立数据库连接
        self.client = MongoClient(MONGO_URL)
        # 获取操作的集合
        self.proxies = self.client['proxy_pool']['proxies']

    def __del__(self):
        # 关闭数据库连接
        self.client.close()

    def insert_one(self, proxy):
        """
        插入代理数据
        使用proxy.ip作为主键_id插入
        :param proxy:
        :return:
        """
        count = self.proxies.count({"_id": proxy.ip})
        if count == 0:
            dic = proxy.__dict__
            dic['_id'] = proxy.ip
            self.proxies.insert_one(dic)
            logger.info("{} 插入成功".format(proxy.ip))
        else:
            logger.warn("{} 已经存在".format(proxy.ip))

    def update_one(self, proxy):
        """
        更新的功能
        :param proxy:
        :return:
        """
        self.proxies.update_one({"_id": proxy.ip}, {"$set": proxy.__dict__})
        logger.info("{} 更新成功".format(proxy.ip))

    def delete_one(self, proxy):
        """
        删除代理
        :param proxy:
        :return:
        """
        count = self.proxies.count({"_id": proxy.ip})
        if count:
            self.proxies.delete_one({"_id": proxy.ip})
            logger.info("{} 删除成功".format(proxy.ip))
        else:
            logger.info("{} 不存在".format(proxy.ip))

    def find_all(self):
        cursor = self.proxies.find()
        for item in cursor:
            item.pop("_id")
            proxy = Proxy(**item)
            yield proxy

    def find(self, conditions={}, count=0):
        """
        根据条件查询
        :param conditions: 查询添加字典
        :param count:       查询的数量
        :return:            返回满足要求的代理列表
        """
        cursor = self.proxies.find(conditions, limit=count).sort([
            ("score", pymongo.DESCENDING), ("speed", pymongo.ASCENDING)
        ])
        # 准备列表用来存储查询出来的数据
        proxy_list = list()
        for item in cursor:
            item.pop("_id")
            proxy = Proxy(**item)
            proxy_list.append(proxy)
        return proxy_list

    def get_proxies(self, protocl=None, domain=None, nick_type=2, count=0):
        """
        返回满足条件的代理
        :param protocl:     支持的协议
        :param domain:      域名
        :param nick_type:   类型
        :param count:       限制获取的数量(more获取所有)
        :return:
        """
        # 定义查询条件
        condations = {"nick_type": nick_type}
        # 根据协议指定查询条件
        if protocl is None:
            # 返回两种类型都支持的数据
            condations["protocl"] = 2
        elif protocl.lower() == "http":
            condations["protocl"] = {"$in": [0, 2]}
        elif protocl.lower() == "https":
            condations["protocl"] = {"$in": [1, 2]}
        else:
            condations["protocl"] = -1

        if domain:
            condations["disable_domains"] = {"$nin": [domain]}
        print(condations)

        return self.find(condations, count=count)

    def get_random_proxy(self, protocl=None, domain=None, nick_type=2, count=0):
        """
        随机返回一个代理
        :param protocl:
        :param domain:
        :param nick_type:
        :param count:
        :return:
        """
        proxy_list = self.get_proxies(protocl=protocl, domain=domain, nick_type=nick_type, count=count)
        return random.choice(proxy_list)

    def disable_domain(self, ip, domain):
        """
        把域名添加到指定ip的disable_domain中
        :param ip:
        :param domain:
        :return:
        """
        count = self.proxies.count({"_id": ip, "disable_domains": domain})
        if count == 0:
            self.proxies.update_one({"_id": ip}, {"$push": {"disable_domains": domain}})
            logger.info("{} 添加成功".format(domain))
            return True
        else:
            logger.info("{} 已经添加过,请勿重复添加".format(domain))
            return False


if __name__ == '__main__':
    proxy = Proxy("192.168.100.118", "10801", score=10)
    proxy2 = Proxy("192.168.100.128", "10801", score=30, protocl=1, nick_type=2)
    proxy1 = Proxy("192.168.100.119", "1080")
    # MongoPool().insert_one(proxy)
    # MongoPool().update_one(proxy=proxy2)
    # MongoPool().delete_one(proxy)
    # result = MongoPool().find_all()
    # for i in result:
    #     print(i)

    # result = MongoPool().find({"port": '10801'})
    # result = MongoPool().find({'nick_type': 2, 'protocl': {'$in': ['1', '2']}})
    #
    # for i in result:
    #     print(i)
    # s = MongoPool().get_proxies(protocl="https")
    # for i in s:
    #     print(i)
    # s = MongoPool().get_random_proxy(protocl="https")
    # print(s)

    MongoPool().disable_domain("192.168.100.118", "baidu.com")
