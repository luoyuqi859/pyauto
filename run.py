#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: run.py
@Created: 2023/2/16 9:23
"""
import argparse
import asyncio
import os
import shutil

import pytest

from conf import settings
from pytest_plugins import CommonPlugin
from utils import config
from utils.allure_fun import AllureDataCollect
from utils.excel_fun import ErrorCaseExcel
from utils.lark_notify import FeiShuTalkChatBot
from utils.log import logger
from utils.model import NotificationType


async def pytest_run():
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
    parser = argparse.ArgumentParser(description="PyAuto command line", prog='PyAuto')
    parser.add_argument('--case', type=str)
    args = parser.parse_args()
    case = args.case
    pytest_args = [f'--alluredir={settings.report_tmp}', "--clean-alluredir"] + config.pytest
    case_list = case.split(";") if case else []
    for i in case_list:
        pytest_args.append(i)
    pytest.main(pytest_args, plugins=[CommonPlugin()])
    os.system(f"{settings.allure_bat} generate {settings.report_tmp} -o {settings.report_html} --clean")


async def env_file_move():
    shutil.copy(src=settings.root_path / "conf" / "categories.json", dst=settings.report_tmp)
    shutil.copy(src=settings.root_path / "conf" / "environment.properties", dst=settings.report_tmp)
    shutil.copy(src=settings.root_path / "conf" / "executor.json", dst=settings.report_tmp)
    shutil.copy(src=settings.root_path / "utils" / "openReport.bat", dst=settings.report_path)


async def excel_report():
    if config.excel_report:
        ErrorCaseExcel(settings.report_path).write_case()


async def notify():
    allure_data = AllureDataCollect(settings.report_path)
    data = allure_data.get_case_count()
    notification_mapping = {
        NotificationType.FEI_SHU.value: FeiShuTalkChatBot(data).post
    }
    if config.notification_type != NotificationType.DEFAULT.value:
        notification_mapping.get(config.notification_type)()


async def main():
    await pytest_run()
    await asyncio.create_task(env_file_move())
    await asyncio.create_task(excel_report())
    await asyncio.create_task(notify())
    # 程序运行之后，自动启动报告，如果不想启动报告，可注释这段代码,
    os.system(f"{settings.allure_bat} open {settings.report_html} -p {settings.localhost_port}")


if __name__ == '__main__':
    asyncio.run(main())
