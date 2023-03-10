#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: device
@Created: 2023/2/20 17:07
"""
import math
import re
import subprocess
import time

from conf import settings
import uiautomator2 as u2
from uiauto.android.adb import ADB
from uiauto.android.android_keys import AndroidKeys
from uiauto.android.parse import Bounds
from uiauto.android.plugins.accessory import Accessory
from uiauto.android.plugins.airplane import Airplane
from uiauto.android.plugins.app import App
from uiauto.android.base import BaseDevice
from uiauto.android.plugins.battery import UiaBattery
from uiauto.android.plugins.bt import Bluetooth
from uiauto.android.plugins.event import Event
from uiauto.android.plugins.forward import Forward
from uiauto.android.plugins.minicap import Minicap
from uiauto.android.plugins.ocr import Ocr
from uiauto.android.plugins.page import AndroidPage
from uiauto.android.plugins.prop import Prop
from uiauto.android.plugins.qs import QuickSettings
from uiauto.android.plugins.rotation import UiaRotation
from uiauto.android.plugins.screenshot import UiaScreenshot
from uiauto.android.plugins.swipe import UiaSwipe
from uiauto.android.plugins.wifi import Wifi
from uiauto.android.u2.element import AndroidElement
from uiauto.android.u2.selector import Selector
from utils.errors import ElementNotFoundError, AdbError

from utils.log import logger


def get_device_id():
    """获取设备id"""
    return ADB().adb.serial


def connect(serial=None) -> u2.Device:
    serial = serial or get_device_id()
    d = u2.Device(serial)
    d.implicitly_wait(settings.ELEMENT_WAIT_TIMEOUT)
    # d.settings['operation_delay'] = (settings.FORCE_STEP_INTERVAL_BEFORE, settings.FORCE_STEP_INTERVAL_AFTER)
    # d.settings['operation_delay_methods'] = ['click', 'swipe', 'drag', 'press']
    # d.jsonrpc.setConfigurator({"waitForIdleTimeout": 100})
    return d


class AndroidDevice(BaseDevice):

    def __init__(self, device, **kwargs):
        super().__init__(**kwargs)
        self.d: u2.Device = device
        self._adb = None

    def __getattr__(self, item):
        self.__get_info()
        return self.get(item, None)

    def __call__(self, o=None, **kwargs):
        if isinstance(o, AndroidElement):
            o.device = self
            return o
        elif isinstance(o, Selector) or isinstance(o, dict):
            kwargs.update(o)
            return AndroidElement(device=self, **kwargs)
        return AndroidElement(device=self, **kwargs)

    def __repr__(self):
        return f'<AndroidDevice {self.name or self.serial}'

    def __eq__(self, other):
        return other and self.serial == other.serial

    def __hash__(self):
        return hash(self.serial)

    @property
    def info(self):
        """获取设备基本信息"""
        return self

    def __get_info(self):
        res = self.d.http.get('/info').json()

        if res:
            self['width'] = res.get("display").get("width")
            self['height'] = res.get("display").get("height")
            self['brand'] = res.get("brand")
            self['model'] = res.get("model")
            self['sdk'] = res.get("sdk")
            self['platform_version'] = res.get("version")

    @property
    def name(self):
        """
        设备名称
        :return:
        """
        return self.get('name') or self.serial

    @property
    def minicap(self):
        """获取设备基本信息"""
        return Minicap(self)

    @property
    def serial(self):
        """
        序列号
        """
        if not self.get('serial'):
            self['serial'] = ADB().adb.serial
        return self['serial']

    @property
    def id(self):
        return self.d.serial

    @property
    def ocr(self):
        if not self._ocr:
            self._ocr = Ocr(self)
        return self._ocr

    @property
    def adb_fp(self):
        """
        得到AdbDevice对象，以便调用相应的api

        :return:
        """
        if not self._adb:
            self._adb = ADB(device_id=self.id)
        return self._adb

    @property
    def event(self):
        return Event(self)

    @property
    def prop(self):
        return Prop(self)

    @property
    def app(self):
        return App(self)

    @property
    def qs(self):
        return QuickSettings(self)

    @property
    def battery(self):
        return UiaBattery(self)

    @property
    def bt(self):
        return Bluetooth(self)

    @property
    def airplane(self):
        return Airplane(self)

    @property
    def wifi(self):
        return Wifi(self)

    @property
    def accessory(self):
        return Accessory(self)

    @property
    def forward(self):
        return Forward(self)

    @property
    def page(self):
        return AndroidPage(device=self)

    @property
    def rotation(self):
        if 'rotation' not in self:
            self['rotation'] = UiaRotation(self)
        return self.get('rotation')

    @property
    def swipe(self):
        return UiaSwipe(self)

    @property
    def screenshot(self):
        """
        屏幕截图
        :return:
        """
        return UiaScreenshot(self)

    @property
    def window_size(self):
        """
        Documents:
            Resolution size
        Return:
            return (width, height)
        """
        info = self.d.http.get('/info').json()
        w, h = info['display']['width'], info['display']['height']
        return w, h

    @property
    def is_multi_window_mode(self):
        """
        是否处于分屏状态

        :return:
        """
        source = self.d.dump_hierarchy()
        p = re.compile(r'package="\S+"')
        _list = p.findall(source)
        return len(set(_list)) > 2

    @property
    def display_bounds(self):
        if not self.__display_bounds:
            w, h = self.window_size
            try:
                f = "com.android.systemui:id/gm_car_status_bar"
                d = "com.android.systemui:id/status_bar"
                status_bar_bounds = self(id=f, timeout=0).bounds
            except ElementNotFoundError:
                status_bar_bounds = Bounds(0, 0, 0, 0)
            try:
                nav_bar_bounds = self(id='com.android.systemui:id/navigation_bar_frame', timeout=0).bounds
            except ElementNotFoundError:
                nav_bar_bounds = Bounds(0, h, 0, 0)
            self.__display_bounds = Bounds(0, status_bar_bounds.bottom, w, nav_bar_bounds.top)

        return self.__display_bounds

    def abs_pos(self, x, y):
        w, h = self.window_size
        if x is not None:
            x = int(x) if x > 1 else int(x * w)
        if y is not None:
            y = int(y) if y > 1 else int(y * h)
        return x, y

    def rel_pos(self, x, y):
        w, h = self.window_size
        x = x / w if x > 1 else x
        y = y / h if y > 1 else y
        return x, y

    def calc_swipe_steps(self, distance=1.0, vertical=True):
        """
        计算滑动所需要的步数，默认纵向滑动一屏（distance=1）需要的步数是55

        :param distance: 滑动距离，取值范围在 0 ~ 1
        :param vertical: 是否纵向滑动
        :return:
        """
        if vertical:
            return math.ceil(distance * settings.MAX_SWIPE_STEPS)
        else:
            w, h = self.window_size
            return math.ceil(distance * w * settings.MAX_SWIPE_STEPS / h)

    def app_list(self):
        """
        Returns:
            list of apps by filter
        """
        return self.d.app_list()

    def app_info(self, pkg_name):
        """
        Get app info
        Args:
            pkg_name (str): package name
        Return example:
            {
                "mainActivity": "com.github.uiautomator.MainActivity",
                "label": "ATX",
                "versionName": "1.1.7",
                "versionCode": 1001007,
                "size":1760809
            }
        Raises:
            UiaError
        """
        return self.d.app_info(pkg_name)

    def click_more(self, x, y, sleep=.01, times=3):
        """
        连续点击
        x: 横坐标
        y: 纵坐标
        sleep(float): 间隔时间
        times(int): 点击次数
        """
        w, h = self.window_size
        x, y = (w * x, h * y) if x < 1 and y < 1 else x, y
        for i in range(times):
            self.d.touch.down(x, y)
            time.sleep(sleep)
            self.d.touch.up(x, y)

    def click(self, *args, **kwargs):
        """
        元素点击
        element:text="Settings" xpath="//*[@text='Settings']"
        :return:
        """

        def _click_process(*args, **kwargs):
            if len(args) == 2 and isinstance(args[0], (int, float)) and isinstance(args[1], (int, float)):
                x, y = self.abs_pos(args[0], args[1])
                self.d.click(x, y)
                logger.success(f'Click {ele_name or f"position: {x}, {y}"}')
            elif len(args) == 1 and isinstance(args[0], str):
                try:
                    self(text=args[0]).click()
                except ElementNotFoundError:
                    self(content=args[0]).click()

            else:
                selectors = [*args]
                if kwargs:
                    selectors.append(kwargs)
                for selector in selectors:
                    selector = self.get_element(**selector)
                    selector.click()
                logger.success("click element:「{}」".format(kwargs))

        ele_name = kwargs.get('name', None)
        times = kwargs.get('times', None)
        if times:
            for i in range(times):
                _click_process(*args, **kwargs)
        else:
            _click_process(*args, **kwargs)

        return self

    def press(self, key, meta=0, times=1):
        """
        按键操作

        :param key: 键值，可以是按键名称或键值，或AndroidKeys枚举
        :param meta: 修饰键
        :param times: 按键次数
        :return:
        """
        if isinstance(key, (int, AndroidKeys)):
            for i in range(times):
                self.d.press(key=key, meta=meta)
                logger.success(f"press {key}")
        else:
            key_code = AndroidKeys.get_code(key)
            for i in range(times):
                self.d.press(key=key_code, meta=meta)
                logger.success(f"press {key}")
        return self

    def get_element(self, **element):
        '''
        获取元素
        :return:
        '''
        xpath = element.get("xpath", None)
        if xpath:
            return self.d.xpath(xpath)
        else:
            return self.d(**element)

    def assert_exist(self, **element):
        """
        断言元素是否存在

        :return:
        """
        selector = self.get_element(**element)
        if not selector.exists:
            raise ElementNotFoundError(f"{element} not found")
        logger.success(f'assert element exists: {element}, successful')
        return selector

    def assert_not_exist(self, **element):
        """
        断言元素不存在

        :return:
        """
        selector = self.get_element(**element)
        assert not selector.exists, f'{element} exists actually.'
        logger.success(f'assert element not exists: {element}, successful')

    def send_keys(self, element, sendtext, log_text):
        """
        文本输入
        element:元素名称
        sendtext:输入的文案
        log_text:打印log的文案
        :return:
        """
        if str(element).startswith("com"):
            self.d(resourceId=element).set_text(sendtext)
        elif re.findall("//", str(element)):
            self.d.xpath(element).set_text(sendtext)
        else:
            self.d(text=element).set_text(sendtext)

        logger.info("输入文字「{}」".format(log_text))

    def double_click(self, x, y, time=0.5):
        """
        双击
        :return:
        """
        self.d.double_click(x, y, time)
        logger.info("点击坐标:「{}」,「{}」".format(x, y))

    def toast_show(self, text, duration=5):
        """
        页面出现弹窗提示时间，默认时间5s
        :param text:弹窗内容
        :param duration:弹窗提示时间
        :return:
        """
        self.d.toast.show(text, duration)
        logger.success(f"toast show : {text}")

    def find_elements(self, element, timeout=5):
        """
        查找元素是否存在当前页面
        :param element: 元素内容
        :param timeout:log元素内容
        :return:
        """
        is_exist = False
        try:
            while timeout > 0:
                xml = self.d.dump_hierarchy()
                if re.findall(element, xml):
                    is_exist = True
                    logger.success("found element success「{}」".format(element))
                    break
                else:
                    timeout -= 1
        except Exception as e:
            logger.error("「{}」found element failed「{}」".format(element, e))
        finally:
            return is_exist

    def shell(self, cmd_args, stream=False, timeout=60):
        cmdline = subprocess.list2cmdline(cmd_args) if isinstance(cmd_args, (list, tuple)) else cmd_args
        if stream:
            return self.d.http.get("get", "/shell/stream", params={"command": cmdline}, timeout=None, stream=True)
        ret = self.d.http.post('/shell', data={'command': cmdline, 'timeout': str(timeout)},
                               timeout=timeout + 10, retry=False)
        if ret.status_code != 200:
            raise RuntimeError("device agent responds with an error code %d" % ret.status_code, ret.text)
        resp = ret.json()
        error = resp.get('error')
        if error:
            raise AdbError(error)
        return resp.get('output')
