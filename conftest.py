#!/usr/bin/env python
# -*- ecoding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: conftest
@Created: 2023/2/16 19:23
"""
import time

import allure
import pytest

from conf import settings
from uiauto import uninstall_atx
from uiauto.android.device import AndroidDevice, connect
from uiauto.perf.cpu import CpuMonitor
from uiauto.perf.flow import TrafficMonitor
from uiauto.perf.fps import FPSMonitor
from uiauto.perf.logcat import LogcatMonitor
from uiauto.perf.memory import MemMonitor
from uiauto.perf.power import PowerMonitor
from uiauto.perf.pref_data_fun import PrefDataFun
from uiauto.perf.thread_num import ThreadNumMonitor
from utils.log import logger
from utils import config
from utils.time_fun import timeoperator


@pytest.fixture(scope='session', autouse=True)
def on_test_start():
    logger.info(f"开始测试")


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """获取到每个用例的执行结果"""
    # 获取钩子方法的调用结果

    out = yield
    res = out.get_result()
    if res.when == "call":
        logger.info(f"用例: {res}")
        logger.info(f"用例描述: {item.function.__doc__}")
        logger.info(f"用例执行阶段: {res.when}")
        logger.info(f"测试结果：{res.outcome}")
        logger.info(f"用例耗时：{res.duration}")
    logger.info("**************************************")


# @pytest.fixture(scope="session", autouse=True)
# def fixture_setup_teardown():
#     logger.info("前置操作：setup")
#     yield
#     logger.info("后置操作：teardown")


def pytest_collection_modifyitems(session, items):
    """改变用例顺序"""
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")
    num = len(items)
    logger.info(f"收集到的测试用例：{items}, 数量:{num}")


def pytest_terminal_summary(terminalreporter):
    """
    收集测试结果
    """
    _TOTAL = terminalreporter._numcollected  # 总数
    _PASSED = len(terminalreporter.stats.get('passed', []))  # 通过
    _FAILED = len(terminalreporter.stats.get('failed', []))  # 失败
    _ERROR = len(terminalreporter.stats.get('error', []))  # 错误
    _SKIP = len(terminalreporter.stats.get('skipped', []))  # 跳过
    _RERUN = len(terminalreporter.stats.get('rerun', []))  # 失败重跑总次数
    _TIMES = round(time.time() - terminalreporter._sessionstarttime, 2)  # 测试用时，保留两位
    logger.info(f"用例总数: {_TOTAL}")
    logger.success(f"成功用例数: {_PASSED}")
    logger.error(f"失败用例数: {_FAILED}")
    logger.error(f"异常用例数: {_ERROR}")
    logger.error(f"跳过用例数: {_SKIP}")
    logger.warning(f"失败重跑总次数: {_RERUN}")
    total_time = timeoperator.s_to_hms(_TIMES)
    logger.info(f"用例执行时长: {total_time}")
    try:
        _RATE = _PASSED / _TOTAL * 100
        logger.info("用例成功率: %.2f" % _RATE + " %")
    except ZeroDivisionError:
        logger.info("用例成功率: 0.00 %")


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
    return d


# @pytest.fixture(scope="session", params=None, autouse=True, ids=None, name=None)
# def uninstall():
#     """测试完毕卸载ATX"""
#     yield



@pytest.fixture(scope="session", autouse=True)
def performance(d_obj):
    """
    统计设备cpu情况
    @return:
    """
    logger.info(d_obj.d.info)
    logger.info("初始化设备成功")
    if config.perf.switch:
        settings.perf_path.mkdir()
        app = config.perf.package
        logger.info(f"即将开启设备监控,app: {app}")
        frequency = 5
        t = settings.current_time
        cpu_monitor = CpuMonitor(packages=[app], interval=frequency, path=settings.perf_path)
        logcat_monitor = LogcatMonitor(path=settings.perf_path)
        # traffic_monitor = TrafficMonitor(packages=[app], interval=frequency, path=settings.perf_path)
        fps_monitor = FPSMonitor(package_name=app, frequency=frequency, path=settings.perf_path)
        mem_monitor = MemMonitor(packages=[app], interval=frequency, path=settings.perf_path)
        # power_monitor = PowerMonitor(interval=frequency, path=settings.perf_path)
        thread_num_monitor = ThreadNumMonitor(packagename=app, interval=frequency, path=settings.perf_path)

        cpu_monitor.start(t)
        # traffic_monitor.start(t)
        fps_monitor.start(t)
        mem_monitor.start(t)
        # power_monitor.start(t)
        thread_num_monitor.start(t)
        logcat_monitor.start(t)\

        yield
        cpu_monitor.stop()
        # traffic_monitor.stop()
        fps_monitor.stop()
        mem_monitor.stop()
        # power_monitor.stop()
        thread_num_monitor.stop()
        logcat_monitor.stop()
        try:
            d = PrefDataFun()
            d.all_handle(path=settings.perf_path)
        except Exception as e:
            logger.error(e)
    else:
        logger.info("没有开启性能监控功能")
    # 调试期间可以注释掉，最后批量执行建议最后删掉ATX
    # yield
    # uninstall_atx()

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
