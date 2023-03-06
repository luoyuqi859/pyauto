#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: config
@Created: 2023/2/20 10:58
"""
from utils import config
from utils.path_fun import Path
from utils.time_fun import timeoperator

root_path = Path(__file__).parent.parent
uiauto_path = root_path / "uiauto"
allure_bat = root_path / 'libs' / 'allure' / "bin" / "allure"
current_time = timeoperator.strftime_now("%Y-%m-%d-%H-%M-%S")
report_path = root_path / "report" / config.project_name / current_time
repos_path = root_path / "repos"
server_path = root_path / "server"
perf_path = report_path / "perf"  # 性能数据路径
ocr_cls = root_path / 'libs' / 'ocr' / 'cls'
ocr_det = root_path / 'libs' / 'ocr' / 'det'
ocr_rec = root_path / 'libs' / 'ocr' / 'rec'
minicap_path = root_path / 'libs' / 'minicap'
minitouch_path = root_path / 'libs' / 'minitouch'

# u2
ELEMENT_WAIT_TIMEOUT = 5  # 元素默认等待时间
FORCE_STEP_INTERVAL_BEFORE = 0.2  # 测试操作前强制间隔时间
FORCE_STEP_INTERVAL_AFTER = 0.2  # 测试操作后强制间隔时间
WAIT_FOR_DEVICE_TIMEOUT = 70
MAX_SWIPE_STEPS = 55  # 滑动一屏最多需要的步数，如果把屏幕分成十等份，那么滑动0.1的距离需要5.5步
LONG_CLICK_DURATION = 1  # 长按时长
MIN_SWIPE = 100

