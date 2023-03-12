#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: watch
@Created: 2023/3/1 19:09
"""
from uuid import uuid4

from uiautomator2 import UiObject

from uiauto.android.u2.selector import Selector
from utils.errors import AdbError, UiaError
from loguru import logger


class Watcher(object):
    """监听器"""

    def __init__(self, device=None, name=None, selector=None, **kwargs):
        self.device = device
        self.name = name or str(uuid4())
        self.conditions = []
        self.registered = False
        self.selector = selector or (Selector(**kwargs) if kwargs else None)
        self.u2obj = UiObject(self.device.d, self.selector)

    def when_exists(self, *args, **kwargs):
        """当元素存在"""
        for arg in args:
            if isinstance(arg, Selector):
                self.conditions.append(arg)
            else:
                self.conditions.append(Selector(**arg))
        if kwargs:
            self.conditions.append(Selector(**kwargs))
        return self

    def click(self, *args, **kwargs):
        """点击元素"""
        if args:
            target = args[0]
        elif kwargs:
            target = Selector(**kwargs)
        else:
            raise AdbError("监听器点击操作必须指定目标元素！")
        if self.device and not self.registered:
            self.u2obj.jsonrpc.registerClickUiObjectWatcher(self.name, self.conditions, target)
            logger.info(f'监听{self.conditions}成功')
            self.registered = True
        return self

    def press(self, *args):
        """按键"""
        if self.device and not self.registered:
            self.u2obj.jsonrpc.registerClickUiObjectWatcher(self.name, self.conditions, args)
            logger.info(f'监听{self.conditions}成功')
            self.registered = True
        return self


class Watch:
    def __init__(self, device=None, selector=None, **kwargs):
        self.device = device
        if self.device.watchers is None:
            self.device.watchers = {}
        self.name = str(uuid4())
        self.conditions = []
        self.registered = False
        self.selector = selector or (Selector(**kwargs) if kwargs else None)
        self.u2obj = UiObject(self.device.d, self.selector)

    def __call__(self, name):
        self.name = name
        return self

    def when_exists(self, *args, **kwargs):
        """当元素存在"""
        for arg in args:
            if isinstance(arg, Selector):
                self.conditions.append(arg)
            else:
                self.conditions.append(Selector(**arg))
        if kwargs:
            self.conditions.append(Selector(**kwargs))
        return self

    def click(self, *args, **kwargs):
        """点击元素"""
        if args:
            target = args[0]
        elif kwargs:
            target = Selector(**kwargs)
        else:
            raise UiaError("监听器点击操作必须指定目标元素！")
        if self.device and not self.registered:
            self.u2obj.jsonrpc.registerClickUiObjectWatcher(self.name, self.conditions, target)
            logger.info(f'监听{self.conditions}成功')
            self.registered = True
        return self

    def press(self, *args):
        """按键"""
        if self.device and not self.registered:
            self.u2obj.jsonrpc.registerClickUiObjectWatcher(self.name, self.conditions, args)
            logger.info(f'监听{self.conditions}成功')
            self.registered = True
        return self

    def remove(self, name):
        if name in self.device.watchers:
            self.device.watchers.pop(name)
            self.u2obj.jsonrpc.removeWatcher(name)
