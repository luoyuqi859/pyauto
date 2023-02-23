#!/usr/bin/env python
# -*- ecoding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: run.py
@Created: 2023/2/16 9:23
"""
import os
import shutil
import traceback

import pytest

from conf import settings
from utils import config
from utils.allure_fun import AllureDataCollect
from utils.excel_fun import ErrorCaseExcel
from utils.lark_notify import FeiShuTalkChatBot
from utils.log import logger
from utils.model import NotificationType


def run():
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
        tmp = settings.report_path / "tmp"
        html = settings.report_path / "html"
        pytest.main(
            ['--reruns=1', '--reruns-delay=2', "--count=1", "--random-order",
             f'--alluredir={tmp}',
             "--clean-alluredir"])
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
        shutil.copy(src=settings.root_path / "conf" / "categories.json", dst=tmp)
        shutil.copy(src=settings.root_path / "conf" / "environment.properties", dst=tmp)
        shutil.copy(src=settings.root_path / "conf" / "executor.json", dst=tmp)
        os.system(f"{settings.allure_bat} generate {tmp} -o {html} --clean")
        logger.info(f"report save path:{settings.report_path}")
        allure_data = AllureDataCollect(settings.report_path)
        data = allure_data.get_case_count()
        shutil.copy(src=settings.root_path / "utils" / "openReport.bat", dst=settings.report_path)
        notification_mapping = {
            NotificationType.FEI_SHU.value: FeiShuTalkChatBot(data).post
        }
        if config.notification_type != NotificationType.DEFAULT.value:
            notification_mapping.get(config.notification_type)()

        if config.excel_report:
            ErrorCaseExcel(settings.report_path).write_case()
        # 程序运行之后，自动启动报告，如果不想启动报告，可注释这段代码
        os.system(f"{settings.allure_bat} open {html} -p 9999")

    except Exception:
        # 如有异常，相关异常发送邮件
        logger.info(traceback.format_exc())
        raise


if __name__ == '__main__':
    run()
