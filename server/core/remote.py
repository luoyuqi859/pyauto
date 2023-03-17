#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: remote
@Created: 2023/3/16 15:05
"""
import traceback
from functools import wraps

import requests
from loguru import logger
from requests import HTTPError


def intercept(func):
    """
    http请求拦截器，用于为请求添加 token，如果token过期，则自动重新发起请求
    """

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.connected is False:
            return
        if not self.token:
            self.login_server()
        headers = {
            "token": self.token,
            # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            #               "(KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
            # "Accept": "application/json, text/javascript, */*; q=0.01",
            # "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            # "Accept-Encoding": "gzip, deflate",
            # "Content-Type": "application/json",
        }
        data = {
            **kwargs,
            "Owner": self.owner
        }
        res = func(self, *args, **data, headers=headers)
        if res.status_code not in [200, 201]:
            print(res.text)
        if 'ExpiredSignatureError' in res.text or res.status_code == 403:
            self.token = None
            return wrapper(*args, **kwargs)
        if not kwargs.get('verify'):
            res.raise_for_status()
        return res.json()

    return wrapper


class RemoteBase:
    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.owner = None
        self.token = None
        self.server_url = kwargs.get('address')
        self.username = kwargs.get('username')
        self.password = kwargs.get('password')
        self._connected = None

    @property
    def connected(self):
        return self._connected

    def login_server(self):
        pass


class Remote(RemoteBase):
    def login_server(self):
        """
        登录
        """
        try:
            url = f'{self.server_url}/api/base/login'
            res = requests.post(url, dict(Username=self.username, Password=self.password))
            res.raise_for_status()
            data = res.json().get('data')
            self.token = data.get('token')
            self.owner = data.get('user').get('nickName')
            self._connected = True
        except ConnectionError:
            self._connected = False
        except HTTPError:
            logger.error(traceback.format_exc())
            self._connected = False

    @intercept
    def register_host(self, **data):
        """
        注册执行主机
        """
        headers = data.pop('headers')
        return requests.post(url=f'{self.server_url}/api/host/register', data=data, headers=headers)

    @intercept
    def register_device(self, **data):
        """
        注册设备
        """
        headers = data.pop('headers')
        res_data = requests.post(url=f'{self.server_url}/api/device/register', data=data, headers=headers)
        return res_data


if __name__ == '__main__':
    remote = Remote(address="http://127.0.0.1:8888", username="luoyuqi", password="luoyuqi")
    remote.login_server()
