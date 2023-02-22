#!/usr/bin/env python
# -*- ecoding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: test_xxx
@Created: 2023/2/22 11:07
"""
from uiauto.android.device import AndroidDevice


def test_350853(device: AndroidDevice):
    device.assert_exist("设置x")
