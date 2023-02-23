#!/usr/bin/env python
# -*- ecoding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: allure_fun
@Created: 2023/2/17 16:32
"""
import builtins
import json
import time

from typing import List, Text

import allure
import pytest

from utils.log import logger
from utils.model import TestMetrics
from utils.path_fun import get_all_files, Path
from utils.time_fun import timeoperator


class AllureDataCollect:
    """allure 报告数据收集"""

    def __init__(self, path):
        self.path = path
        self.data_path = self.path / "html" / "data" / "test-cases"
        self.summary_path = self.path / "html" / "widgets" / "summary.json"

    def get_testcases(self) -> List:
        """ 获取所有 allure 报告中执行用例的情况"""
        # 将所有数据都收集到files中
        files = []
        for i in get_all_files(self.data_path):
            with open(i, 'r', encoding='utf-8') as file:
                date = json.load(file)
                files.append(date)

        return files

    def get_failed_case(self) -> List:
        """ 获取到所有失败的用例标题和用例代码路径"""
        error_case = []
        for i in self.get_testcases():
            if i['status'] == 'failed' or i['status'] == 'broken':
                error_case.append(i)
        return error_case

    def get_failed_cases_detail(self) -> Text:
        """ 返回所有失败的测试用例相关内容 """
        date = self.get_failed_case()
        values = ""
        # 判断有失败用例，则返回内容
        if len(date) >= 1:
            values = "失败用例:\n"
            values += "        **********************************\n"
            for i in date:
                values += "        " + i[0] + ":" + i[1] + "\n"
        return values

    def get_uid(self, test_case):
        """
        获取 allure 报告中的 uid
        @param test_case:
        @return:
        """
        uid = test_case['uid']
        return uid

    def get_case_name(self, test_case):
        """
        收集测试用例名称
        @return:
        """
        name = test_case['name']
        return name

    def get_case_start(self, test_case):
        """
        收集测试用例开始时间
        @return:
        """
        data = int(test_case['time'].get("start", None))
        return timeoperator.strftime_now("%Y-%m-%d %H:%M:%S", data / 1000)

    def get_case_stop(self, test_case):
        """
        收集测试用例结束时间
        @return:
        """
        data = int(test_case['time'].get("stop", None))
        return timeoperator.strftime_now("%Y-%m-%d %H:%M:%S", data / 1000)

    def get_case_time(self, test_case):
        """
        获取用例运行时长
        @param test_case:
        @return:
        """
        data = test_case['time'].get("duration", None) / 1000
        return timeoperator.s_to_hms(data)

    def get_case_full_name(self, test_case):
        """
        收集测试用例完整路径
        @return:
        """
        name = test_case['fullName']
        return name

    def get_case_status(self, test_case):
        """
        收集测试用例状态
        @return:
        """
        name = test_case['status']
        return name

    def get_case_status_trace(self, test_case):
        """
        收集测试用例trace
        @return:
        """
        name = test_case['statusTrace']
        return name

    def get_case_count(self) -> "TestMetrics":
        """ 统计用例数量 """
        try:
            with open(self.summary_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            _case_count = data['statistic']
            _time = data['time']
            keep_keys = {"passed", "failed", "broken", "skipped", "total"}
            run_case_data = {k: v for k, v in data['statistic'].items() if k in keep_keys}
            # 判断运行用例总数大于0
            if _case_count["total"] > 0:
                # 计算用例成功率
                run_case_data["pass_rate"] = round(
                    (_case_count["passed"] + _case_count["skipped"]) / _case_count["total"] * 100, 2
                )
            else:
                # 如果未运行用例，则成功率为 0.0
                run_case_data["pass_rate"] = 0.0
            # 收集用例运行时长
            run_case_data['time'] = _time if run_case_data['total'] == 0 else timeoperator.s_to_hms(
                _time['duration'] / 1000)
            return TestMetrics(**run_case_data)
        except FileNotFoundError as exc:
            raise FileNotFoundError(
                "程序中检查到您未生成allure报告，"
                "通常可能导致的原因是allure环境未配置正确，"
                "详情可查看如下博客内容："
                "https://blog.csdn.net/weixin_43865008/article/details/124332793"
            ) from exc


def compose(**kwargs):
    """
    将头部ALlure装饰器进行封装
    可以采用：
        feature='模块名称'
        story='用户故事'
        title='用例标题'
        testcase='测试用例链接地址'
        severity='用例等级(blocker、critical、normal、minor、trivial)'
        link='链接'
        testcase=("url", "xx测试用例")
        issue=('bug地址', 'bug名称')
    的方式入参数
    :param kwargs:
    :return:
    """

    def deco(f):
        builtins.__dict__.update({'allure': allure})
        # 失败重跑
        if kwargs.get("reruns"):
            f = pytest.mark.flaky(
                reruns=kwargs.get("reruns", 2),  # 默认共执行2次
                reruns_delay=kwargs.get("reruns_delay", 2)  # 默认等待5秒
            )(f)
            kwargs.pop("reruns")
            if kwargs.get("reruns_delay"):
                kwargs.pop("reruns_delay")
        _kwargs = [('allure.' + key, value) for key, value in kwargs.items()]
        for allurefunc, param in reversed(_kwargs):
            if param:
                if isinstance(param, tuple):
                    f = eval(allurefunc)(*param)(f)
                else:
                    f = eval(allurefunc)(param)(f)
            else:
                f = eval(allurefunc)(f)
        return f

    return deco


def attach_text(body, name):
    """
    将text放在allure报告上
    :param body: 内容
    :param name: 标题
    :return:
    """
    try:
        allure.attach(body=str(body), name=str(name), attachment_type=allure.attachment_type.TEXT)
        logger.info(f'存放文字 {name}:{body} 成功！')
    except Exception as e:
        logger.error(f'存放文字失败 {name}:{body}！:{e}')
