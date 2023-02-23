#!/usr/bin/env python
# -*- ecoding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: test_xxx
@Created: 2023/2/22 11:07
"""
import allure

from uiauto.android.device import AndroidDevice
from utils.allure_fun import compose


@compose(feature="微医主站", story="首页", title='主入口下方文案校验')
def test_350853(device: AndroidDevice):
    with allure.step("xxxxxx"):
        device.assert_exist("设置x")
