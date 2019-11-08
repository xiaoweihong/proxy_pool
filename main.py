#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/11/8 上午9:59
# @Author : xiaowei
# @Site : 
# @File : main.py
# @Software: PyCharm
from utils.log import logger
from utils.http import get_user_agent
from lxml import etree
import requests
from core.proxy_validator.httpbin_validator import check_proxy
from domain import Proxy

content = requests.get("https://www.xicidaili.com/nt/1", headers=get_user_agent()).text
html = etree.HTML(content)
trs = html.xpath("//tr")
iplist = list()
for tr in trs:
    ipinfo = dict()
    tds = tr.xpath("./td")
    if tds:
        ip = tds[1].xpath("./text()")[0]
        port = tds[2].xpath("./text()")[0]
        # print(ip, port)
        ipinfo['ip'] = ip
        ipinfo['port'] = port

        proxy = check_proxy(Proxy(ip=ip, port=port))
        print(proxy)
        logger.info(proxy)
        iplist.append(ipinfo)
# print(iplist)
