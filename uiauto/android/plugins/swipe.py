#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: swipe
@Created: 2023/2/25
"""
import math
import time

from utils.log import logger


class Swipe:
    def __init__(self, device):
        self.device = device
        self.fx, self.fy, self.tx, self.ty = 0.5, 0.8, 0.5, 0.2

    @property
    def left(self):
        self.fx, self.fy, self.tx, self.ty = 0.2, 0.5, 0.8, 0.5
        return self

    @property
    def right(self):
        self.fx, self.fy, self.tx, self.ty = 0.8, 0.5, 0.2, 0.5
        return self

    @property
    def down(self):
        self.fx, self.fy, self.tx, self.ty = 0.5, 0.8, 0.5, 0.2
        return self

    @property
    def up(self):
        self.fx, self.fy, self.tx, self.ty = 0.5, 0.2, 0.5, 0.8
        return self

    def __call__(self, fx=None, fy=None, tx=None, ty=None, duration=None, **kwargs):
        sx, sy = self.device.abs_pos(fx or self.fx, fy or self.fy)
        ex, ey = self.device.abs_pos(tx or self.tx, ty or self.ty)
        if not duration:
            self.device.d.shell(f'input swipe {sx} {sy} {ex} {ey}')
        else:
            self.device.d.shell(f'input swipe {sx} {sy} {ex} {ey} {duration}')
        time.sleep(0.5)
        return self

    def until(self, condition):
        assert callable(condition)
        satisfied = condition()
        while not satisfied:
            logger.info("condition not satisfaction, will continue to swipe")
            self.device.swipe(self.fx, self.fy, self.tx, self.ty)
            time.sleep(0.5)
            satisfied = condition()


class UiaSwipe(Swipe):
    def __init__(self, device):
        super().__init__(device)
        self.steps = None

    @property
    def left(self):
        self.fx, self.fy, self.tx, self.ty = 0.2, 0.5, 0.8, 0.5
        self.steps = self.device.calc_swipe_steps(0.6)
        return self

    @property
    def right(self):
        self.fx, self.fy, self.tx, self.ty = 0.8, 0.5, 0.2, 0.5
        self.steps = self.device.calc_swipe_steps(0.6)
        return self

    @property
    def down(self):
        self.fx, self.fy, self.tx, self.ty = 0.5, 0.8, 0.5, 0.2
        self.steps = self.device.calc_swipe_steps(0.6)
        return self

    @property
    def up(self):
        self.fx, self.fy, self.tx, self.ty = 0.5, 0.2, 0.5, 0.8
        self.steps = self.device.calc_swipe_steps(0.6)
        return self

    def gesture(self, points, duration=0.5):
        """
        多点滑动
        :param points:
        :param duration:
        :return:
        """
        return self.device.d.swipe_points(points, duration)

    def until_exists(self, **kwargs):
        self.until(lambda: self.device.get_element(**kwargs).exists)

    def __call__(self, fx=None, fy=None, tx=None, ty=None, duration=0.1, steps=None, **kwargs):
        """
        滑动操作
        :param fx: 起始点x坐标，相对值或绝对值
        :param fy: 起始点y坐标，相对值或绝对值
        :param tx: 目标点x坐标，相对值或绝对值
        :param ty: 目标点y坐标，相对值或绝对值
        :param duration: 滑动时长，影响滑动速度，值越小，滑动越快
        :param steps: 也是影响滑动速度，一般不使用
        :param kwargs: 不使用
        :return:
        """
        fx, fy, tx, ty = fx or self.fx, fy or self.fy, tx or self.tx, ty or self.ty
        instance = math.sqrt(math.pow(ty - fy, 2) + math.pow(tx - fx, 2))
        steps = steps or self.device.calc_swipe_steps(instance) or int(duration * 200)
        fx, fy = self.device.abs_pos(fx, fy)
        tx, ty = self.device.abs_pos(tx, ty)
        self.device.d.swipe(fx=fx, fy=fy, tx=tx, ty=ty, steps=steps)
        logger.success(f'swipe from {(fx, fy)} to {(tx, ty)}')
        return self
