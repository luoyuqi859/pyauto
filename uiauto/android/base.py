#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: base
@Created: 2023/2/20 17:01
"""

OFFLINE = 'offline'  # 离线
IDLE = 'idle'  # 空闲
ASSIGNED = 'assigned'  # 已分配
RUNNING = 'running'  # 执行中


class BaseDevice(dict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._status = None

    @property
    def id(self):
        raise NotImplementedError

    @property
    def status(self):
        return self._status

    def __getattr__(self, item):
        return self.get(item, None)

    def __eq__(self, other):
        return other and other.id == self.id

    def __hash__(self):
        return hash(self.id)


class DeviceError(Exception):
    """设备异常"""

    def __init__(self, device):
        self.device = device


class DeviceNotIdleError(DeviceError):
    """
    设备不空闲异常
    """


class DeviceNotFoundError(DeviceError):
    """
    设备未找到错误
    """
