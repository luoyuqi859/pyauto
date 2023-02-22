#!/usr/bin/env python
# -*- coding: utf-8 -*-
# --------------------------------------------------------------
# ProjectName: HmdUIAutomator
# Author: gentliu
# CreateTime: 2022/1/4 11:19
# File Name: test
# Description:
# --------------------------------------------------------------
import logging
import re
import time

import adbutils

import uiautomator2 as u2
from uiautomator2 import Initer


def get_cont(prompt, result):
    total_re = r'%s(?P<count>\d+)' % prompt
    search = re.search(total_re, result)
    count = search.group("count")
    print("%s%s\n" % (prompt, count))
    return count


if __name__ == '__main__':
    for device in adbutils.adb.iter_device():
        init = Initer(device, loglevel=logging.DEBUG)
        init.install()

    serial = "PT19655DA1192500053"
    d = u2.connect(serial)
    while True:
        info_result = d.shell(['dumpsys', 'gfxinfo', 'com.android.systemui']).output
        get_cont("Total attached Views : ", info_result)
        time.sleep(2)
