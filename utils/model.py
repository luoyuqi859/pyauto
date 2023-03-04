#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
    frequency: int


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
    retry: int
