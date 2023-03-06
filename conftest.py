#! /usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: conftest
@Created: 2023/2/16 19:23
"""

import allure
import pytest

from conf import settings
from uiauto.android.device import AndroidDevice, connect
from uiauto.perf.monitors import monitors
from uiauto.perf.pref_data_fun import PrefDataFun
from utils.log import logger
from utils import config


@pytest.fixture(scope='session', autouse=True)
def on_test_start():
    logger.info(f"开始测试")


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
            allure.attach(device.d.screenshot(format='base64'), "失败截图", allure.attachment_type.PNG)


@pytest.fixture(scope="session", params=None, autouse=True, ids=None, name=None)
def d_obj():
    u2 = connect()
    d = AndroidDevice(device=u2)
    d.minicap.install_minicap()
    yield d
    # 调试过程中可以注释删除ATX功能
    uninstall_atx(d)


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
def performance(d_obj):
    """
    统计设备cpu情况
    @return:
    """
    logger.info(d_obj.d.info)
    logger.info("初始化设备成功")
    if config.perf.switch:
        monitors.run()
        yield
        monitors.stop()
        try:
            d = PrefDataFun()
            d.all_handle(path=settings.perf_path)
        except Exception as e:
            logger.error(e)
    else:
        logger.info("没有开启性能监控功能")
    yield

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
