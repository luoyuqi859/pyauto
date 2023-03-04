#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: bt
@Created: 2023/2/25
"""

class Bluetooth:
    """
    蓝牙
    """
    def __init__(self, device):
        self.device = device

    def enable(self):
        """
        启用蓝牙
        :return:
        """
        self.device.shell('svc bluetooth enable')  # 可能不成功

    def disable(self):
        """
        禁用蓝牙
        :return:
        """
        self.device.shell('svc bluetooth disable')

    @property
    def enabled(self):
        """
        蓝牙是否启用
        :return:
        """
        output = self.device.shell('settings get global bluetooth_on')
        return output == '1'

    def switch(self):
        """
        切换蓝牙状态
        :return:
        """
        if self.enabled:
            self.disable()
        else:
            self.enable()
