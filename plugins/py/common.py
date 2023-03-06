#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: common
@Created: 2023/3/6 13:41
"""
import time

import pytest

from utils.log import logger
from utils.time_fun import timeoperator


class CommonPlugin(object):

    @pytest.hookimpl(hookwrapper=True, tryfirst=True)
    def pytest_runtest_makereport(self, item, call):
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

    def pytest_collection_modifyitems(self, session, items):
        """改变用例顺序"""
        for item in items:
            item.name = item.name.encode('utf-8').decode('unicode-escape')
            item._nodeid = item.nodeid.encode('utf-8').decode('unicode-escape')
        num = len(items)
        logger.info(f"收集到的测试用例：{items}, 数量:{num}")

    def pytest_terminal_summary(self, terminalreporter):
        """
        收集测试结果
        """
        _TOTAL = terminalreporter._numcollected  # 总数
        _PASSED = (len([i for i in terminalreporter.stats.get('passed', []) if i.when == 'call']))  # 通过
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
