#! /usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: wifi
@Created: 2023/2/25
"""


class Wifi:
    def __init__(self, device):
        self.device = device

    def enable(self):
        self.device.shell('svc wifi enable')

    def disable(self):
        self.device.shell('svc wifi disable')

    def connect(self):
        pass
