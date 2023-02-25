#!/usr/bin/env python
# -*- ecoding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: conftest.py
@Created: 2023/2/22 16:53
"""

import uiautomator2 as u2

from uiauto.android.adb import ADB
from uiauto.android.device import AndroidDevice
from utils.log import logger
import allure
import pytest


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    '''
    获取每个用例状态的钩子函数
    :param item:
    :param call:
    :return:
    '''
    # 获取钩子方法的调用结果
    outcome = yield
    res = outcome.get_result()
    if res.outcome in ['failed', 'error']:
        device: AndroidDevice = item.funcargs.get("d_obj", None)
        # 添加allure报告截图
        if device is not None:
            logger.warning("用例出错,即将截图")
            allure.attach(device.d.screenshot(format="base64"), "失败截图", allure.attachment_type.PNG)


@pytest.fixture(scope="session", params=None, autouse=True, ids=None, name=None)
def d_obj():

    serial = ADB().adb.serial
    device = u2.Device(serial)
    # device = u2.connect()
    logger.info(device.info)
    logger.info("初始化设备成功")
    return AndroidDevice(device=device)
