#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: airplane
@Created: 2023/2/25
"""


class Airplane:
    """飞行模式"""

    def __init__(self, device):
        self.device = device

    def enable(self):
        self.device.shell('settings put global airplane_mode_on 1')

    def disable(self):
        self.device.shell('settings put global airplane_mode_on 0')

    @property
    def enabled(self):
        output = self.device.shell('settings get global airplane_mode_on')
        return output == '1'

    def switch(self):
        if self.enabled:
            self.disable()
            return False
        else:
            self.enable()
            return True