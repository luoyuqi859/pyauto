#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: test
@Created: 2023/3/10 15:53
"""
from repos.GM.keywords.gm_vehicle_sim import GMS
from uiauto.android.device import connect, AndroidDevice

u2 = connect()
d = AndroidDevice(device=u2)

d(content="Change PIN").assert_exist()
# d(text="Add / Remove Teen Driver Keys").assert_exist()
# d(text="View Report Card").assert_exist()
# d(text="Teen Driver Settings").assert_exist()
# d(text="Clear PIN and All Teen Driver Keys").assert_exist()
# d(text="Change PIN").assert_exist()

