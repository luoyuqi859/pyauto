#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: accessory
@Created: 2023/2/25
"""
import re


class Accessory:
    """Android配件"""

    def __init__(self, device):
        self.device = device

    @property
    def sdcard_serial(self):
        if 'sdcard_serial' not in self.device.info:
            output = self.device.shell('cd storage;ls -al')
            p = re.compile(r'\d+-\d+-\d+ \d{2}:\d+ (\S+)', re.DOTALL)
            result = p.findall(output, re.DOTALL)
            if result:
                for item in result:
                    if item not in ['.', '..', 'emulated', 'self']:
                        self.device.info['sdcard_serial'] = item
                        return item
        return self.device.info.get('sdcard_serial')

    @property
    def phone_numbers(self):
        """
        获取手机号码

        :return: 号码 list
        """

        def get_number(code):
            info = self.device.shell(f'service call iphonesubinfo {code}')
            p = re.compile(r'((?:\+\.)|(?:\d\.))', re.DOTALL)
            return ''.join([s[0] for s in p.findall(info)])

        numbers = set()
        for i in [15, 16, 17]:
            number = get_number(i)
            if number:
                numbers.add(number)
        return list(numbers)