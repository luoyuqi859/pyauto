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


# 实现了项目的主要逻辑
class PyAutoRun:
    @staticmethod
    def pytest_run(d=None) -> None:
        logger.info(f"开始执行{config.project_name}项目... 佛祖保佑       全部跑过")
        pytest_args = [f'--alluredir={settings.report_tmp}', "--clean-alluredir"]
        if d:
            pytest_args.append(f"--cmdopt={d}")
        pytest_args.extend(config.pytest)
        pytest.main(pytest_args, plugins=[CommonPlugin()])
        execute_command(f"{settings.allure_bat} generate {settings.report_tmp} -o {settings.report_html} --clean")

    @staticmethod
    async def env_file_move():
        shutil.copy(src=settings.root_path / "conf" / "categories.json", dst=settings.report_tmp)
        shutil.copy(src=settings.root_path / "conf" / "environment.properties", dst=settings.report_tmp)
        shutil.copy(src=settings.root_path / "conf" / "executor.json", dst=settings.report_tmp)
        shutil.copy(src=settings.root_path / "conf" / "openReport.bat", dst=settings.report_path)

    @staticmethod
    async def excel_report() -> None:
        if config.excel_report:
            ErrorCaseExcel(settings.report_path).write_case()

    @staticmethod
    async def notify() -> None:
        allure_data = AllureDataCollect(settings.report_path)
        data = allure_data.get_case_count()
        notification_mapping = {
            NotificationType.FEI_SHU.value: FeiShuTalkChatBot(data).post
        }
        if config.notification_type != NotificationType.DEFAULT.value:
            notification_mapping.get(config.notification_type)()

    @staticmethod
    async def main(d=None):
        PyAutoRun.pytest_run(d)
        start_time = time.time()
        tasks = [
            asyncio.create_task(PyAutoRun.env_file_move()),
            asyncio.create_task(PyAutoRun.excel_report()),
            asyncio.create_task(PyAutoRun.notify())
        ]
        await asyncio.gather(*tasks, return_exceptions=True)
        end_time = time.time()
        logger.info(f"Execution time: {end_time - start_time}")
        # # 启动子进程自动打开报告
        cmd = f"{settings.allure_bat} open {settings.report_html} -p {settings.localhost_port}"
        await asyncio.create_subprocess_shell(cmd)

    @staticmethod
    def init_arguments():
        parser = argparse.ArgumentParser(description='PyAuto command line')
        parser.add_argument('-c', '--case', dest='case',
                            default=None, required=False,
                            help='测试用例路径,依据pytest风格')

        parser.add_argument('-s', '--serial', dest='serial',
                            default=None, required=False,
                            help='设备序列号')

        return parser.parse_args()

    @staticmethod
    def async_start(d=None) -> None:
        try:
            asyncio.run(PyAutoRun.main(d))
        except KeyboardInterrupt:
            logger.info("Interrupt catched")

    @staticmethod
    def startup():
        args = PyAutoRun.init_arguments()
        logger.info(args.serial)
        serials = args.serial or list(device_pool.devices.keys())
        for device in device_pool.devices.values():
            device.minicap.install_minicap()

        if len(serials) > 1 and config.concurrent:
            with ProcessPoolExecutor() as executor:
                futures = [executor.submit(PyAutoRun.async_start, s) for s in serials]
                for future in concurrent.futures.as_completed(futures):
                    try:
                        future.result()
                    except Exception as exc:
                        print(f'Generated an exception: {exc}')
        else:
            PyAutoRun.async_start(serials)


if __name__ == '__main__':
    PyAutoRun.startup()
