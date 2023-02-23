#!/usr/bin/env python
# -*- ecoding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: config
@Created: 2023/2/20 10:58
"""
from utils import config
from utils.path_fun import Path
from utils.time_fun import timeoperator

root_path = Path(__file__).parent.parent
allure_bat = root_path / 'libs' / 'allure' / "bin" / "allure"
current_time = timeoperator.strftime_now("%Y-%m-%d-%H-%M-%S")
report_path = root_path / "report" / config.project_name / current_time

# Android
ELEMENT_WAIT_TIMEOUT = 5  # 元素默认等待时间
FORCE_STEP_INTERVAL_BEFORE = 0.5  # 测试操作前强制间隔时间
FORCE_STEP_INTERVAL_AFTER = 0.5  # 测试操作后强制间隔时间
WAIT_FOR_DEVICE_TIMEOUT = 70
