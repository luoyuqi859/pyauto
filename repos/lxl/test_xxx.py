#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: test_xxx
@Created: 2023/3/11
"""
import time


# def test_1(d_obj):
#     d_obj[0].press("home")
#     d_obj[1].press("home")
#     assert 1 == 2

def test_2(d_obj):
    d_obj.press("home")
    d_obj.swipe.down.until_exists(text="xxxx")


class TestXXX():

    def test_123123(self):
        pass
