#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: run.py
@Created: 2023/2/16 9:23
"""
import argparse
import asyncio
import concurrent
import os
import shutil
import time
from concurrent.futures import ProcessPoolExecutor
import pytest

from conf import settings
from pytest_plugins import CommonPlugin
from uiauto.android.pool import device_pool
from utils import config
from utils.allure_fun import AllureDataCollect
from utils.command import execute_command
from utils.excel_fun import ErrorCaseExcel
from utils.lark_notify import FeiShuTalkChatBot
from utils.log import logger
from utils.model import NotificationType


def pytest_run(d=None) -> None:
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
    pytest_args = [f'--alluredir={settings.report_tmp}', "--clean-alluredir"]
    if d:
        pytest_args.append(f"--cmdopt={d}")
    pytest_args.extend(config.pytest)
    if case:
        case_list = case.split(";")
        for i in case_list:
            pytest_args.append(i)
    pytest.main(pytest_args, plugins=[CommonPlugin()])
    execute_command(f"{settings.allure_bat} generate {settings.report_tmp} -o {settings.report_html} --clean")


async def env_file_move():
    shutil.copy(src=settings.root_path / "conf" / "categories.json", dst=settings.report_tmp)
    shutil.copy(src=settings.root_path / "conf" / "environment.properties", dst=settings.report_tmp)
    shutil.copy(src=settings.root_path / "conf" / "executor.json", dst=settings.report_tmp)
    shutil.copy(src=settings.root_path / "conf" / "openReport.bat", dst=settings.report_path)


async def excel_report() -> None:
    if config.excel_report:
        ErrorCaseExcel(settings.report_path).write_case()


async def notify() -> None:
    allure_data = AllureDataCollect(settings.report_path)
    data = allure_data.get_case_count()
    notification_mapping = {
        NotificationType.FEI_SHU.value: FeiShuTalkChatBot(data).post
    }
    if config.notification_type != NotificationType.DEFAULT.value:
        notification_mapping.get(config.notification_type)()


async def main(d=None):
    pytest_run(d)
    start_time = time.time()
    tasks = [
        asyncio.create_task(env_file_move()),
        asyncio.create_task(excel_report()),
        asyncio.create_task(notify())
    ]
    await asyncio.gather(*tasks)
    end_time = time.time()
    print("Execution time:", end_time - start_time)
    # folder_path = settings.project_path

    # # 获取文件夹中所有文件和文件夹的名称列表，并按照修改时间排序
    # items = os.listdir(folder_path)
    # items.sort(key=lambda x: os.path.getmtime(os.path.join(folder_path, x)))
    # last_folder_name = ''
    # # 查找最后一个文件夹的名称
    # for item in reversed(items):
    #     if os.path.isdir(os.path.join(folder_path, item)):
    #         last_folder_name = item
    #         break
    #
    # # 得到最后一次生成的文件夹路径
    # last_folder_path = folder_path / last_folder_name / "html"
    # # 启动子进程自动打开报告
    # cmd = f"{settings.allure_bat} open {settings.report_html} -p {settings.localhost_port}"
    # await asyncio.create_subprocess_shell(cmd)


def start(d=None) -> None:
    """启动入口"""
    try:
        asyncio.run(main(d))
    except KeyboardInterrupt:
        logger.info("Interrupt catched")


def startup():
    serials = list(device_pool.devices.keys())
    for device in device_pool.devices.values():
        device.minicap.install_minicap()

    if len(serials) > 1 and config.concurrent:
        with ProcessPoolExecutor() as executor:
            futures = [executor.submit(start, s) for s in serials]
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as exc:
                    print(f'Generated an exception: {exc}')
    else:
        start(serials)


if __name__ == '__main__':
    startup()
