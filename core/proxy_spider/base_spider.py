#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/11/11 上午9:15
# @Author : xiaowei
# @Site : 
# @File : base_spider.py
# @Software: PyCharm


import requests
import time
import random
from lxml import etree

from utils.http import get_user_agent
from domain import Proxy


class BaseSpider(object):
    # 代理ip列表
    urls = []
    # 分组xpath，获取包含代理ip信息标签列表的xpath
    group_xpath = ''
    # 组内xpath，获取代理ip详情信息的xapth，格式为{'ip':xxx,'port':xxx,'area':xxx}
    detail_xpath = {}

    def __init__(self, urls=[], group_xpath='', detail_xpath={}):
        if urls:
            self.urls = urls

        if group_xpath:
            self.group_xpath = group_xpath

        if detail_xpath:
            self.detail_xpath = detail_xpath

    def get_page_from_url(self, url):
        # 根据url发送请求，获取页面数据
        response = requests.get(url, headers=get_user_agent())
        time.sleep(random.uniform(1, 3))
        # print(response.content)
        return response.content

    def get_first_from_list(self, lis):
        return lis[0] if len(lis) != 0 else ""

    def get_proxies_from_page(self, page):
        # 解析页面，提取数据，封装为Proxy对象
        element = etree.HTML(page)
        # 获取包含代理信息ip的标签列表
        # print(element.xpath(self)
        trs = element.xpath(self.group_xpath)
        # print(trs)
        # 遍历trs，获取代理ip相关信息
        for tr in trs:
            ip = self.get_first_from_list(tr.xpath(self.detail_xpath['ip']))
            port = self.get_first_from_list(tr.xpath(self.detail_xpath['port']))
            area = self.get_first_from_list(tr.xpath(self.detail_xpath['area']))
            proxy = Proxy(ip, port, area=area)
            # 使用yield返回提取的数据
            yield proxy

    def get_proxies(self):
        # 对外提供一个获取代理IP的方法
        for url in self.urls:
            print(url)

            # 根据url发送请求，获取页面数据
            page = self.get_page_from_url(url)
            # 解析页面，提取数据，封装为Proxy对象
            proxies = self.get_proxies_from_page(page)
            yield from proxies


if __name__ == '__main__':
    config = {
        'urls': ['https://www.xicidaili.com/nt/{}'.format(i) for i in range(1, 4)],
        'group_xpath': '//*[@id="ip_list"]/tr',
        'detail_xpath': {
            'ip': '//*[@id="ip_list"]/tr[3]/td[2]/text()',
            'port': '//*[@id="ip_list"]/tr[3]/td[3]/text()',
            'area': '//*[@id="ip_list"]/tr[2]/td[4]/a/text()'.strip()
        }
    }
    s = BaseSpider(**config).get_proxies()
    for s in s:
        print(s)
