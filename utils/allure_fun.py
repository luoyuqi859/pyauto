#!/usr/bin/env python
# -*- ecoding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: allure_fun
@Created: 2023/2/17 16:32
"""

import json
import time

from typing import List, Text

from conf import settings
from utils.model import TestMetrics
from utils.path_fun import get_all_files, Path


class AllureDataCollect:
    """allure 报告数据收集"""

    def __init__(self, report_path):
        self.report_path = report_path
        self.data_path = Path(report_path) / "html" / "data" / "test-cases"
        self.summary_path = Path(report_path) / "html" / "widgets" / "summary.json"

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
        data = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(test_case['time'].get("start", None) / 1000))
        return data

    def get_case_stop(self, test_case):
        """
        收集测试用例结束时间
        @return:
        """
        data = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(test_case['time'].get("stop", None) / 1000))
        return data

    def get_case_time(self, test_case):
        """
        获取用例运行时长
        @param test_case:
        @return:
        """
        data = time.strftime('%H:%M:%S', time.gmtime(round(test_case['time'].get("duration", None) / 1000, 2)))
        return data

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
            run_case_data['time'] = _time if run_case_data['total'] == 0 else time.strftime('%H:%M:%S', time.gmtime(
                round(_time['duration'] / 1000, 2)))
            return TestMetrics(**run_case_data)
        except FileNotFoundError as exc:
            raise FileNotFoundError(
                "程序中检查到您未生成allure报告，"
                "通常可能导致的原因是allure环境未配置正确，"
                "详情可查看如下博客内容："
                "https://blog.csdn.net/weixin_43865008/article/details/124332793"
            ) from exc


if __name__ == '__main__':
    root = settings.root_path()
    path = root / "report" / "2023-02-20-09-39-36"
    allure_data = AllureDataCollect(path)
    allure_data.get_failed_case()
    pass
