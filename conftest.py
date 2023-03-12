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
        for args, obj in item.funcargs.items():
            if isinstance(obj, AndroidDevice):
                logger.warning("用例出错,即将截图")
                buffer = io.BytesIO()
                screenshot = obj.d.screenshot()
                screenshot.convert("RGB").save(buffer, format='PNG')
                allure.attach(buffer.getvalue(), "失败截图", allure.attachment_type.PNG)


@pytest.fixture(scope="session")
def d_obj(cmd_opt):
    """设备对象，支持多进程并发执行"""
    serial = cmd_opt
    device: AndroidDevice = device_pool.find_available_device(serial)
    device.minicap.install_minicap()
    logger.info(device.d.info)
    logger.info("初始化设备成功")
    yield device
    # 调试过程中可以注释删除ATX功能
    uninstall_atx(device)


@pytest.fixture(scope="session")
def d1():
    """设备对象"""
    device: AndroidDevice = device_pool.find_available_device()
    device.minicap.install_minicap()
    logger.info(device.d.info)
    logger.info("初始化设备成功")
    yield device
    # 调试过程中可以注释删除ATX功能
    uninstall_atx(device)


@pytest.fixture(scope="session")
def d2():
    """设备对象"""
    device: AndroidDevice = device_pool.find_available_device()
    device.minicap.install_minicap()
    logger.info(device.d.info)
    logger.info("初始化设备成功")
    yield device
    # 调试过程中可以注释删除ATX功能
    uninstall_atx(device)


def uninstall_atx(d_obj: AndroidDevice):
    d_obj.adb_fp.adb.shell("/data/local/tmp/atx-agent server --stop")
    d_obj.adb_fp.adb.shell("rm /data/local/tmp/atx-agent")
    logger.info("atx-agent stopped and removed")
    d_obj.adb_fp.adb.shell("rm /data/local/tmp/minicap")
    d_obj.adb_fp.adb.shell("rm /data/local/tmp/minicap.so")
    d_obj.adb_fp.adb.shell("rm /data/local/tmp/minitouch")
    logger.info("minicap, minitouch removed")
    d_obj.adb_fp.adb.shell("pm uninstall com.github.uiautomator")
    d_obj.adb_fp.adb.shell("pm uninstall com.github.uiautomator.test")
    logger.info("com.github.uiautomator uninstalled, all done !!!")


@pytest.fixture(scope="session", autouse=True)
def performance():
    """
    统计设备cpu情况
    @return:
    """
    if not config.perf.switch:
        logger.info("没有开启性能监控功能")
        yield
    else:
        monitors.run()
        yield
        monitors.stop()
        try:
            from uiauto.android.adb import ADB
            adb = ADB()
            adb_devices = {item[0]: item[1] for item in adb.adb.devices()}
            for serial, _ in adb_devices.items():
                pref = PrefDataFun()
                pref.all_handle(path=settings.perf_path / serial)
        except Exception as e:
            logger.error(e)

# def pytest_report_teststatus(report, config):
#     """自定义测试结果"""
#     if report.when == 'call' and report.passed:
#         return report.outcome, '√', 'passed'
#     if report.when == 'call' and report.failed:
#         return report.outcome, 'x', 'failed'
#     if report.when == 'setup' and report.failed:
#         return report.outcome, '0', 'error'
#     if report.when == 'teardown' and report.failed:
#         return report.outcome, '1', 'error'
#     if report.skipped:
#         return report.outcome, '/', 'skipped'

# def pytest_generate_tests(metafunc):
#     if "param" in metafunc.fixturenames:
#         metafunc.parametrize("param", metafunc.module.case_data, ids=metafunc.module.case_id, scope="function")


# @pytest.mark.optionalhook
# def pytest_metadata(metadata):
#     """访问元数据"""
#     pass
