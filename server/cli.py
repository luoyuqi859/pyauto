#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: cli
@Created: 2023/3/4
"""
import argparse
import os
import shutil
import traceback

import pytest

from conf import settings
from utils import config
from utils.allure_fun import AllureDataCollect
from utils.dict import Dict
from utils.excel_fun import ErrorCaseExcel
from utils.lark_notify import FeiShuTalkChatBot
from utils.log import logger
from utils.model import NotificationType


def run(case=None):
    # 从配置文件中获取项目名称
    try:
        logger.info(
            f"""
                               _ooOoo_
                              o8888888o
                              88" . "88
                              (| -_- |)
                              O\  =  /O
                           ____/`---'\____
                         .'  \\|     |//  `.
                        /  \\|||  :  |||//  \
                       /  _||||| -:- |||||-  \
                       |   | \\\  -  /// |   |
                       | \_|  ''\---/''  |   |
                       \  .-\__  `-`  ___/-. /
                     ___`. .'  /--.--\  `. . __
                  ."" '<  `.___\_<|>_/___.'  >'"".
                 | | :  `- \`.;`\ _ /`;.`/ - ` : | |
                 \  \ `-.   \_ __\ /__ _/   .-` /  /
            ======`-.____`-.___\_____/___.-`____.-'======
                               `=---='
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                        开始执行{config.project_name}项目... 佛祖保佑       全部跑过
            """
        )
        settings.report_path.mkdir()
        args = ['--reruns=1', '--reruns-delay=2', "--count=1", "--random-order"]
        case_list = case.split(",")
        for i in case_list:
            args.append(i)

        # pytest.main(
        #     [f"{settings.repos_path}/lxl/test_xxx.py::test_xxx", f"{settings.repos_path}/lxl/test_xxx.py::test_xxx1",
        #      '--reruns=1', '--reruns-delay=2', "--count=1", "--random-order"])
        pytest.main(args)
        """
                   --reruns: 失败重跑次数
                   --count: 重复执行次数
                   -v: 显示错误位置以及错误的详细信息
                   -s: 等价于 pytest --capture=no 可以捕获print函数的输出
                   -q: 简化输出信息
                   -m: 运行指定标签的测试用例
                   -x: 一旦错误，则停止运行
                   --maxfail: 设置最大失败次数，当超出这个阈值时，则不会在执行测试用例
                    "--reruns=3", "--reruns-delay=2"
        """

    except Exception:
        # 如有异常，相关异常发送邮件
        logger.info(traceback.format_exc())
        raise


class ServiceProxy:
    def __init__(self):
        self.info = Dict(ip='127.0.0.1')
        description = 'PyAuto command line'
        self.parser = argparse.ArgumentParser(description=description, prog='PyAuto')


service = ServiceProxy()

parser = service.parser
parser.add_argument('--case', type=str)
args = parser.parse_args()
case = args.case
run(case)
