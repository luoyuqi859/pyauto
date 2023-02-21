#!/usr/bin/env python
# -*- ecoding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: test_smple.py
@Created: 2023/2/20 13:50
"""
import logging

import pytest

from uiauto.android.device import AndroidDevice





# 测试类
# class TestAdd:

# 跳过用例
# def test_first(self, ):
#     pytest.skip('跳过')
#     assert add(3, 4) == 7
#
# # 异常用例
# def test_second(self, d: AndroidDevice):
#     assert add(-3, 4) == 1
#     raise Exception('异常')

# 成功用例
def test_three(device):
    device.assert_exist("抖音")
    # assert add(3, -4) == -1

def test_three_2(device):
    device.assert_exist("xxx")

def test_three_4(device):
    device.assert_exist("xxx")

def test_three_5(device):
    device.assert_exist("xxx")

# # 失败用例
# def test_four(self, d: AndroidDevice):
#     assert add(-3, -4) == 7

# def test_xxx(device: AndroidDevice):
#     device.d(resourceId="com.miui.home:id/icon_icon", description="ATX").click()


# if __name__ == '__main__':
#     pytest.main(["test_xxx"])
