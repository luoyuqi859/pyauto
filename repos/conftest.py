#!/usr/bin/env python
# -*- ecoding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: conftest.py
@Created: 2023/2/22 16:53
"""
import inspect
import os

import allure
import pytest

import uiautomator2 as u2

from uiauto.android.device import AndroidDevice
from utils.log import logger


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
        # for k, v in item.funcargs.items():
        #     if hasattr(v, 'driver'):
        #         pass
        device: AndroidDevice = item.funcargs.get("device", None)
        # 添加allure报告截图
        if device is not None:
            logger.warning("用例出错,即将截图")
            allure.attach(device.d.screenshot(format="base64"), "失败截图", allure.attachment_type.PNG)


# def pytest_assume_fail(lineno, entry):
#     """
#     assume 断言报错截图
#     """
#     print(entry)
#     for i in inspect.stack():
#         if os.path.split(i.filename)[1].startswith('test_'):
#             try:
#                 for k, v in i.frame.f_locals.items():
#                     if hasattr(v, 'driver'):
#                         attach_png(f'{TEST_PIC}/{int(time.time())}.png', f"失败截图_{int(time.time())}", v)
#                         break
#             except Exception:
#                 pass


@pytest.fixture(scope="session", params=None, autouse=True, ids=None, name=None)
def device():
    device = u2.connect()
    logger.info(device.info)
    logger.info("初始化设备成功")
    return AndroidDevice(device=device)
