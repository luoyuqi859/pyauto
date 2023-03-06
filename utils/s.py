#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: s
@Created: 2023/2/27 11:00
"""

import re
from typing import Union

from utils.path_fun import Path


class Str(str):
    def __new__(cls, o, *args, **kwargs):  # 重写 __new__ 否则无法正常重写 __init__
        return super().__new__(cls, o)

    def ints(self):
        _list = re.compile(r'\d+').findall(self)
        return [int(n) for n in _list]

    def numbers(self):
        _list = re.compile(r'\d+(?:\.\d+)?').findall(self)
        return [float(n) for n in _list]

    def uncamel(self):
        """
        变量名风格转换：驼峰 --> 下划线
        """
        s1 = re.sub('([A-Z][a-z]+)(?=[A-Z]]?)', r'\1_', self)
        return s1.lower()

    def camel(self):
        """
        变量名风格转换：下划线 --> 驼峰
        """
        s1 = ''.join([s.title() if s else '_' for s in self.split('_')])
        return s1

    def startswith_any(self, prefixes: Union[list, tuple]):
        for prefix in prefixes:
            if self.startswith(prefix):
                return True
        return False

    def endswith_any(self, suffixes: Union[list, tuple]):
        for suffix in suffixes:
            if self.endswith(suffix):
                return True
        return False

    def sep(self, n=1):
        """
        生成器，用于将字符串按照指定数量分组

        list(sep('123456', 8)) >> ['123456']

        list(sep('13465782345', 4)) >> ['1346', '5782', '345']

        :param n:
        :return:
        """
        length = len(self)
        for i in range(0, length, n):
            if i > 0:
                yield self[i - n: i]
        yield self[length - (length % n or 4):]

    def path(self, relpath):
        return Path.abspath(relpath, self)

    @property
    def is_ip_address(self):
        m = re.match(r'.*(?:(?:\d+)\.){3}\d+(?::\d+)?.*', self)
        return m is not None
