#!/usr/bin/env python
# -*- ecoding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: ddd
@Created: 2023/2/21 17:42
"""

import uiautomator2 as u2

from uiauto.android.adb import ADB

serial = ADB().adb.serial
device = u2.Device(serial)
print(device.info)