#! /usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: prop
@Created: 2023/2/25
"""
import re
from typing import Union


class Prop:
    def __init__(self, device):
        self.device = device
        self._props = {}

    def __getattr__(self, item):
        return self[item]

    def __getitem__(self, item):
        if item not in self._props:
            self._props[item] = self.device.shell(f'getprop {item}')
        return self._props[item]

    def __call__(self, name=None) -> Union[str, dict]:
        """
        获取指定属性，如果没有指定，则获取所有
        :param name:
        :return:
        """
        if name:
            return self[name]
        else:
            output = self.device.shell('getprop')
            self._props = {item[0]: item[1] for item in re.findall(r'\[(.+?)\]: \[(.+?)\]', output, re.DOTALL)}
            return self._props

