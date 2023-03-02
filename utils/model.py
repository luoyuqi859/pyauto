#!/usr/bin/env python
# -*- ecoding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: model
@Created: 2023/2/17 17:24
"""
import threading
from dataclasses import dataclass
from enum import Enum
from typing import Text, Union

from pydantic import BaseModel


class Webhook(BaseModel):
    webhook: Union[Text, None]


class Serial(BaseModel):
    serial: Union[Text, None]


class Pref(BaseModel):
    switch: bool
    package: Union[Text, None]


class NotificationType(Enum):
    """ 自动化通知方式 """
    DEFAULT = 0
    FEI_SHU = 1
    WECHAT = 2
    EMAIL = 3
    DING_TALK = 4


class Config(BaseModel):
    project_name: Text
    tester_name: Text
    lark: "Webhook"
    notification_type: int = 0
    excel_report: bool
    device: "Serial" = "auto"
    perf: "Pref"


@dataclass
class TestMetrics:
    """ 用例执行数据 """
    passed: int
    failed: int
    broken: int
    skipped: int
    total: int
    pass_rate: float
    time: Text


# 记录运行时需要共享的全局变量
class RuntimeData():
    # 记录pid变更前的pid
    old_pid = None
    packages = None
    package_save_path = None
    start_time = None
    exit_event = threading.Event()
    top_dir = None
    config_dic = {}
