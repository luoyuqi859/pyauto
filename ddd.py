#!/usr/bin/env python
# -*- ecoding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: ddd
@Created: 2023/2/21 17:42
"""

import uiautomator2 as u2

d = u2.connect()
d(text="飞书").click()
