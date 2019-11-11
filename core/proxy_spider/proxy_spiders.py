#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/11/11 上午11:43
# @Author : xiaowei
# @Site : 
# @File : proxy_spiders.py
# @Software: PyCharm

from core.proxy_spider.base_spider import BaseSpider
import requests


class XiCiSpider(BaseSpider):
    urls = ['https://www.xicidaili.com/nt/{}'.format(i) for i in range(1, 4)]
    group_xpath = '//*[@id="ip_list"]/tr[position()>1]'
    detail_xpath = {
        'ip': './td[2]/text()',
        'port': './td[3]/text()',
        'area': './td[4]/a/text()'.strip()
    }


class IP3366Spider(BaseSpider):
    urls = ['http://www.ip3366.net/free/?stype={}&page={}'.format(i, j) for i in range(1, 3) for j in range(1, 4)]
    group_xpath = '//*[@id="list"]/table/tbody/tr'
    detail_xpath = {
        'ip': './td[1]/text()',
        'port': './td[2]/text()',
        'area': './td[5]/text()'
    }


class KuaiDailiProxy(BaseSpider):
    urls = ['https://www.kuaidaili.com/free/{}/{}'.format(i, j) for i in list(['inha', 'intr']) for j in range(1, 6)]
    group_xpath = '//*[@id="list"]/table/tbody/tr'
    detail_xpath = {
        'ip': './td[1]/text()',
        'port': './td[2]/text()',
        'area': './td[5]/text()'
    }


class ProxyListPlusProxy(BaseSpider):
    urls = ['https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-{}'.format(i) for i in range(1, 2)]
    group_xpath = '//*[@id="page"]/table[2]/tr[position()>2]'
    detail_xpath = {
        'ip': './td[2]/text()',
        'port': './td[3]/text()',
        'area': './td[5]/text()'
    }


class A66IpProxy(BaseSpider):
    urls = ['http://www.66ip.cn/{}.html'.format(i) for i in range(1, 3)]
    group_xpath = '//*[@id="main"]/div/div[1]/table/tr[position()>1]'
    detail_xpath = {
        'ip': './td[1]/text()',
        'port': './td[2]/text()',
        'area': './td[3]/text()'
    }


if __name__ == '__main__':
    # proexies = XiCiSpider().get_proxies()
    # proexies = IP3366Spider().get_proxies()
    # proexies = KuaiDailiProxy().get_proxies()
    # proexies=ProxyListPlusProxy().get_proxies()
    proexies = A66IpProxy().get_proxies()
    # url = 'http://www.66ip.cn/2.html'
    # content = requests.get(url).content.decode("gb2312")
    # print(content)
    count = 0
    for proxy in proexies:
        count += 1
        print(proxy)

    print(count)
