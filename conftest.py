#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: conftest
@Created: 2023/2/16 19:23
"""
import ast
import io

import allure
import pytest

from conf import settings
from uiauto.android.device import AndroidDevice
from uiauto.android.pool import device_pool
from uiauto.perf.monitors import monitors
from uiauto.perf.pref_data_fun import PrefDataFun
from loguru import logger
from utils import config


def pytest_addoption(parser):
    parser.addoption("--cmdopt", action="store", default="device_info", help=None)


@pytest.fixture(scope="session")
def cmd_opt(request):
    return request.config.getoption("--cmdopt")


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
        logger.warning("用例出错,即将截图")
        d_obj = item.funcargs.get("d_obj", None)
        devices = d_obj if isinstance(d_obj, list) else [d_obj]
        if devices is not None:
            for device in devices:
                buffer = io.BytesIO()
                screenshot = device.d.screenshot()
                screenshot.convert("RGB").save(buffer, format='PNG')
                allure.attach(buffer.getvalue(), "失败截图", allure.attachment_type.PNG)


@pytest.fixture(scope="session")
def d_obj(cmd_opt):
    """设备对象"""
    opt = ast.literal_eval(cmd_opt) if cmd_opt.__contains__("[") else cmd_opt
    serial = opt if isinstance(opt, list) else [opt]
    devices = []
    for i in serial:
        device: AndroidDevice = device_pool.find_available_device(serial=i)
        logger.info(device.d.info)
        logger.info("初始化设备成功")
        devices.append(device)

    if len(devices) == 1:
        yield devices[0]
        uninstall_atx(devices[0])
    else:
        yield devices
        for d in devices:
            uninstall_atx(d)


def uninstall_atx(d: AndroidDevice):
    d.adb_fp.adb.shell("/data/local/tmp/atx-agent server --stop")
    d.adb_fp.adb.shell("rm /data/local/tmp/atx-agent")
    logger.info("atx-agent stopped and removed")
    d.adb_fp.adb.shell("rm /data/local/tmp/minicap")
    d.adb_fp.adb.shell("rm /data/local/tmp/minicap.so")
    d.adb_fp.adb.shell("rm /data/local/tmp/minitouch")
    logger.info("minicap, minitouch removed")
    d.adb_fp.adb.shell("pm uninstall com.github.uiautomator")
    d.adb_fp.adb.shell("pm uninstall com.github.uiautomator.test")
    logger.info("com.github.uiautomator uninstalled, all done !!!")


@pytest.fixture(scope="session", autouse=True)
def performance(cmd_opt):
    """
    统计设备cpu情况
    @return:
    """
    if not config.perf.switch:
        logger.info("没有开启性能监控功能")
        yield
    else:
        opt = ast.literal_eval(cmd_opt) if cmd_opt.__contains__("[") else cmd_opt
        serial = opt if isinstance(opt, list) else [opt]
        for i in serial:
            path = settings.perf_path / i
            monitors.run(serial=i, path=path)
        yield
        monitors.stop()
        try:
            for i in serial:
                path = settings.perf_path / i
                pref = PrefDataFun()
                pref.all_handle(path=path)
        except Exception as e:
            logger.error(e)
