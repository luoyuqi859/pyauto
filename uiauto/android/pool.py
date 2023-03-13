#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: pool
@Created: 2023/3/11
"""
import threading

from uiauto.android.adb import adb
from uiauto.android.base import IDLE, ASSIGNED, NoAvailableDeviceError, OFFLINE
from uiauto.android.device import AndroidDevice, connect
from loguru import logger


class DevicePool:
    """设备池"""
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self):
        self.thread_id = None
        self.devices = {}
        self.device_injection()
        self._lock = threading.Lock()
        self._event = threading.Event()
        self._event.set()
        self._working = False


    @property
    def working(self):
        return self._working

    def device_injection(self):
        if not self.devices:
            adb_devices = {item[0]: item[1] for item in adb.devices() if item[1] != OFFLINE}
            for serial, _ in adb_devices.items():
                u2 = connect(serial)
                device = AndroidDevice(device=u2)
                self.devices[serial] = device
                device.status = IDLE

    def find_available_device(self, applicant=None, timeout=60, **kwargs):
        """
        查找合适的设备
        :param applicant: 申请人
        :param timeout: 超时时间
        :param kwargs:
        :return:
        """
        with self._lock:
            has_matches = False
            if 'status' not in kwargs:
                kwargs['status'] = IDLE
            status = kwargs['status']
            if 'serial' in kwargs:
                device = self.devices[kwargs["serial"]]
                if device.match(**kwargs):
                    if device.status == status:
                        device.status = ASSIGNED
                        return device

            for _, device in self.devices.items():
                if device.match(**kwargs):
                    if device.status == status:
                        device.status = ASSIGNED
                        return device
                    else:
                        has_matches = True

            if has_matches:
                logger.debug(f'{applicant} waiting for idle device: {kwargs}')
                self._event.clear()
                self._event.wait(timeout)
                return self.find_available_device(applicant=applicant, **kwargs)
            else:
                raise NoAvailableDeviceError(kwargs)


device_pool = DevicePool()

if __name__ == '__main__':
    # d = device_pool.find_available_device()
    # d1 = device_pool.find_available_device()
    d = device_pool.devices
    f = d

