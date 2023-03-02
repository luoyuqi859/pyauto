#!/usr/bin/env python
# -*- ecoding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: rotation
@Created: 2023/2/27 10:48
"""
import re
from enum import Enum

from utils.log import logger

NORMAL = 0
LEFT = 1
UPSIDE_DOWN = 2
RIGHT = 3


class Rotation(Enum):
    """
    旋转枚举
    """
    normal = 0
    left = 1
    upside_down = 2
    right = 3


def _parse_rotation_status(command_output):
    _DISPLAY_RE = re.compile(r'.*DisplayViewport{.+valid=true, '
                             r'.*orientation=(?P<orientation>\d+), '
                             r'.*deviceWidth=(?P<width>\d+), '
                             r'deviceHeight=(?P<height>\d+).*')
    code = None
    for line in command_output.splitlines():
        m = _DISPLAY_RE.search(line, 0)
        if not m:
            continue
        code = int(m.group('orientation'))
        break
    return code


class _BaseRotation:
    def __init__(self, device):
        self.device = device

    def __getitem__(self, item):
        return getattr(self, item)

    @property
    def status(self):
        _DISPLAY_RE = re.compile(r'.*DisplayViewport{.+valid=true, '
                                 r'.*orientation=(?P<orientation>\d+), '
                                 r'.*deviceWidth=(?P<width>\d+), '
                                 r'deviceHeight=(?P<height>\d+).*')
        output = self.device.shell('dumpsys display').output
        code = _parse_rotation_status(output)
        code = code if code is not None else self.device.info["displayRotation"]
        rotation = Rotation(code)
        return rotation


class AdbRotation(_BaseRotation):

    def back(self):
        self.__user_rotate(NORMAL)
        return self

    def left(self):
        self.__user_rotate(LEFT)
        return self

    def upside_down(self):
        self.__user_rotate(UPSIDE_DOWN)
        return self

    def right(self):
        self.__user_rotate(RIGHT)
        return self

    def enable(self):
        self.__accelerometer_rotate(1)
        return self

    def disable(self):
        self.__accelerometer_rotate(0)
        return self

    def __user_rotate(self, value):
        self.device.shell(f'content insert --uri content://settings/system '
                          f'--bind name:s:user_rotation --bind value:i:{value}')

    def __accelerometer_rotate(self, value):
        self.device.shell(f'content insert --uri content://settings/system '
                          f'--bind name:s:accelerometer_rotation --bind value:i:{value}')


class UiaRotation(_BaseRotation):

    def _set_direction(self, direction='natural'):
        self.device.d.jsonrpc.setOrientation(direction)

    def left(self):
        self._set_direction('left')

    def right(self):
        self._set_direction('right')

    def back(self):
        self._set_direction('natural')

    def upside_down(self):
        self._set_direction('upsidedown')

    def enable(self, enabled=False):
        self.device.d.jsonrpc.freezeRotation(not enabled)
        logger.success(f'{"enable" if enabled else "disable"} rotation')

    def disable(self):
        self.enable(enabled=False)
