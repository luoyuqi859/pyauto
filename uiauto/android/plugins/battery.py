#! /usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: battery
@Created: 2023/2/25
"""
from utils.dict import Dict


class Battery:
    """
    电池
    """

    def __init__(self, device):
        self.device = device
        self._technology = None

    def is_low(self):
        """
        是否低电量
        :return:
        """
        return self.device.shell('dumpsys power | grep mBatteryLevelLow=') == "mBatteryLevelLow=true"

    @property
    def level(self):
        """
        电量
        :return:
        """
        return self.dump().level

    @property
    def technology(self):
        """
        厂商
        :return:
        """
        if not self._technology:
            self._technology = self.dump().technology
        return self._technology

    def watch(self):
        raise NotImplementedError

    def dump(self):
        """电池状态： ac_powered, usb_powered, wireless_powered, max_charging_current, max_charging_voltage"""
        output = self.device.shell('dumpsys battery')
        data = {}
        for line in output.split('\n'):
            line = line.strip()
            arr = line.split(':')
            if len(arr) > 1:
                data[arr[0].lower().replace(' ', '_')] = arr[1].strip()
        return Dict(data)


class AdbBattery(Battery):
    def watch(self):
        pass


class UiaBattery(Battery):
    def watch(self):
        pass
