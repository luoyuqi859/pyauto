#!/usr/bin/env python
# -*- ecoding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: conftest
@Created: 2023/2/17 10:44
"""
import os
from contextvars import Context

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
    rep = outcome.get_result()
    # 仅仅获取用例call 执行结果是失败的情况, 不包含 setup/teardown
    if rep.when == "call" and rep.failed:
        mode = "a" if os.path.exists("failures") else "w"
        with open("failures", mode) as f:
            # let's also access a fixture for the fun of it
            if "tmpdir" in item.fixturenames:
                extra = " (%s)" % item.funcargs["tmpdir"]
            else:
                extra = ""
            f.write(rep.nodeid + extra + "\n")

        device: AndroidDevice = item.funcargs.get("device", None)
        # 添加allure报告截图
        if device is not None:
            with allure.step('失败截图...'):
                allure.attach(device.d.screenshot(format="base64"), "失败截图", allure.attachment_type.PNG)


# def pytest_generate_tests(metafunc):
#     if "param" in metafunc.fixturenames:
#         metafunc.parametrize("param", metafunc.module.case_data, ids=metafunc.module.case_id, scope="function")


@pytest.fixture(scope="session", params=None, autouse=True, ids=None, name=None)
def device():
    device = u2.connect()
    logger.info("初始化设备成功")
    return AndroidDevice(device=device)
