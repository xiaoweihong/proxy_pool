#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/11/12 下午2:42
# @Author : xiaowei
# @Site : 
# @File : proxy_api.py
# @Software: PyCharm

from flask import Flask, request

from core.db.mongo_pool import MongoPool
from settings import PROXIES_MAX_COUNT

import json


class ProxyApi(object):
    def __init__(self):
        # 初始化flask服务
        self.app = Flask(__name__)
        self.mongo_pool = MongoPool()

        @self.app.route('/random')
        def random():
            protocol = request.args.get("protocol")
            domain = request.args.get("domain")
            proxy = self.mongo_pool.get_random_proxy(protocl=protocol, domain=domain)
            if proxy:
                return "{}://{}:{}".format(protocol, proxy.ip, proxy.port)
            return "test"

        @self.app.route('/proxies')
        def proxies():
            # 获取的协议
            protocol = request.args.get("protocol")
            # 域名
            domain = request.args.get("domain")
            proxies = self.mongo_pool.get_proxies(protocl=protocol, domain=domain, count=PROXIES_MAX_COUNT)
            proxies_list = [proxy.__dict__ for proxy in proxies]
            return json.dumps(proxies_list)

        @self.app.route('/disable_domain')
        def disable_domain():
            ip = request.args.get('ip')
            domain = request.args.get("domain")
            if ip is None:
                return "ip不能为空"
            if domain is None:
                return "domain不能为空"
            self.mongo_pool.disable_domain(ip, domain)
            return "{} 禁用{} 成功".format(ip, domain)

    def run(self):
        self.app.run('0.0.0.0', port=17777)

    @classmethod
    def start(cls):
        proxyApi = cls()
        proxyApi.run()


if __name__ == '__main__':
    ProxyApi.start()
