#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: base
@Created: 2023/2/20 17:01
"""
from uiauto.android import listener
from utils.check import Check
from loguru import logger

OFFLINE = 'offline'  # 离线
IDLE = 'idle'  # 空闲
ASSIGNED = 'assigned'  # 已分配
RUNNING = 'running'  # 执行中
RECORDING = 'recording'


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

    @status.setter
    def status(self, value):
        logger.debug(f'current device status: {self.status}, update to {value}')
        changed = self._status != value
        if self._status is None and value == IDLE:
            logger.debug(f'device {self.id} connect')
            listener.on_device_connected(self)
        elif self._status and value == OFFLINE and changed:
            logger.debug(f'device {self.id} disconnect')
            listener.on_device_disconnected(self)
        elif self._status == OFFLINE and value == IDLE:
            logger.debug(f'device {self.id} reconnect')
            listener.on_device_reconnected(self)
        elif self._status in [RUNNING, RECORDING] and value == IDLE:
            listener.on_device_idle(self)
        elif value == 'Authorized':
            pass
        self._status = value

    def assign(self, occupier):
        """
        分配设备
        :param occupier: 设备占用者
        :return:
        """
        self.occupier = occupier
        self.status = ASSIGNED

    def match(self, **kwargs):
        return Check(self).test(**kwargs)

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


class DeviceUnsubscribedError(DeviceError):
    """
    设备未订阅异常
    """


class DeviceNotIdleError(DeviceError):
    """
    设备不空闲异常
    """


class NoIdleDeviceError(DeviceError):
    """
    没有空闲设备异常，指有符合条件，但是暂不空闲
    """


class DeviceNotFoundError(DeviceError):
    """
    设备未找到错误
    """


class NoAvailableDeviceError(DeviceError):
    """
    没有合适的设备
    """
