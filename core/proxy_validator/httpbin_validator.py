#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/11/8 上午11:58
# @Author : xiaowei
# @Site : 
# @File : httpbin_validator.py
# @Software: PyCharm

import requests
import time

from utils.http import get_user_agent
from utils.log import logger
from settings import TIMEOUT
from domain import Proxy


def check_proxy(proxy):
    """
    用于检查指定代理ip的响应速度,匿名程度,支持的协议
    :param proxies:
    :return:
    """

    # 准备代理ip
    proxies = {
        "http": "http://{}:{}".format(proxy.ip, proxy.port),
        "https": "https://{}:{}".format(proxy.ip, proxy.port),
    }
    # 测试该代理ip
    http, http_nick_type, http_speed = __check_http_proxies(proxies)
    https, https_nick_type, https_speed = __check_http_proxies(proxies, is_http=False)

    #
    if http and https:
        proxy.protocl = 2
        proxy.nick_type = http_nick_type
        proxy.speed = http_speed
    elif http:
        proxy.protocl = 0
        proxy.nick_type = http_nick_type
        proxy.speed = http_speed
    elif https:
        proxy.protocl = 1
        proxy.nick_type = https_nick_type
        proxy.speed = https_speed
    else:
        proxy.protocl = -1
        proxy.nick_type = -1
        proxy.speed = -1
    return proxy


def __check_http_proxies(proxies, is_http=True):
    # 代理IP的匿名程度 高匿 0，匿名 1，透明 2
    nick_type = -1
    # 连接速度
    speed = -1
    if is_http:
        test_url = "http://httpbin.org/get"
    else:
        test_url = "https://httpbin.org/get"
    try:
        # 获取开始时间
        start = time.time()
        # 发送请求，获取响应数据
        response = requests.get(test_url, proxies=proxies, headers=get_user_agent(), timeout=TIMEOUT)
        if response.ok:
            # 响应速度
            speed = round(time.time() - start, 2)
            # 匿名程度
            #  获取origin
            origin = response.json()['origin']
            # print(response.json())
            #  获取响应中的proxy-connection，匿名代理
            try:
                proxy_connection = origin.get("Proxy-Connection", None)
            except Exception as e:
                logger.info("代理不是高匿。。。")
                proxy_connection = 1
            if '.' in origin:
                nick_type = 2
            elif proxy_connection:
                nick_type = 1
            else:
                nick_type = 0

            return True, nick_type, speed
        else:
            return False, nick_type, speed
    except Exception as e:
        logger.error("{} 链接失败".format(proxies['http']))
        return False, nick_type, speed


if __name__ == '__main__':
    proxy = Proxy(ip="222.223.182.66", port="8000")
    # print(proxy)
    print(check_proxy(proxy))
