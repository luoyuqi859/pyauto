#! /usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: event
@Created: 2023/2/25
"""
import re
import time


class Event:
    """
    事件
    用法：
        device.event('/dev/input/event0').keys('1c').down().wait(2).up()
    """

    def __init__(self, device):
        self.device = device
        self._event = None
        self._cur_keys = []

    def __call__(self, event_type):
        self._event = event_type
        return self

    def all(self):
        output = self.device.shell('getevent -i')
        p = re.compile(r'add device \d: ((?:/\w+){3}).+?name:\s+"(.+?)"', re.DOTALL)
        for item in p.finditer(output):
            yield item

    def keys(self, *values):
        values = [int(str(value), 16) for value in values]
        self._cur_keys = values
        return self

    def down(self):
        assert self._cur_keys, 'please call keys() first!'
        for key in self._cur_keys:
            self.device.shell(f'sendevent {self._event} 1 {key} 1')
        self.device.shell(f'sendevent {self._event} 0 0 0')
        return self

    def wait(self, seconds=1):
        time.sleep(seconds)
        return self

    def up(self):
        assert self._cur_keys, 'please call keys() and down() first!'
        for key in self._cur_keys:
            self.device.shell(f'sendevent {self._event} 1 {key} 0')
        self.device.shell(f'sendevent {self._event} 0 0 0')
        self._cur_keys.clear()

    def press(self):
        """
        按键操作
        :return:
        """
        return self.down().up()

    def long_press(self, duration=1):
        """
        长按
        :param duration:
        :return:
        """
        return self.down().wait(duration).up()