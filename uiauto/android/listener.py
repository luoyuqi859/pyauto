#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: listener
@Created: 2023/3/11
"""
import inspect

from httpx import Proxy

from conf import settings
from utils import py


class __ListenService:
    def __init__(self):
        self.device_listeners = []

    def add_device_listener(self, listener):
        self.device_listeners.append(listener)

    def trigger_device_connected(self, adb):
        for listener in self.device_listeners:
            listener().on_device_connected(adb)

    def trigger_device_reconnected(self, adb):
        for listener in self.device_listeners:
            listener().on_device_reconnected(adb)

    def trigger_device_disconnected(self, device):
        for listener in self.device_listeners:
            listener().on_device_disconnected(device)

    def trigger_device_status_changed(self, device, old, new, *args, **kwargs):
        for listener in self.device_listeners:
            listener().on_status_changed(device, old, new, *args, **kwargs)


listen_service = __ListenService()


def device_listener(cls):
    listen_service.device_listeners.append(cls)
    return cls


class DeviceListener:
    """
    设备监听器
    """

    def on_status_changed(self, device, old, new, **kwargs):
        pass

    def on_detected(self, devices, *args, **kwargs):
        pass

    def on_device_connected(self, device):
        pass

    def on_device_disconnected(self, device):
        pass

    def on_device_reconnected(self, device):
        pass


listeners = []


def _iter_listeners():
    if not listeners:
        for item in settings.DEVICE_LISTENERS:
            if isinstance(item, str):
                item = py.get_object(item)
            if inspect.isclass(item):
                listener = Proxy(item())
                listeners.append(listener)
            elif inspect.ismodule(item):
                listener = Proxy(item)
                listeners.append(listener)
            else:
                raise InvalidDeviceListenerError(item)
            yield listener
    else:
        for listener in listeners:
            yield listener


def on_device_connected(device):
    for listener in _iter_listeners():
        listener.on_device_connected(device)


def on_device_disconnected(device):
    for listener in _iter_listeners():
        listener.on_device_disconnected(device)


def on_device_reconnected(device):
    for listener in _iter_listeners():
        listener.on_device_reconnected(device)


def on_device_idle(device):
    for listener in _iter_listeners():
        listener.on_device_idle(device)


def on_device_running(device):
    for listener in _iter_listeners():
        listener.on_device_running(device)


def on_device_recording(device):
    for listener in _iter_listeners():
        listener.on_device_recording(device)


class InvalidDeviceListenerError(Exception):
    """"""

