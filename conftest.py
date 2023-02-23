#!/usr/bin/env python
# -*- ecoding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: conftest
@Created: 2023/2/16 19:23
"""
import time

import pytest

from utils.log import logger


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
    logger.info(f"收集到的测试用例：{items}")


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
    logger.info(f"用例执行时长: {_TIMES}")
    try:
        _RATE = _PASSED / _TOTAL * 100
        logger.info("用例成功率: %.2f" % _RATE + " %")
    except ZeroDivisionError:
        logger.info("用例成功率: 0.00 %")


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
