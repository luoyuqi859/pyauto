#!/usr/bin/env python
# -*- ecoding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: device
@Created: 2023/2/20 17:07
"""
import math
import re
import time

import uiautomator2
from cached_property import cached_property

from conf import settings
from uiauto.android.adb import ADB
from uiauto.android.android_keys import AndroidKeys
from uiauto.android.plugins.accessory import Accessory
from uiauto.android.plugins.airplane import Airplane
from uiauto.android.plugins.app import App
from uiauto.android.base import BaseDevice
from uiauto.android.plugins.battery import UiaBattery
from uiauto.android.plugins.bt import Bluetooth
from uiauto.android.plugins.event import Event
from uiauto.android.plugins.forward import Forward
from uiauto.android.plugins.page import AndroidPage
from uiauto.android.plugins.prop import Prop
from uiauto.android.plugins.qs import QuickSettings
from uiauto.android.plugins.swipe import UiaSwipe
from uiauto.android.plugins.wifi import Wifi
from utils.errors import ElementNotFoundError

from utils.log import logger


class AndroidDevice(BaseDevice):

    def __init__(self, device: uiautomator2.Device, **kwargs):
        super().__init__(**kwargs)
        self.d = device
        self._adb = None

    @property
    def id(self):
        return self.d.serial

    @cached_property
    def adb_fp(self):
        return ADB(device_id=self.id)

    @property
    def event(self):
        return Event(self.d)

    @property
    def prop(self):
        return Prop(self.d)

    @property
    def app(self):
        return App(self.d)

    @property
    def qs(self):
        return QuickSettings(self.d)

    @property
    def battery(self):
        return UiaBattery(self.d)

    @property
    def bt(self):
        return Bluetooth(self.d)

    @property
    def airplane(self):
        return Airplane(self.d)

    @property
    def wifi(self):
        return Wifi(self.d)

    @property
    def accessory(self):
        return Accessory(self.d)

    @property
    def forward(self):
        return Forward(self)

    @property
    def page(self):
        return AndroidPage(device=self.d)

    @property
    def swipe(self):
        return UiaSwipe(self)

    @property
    def window_size(self):
        """
        Documents:
            Resolution size
        Return:
            return (width, height)
        """
        return self.d.window_size()

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
        w, h = self.window_size()
        x, y = (w * x, h * y) if x < 1 and y < 1 else x, y
        for i in range(times):
            self.d.touch.down(x, y)
            time.sleep(sleep)
            self.d.touch.up(x, y)

    def click(self, **element):
        """
        元素点击
        element:text="Settings" xpath="//*[@text='Settings']"
        :return:
        """
        selector = self.get_element(**element)
        selector.click(),
        logger.info("点击元素:「{}」".format(element))
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
                logger.info(f"press {key}")
        else:
            key_code = AndroidKeys.get_code(key)
            for i in range(times):
                self.d.press(key=key_code, meta=meta)
                logger.info(f"press {key}")
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
            raise ElementNotFoundError(f"{element} 不存在")
        logger.info(f'断言元素存在: {element}, 成功')
        return selector

    def assert_not_exist(self, **element):
        """
        断言元素是否存在

        :return:
        """
        selector = self.get_element(**element)
        assert not selector.exists, f'{element} exists actually.'
        logger.info(f'断言元素不存在: {element}, 成功')

    def up(self, scale=0.9, times=1, duration=1.0, **kwargs):
        """
        上滑操作
        :param scale: 滑动单位，默认0.9个单位
        :param times: 滑动次数，默认1次
        :param duration: 滑动时间，默认1.0秒
        :return:
        """
        for i in range(times):
            self.d.swipe_ext("up", scale, duration=duration, **kwargs)
            logger.info("向上滑动")

    def down(self, scale=0.9, times=1, duration=1.0, **kwargs):
        """
        下滑操作
        :param scale: 滑动单位，默认0.9个单位
        :param times: 滑动次数，默认1次
        :param duration: 滑动时间，默认1.0秒
        :return:
        """
        for i in range(times):
            self.d.swipe_ext("down", scale, duration=duration, **kwargs)
            logger.info("向下滑动")

    def left(self, scale=0.9, times=1, duration=1.0, **kwargs):
        """
        左滑操作
        :param scale: 滑动单位，默认0.9个单位
        :param times: 滑动次数，默认1次
        :param duration: 滑动时间，默认1.0秒
        :return:
        """
        for i in range(times):
            self.d.swipe_ext("left", scale, duration=duration, **kwargs)
            logger.info("向左滑动")

    def right(self, scale=0.9, times=1, duration=1.0, **kwargs):
        """
        右滑操作
        :param scale: 滑动单位，默认0.9个单位
        :param times: 滑动次数，默认1次
        :param duration: 滑动时间，默认1.0秒
        :return:
        """
        for i in range(times):
            self.d.swipe_ext("right", scale, duration=duration, **kwargs)
            logger.info("向右滑动")

    def wait_until_element_found(self, param, timeout=30.0, retry_interval=2, wait_after_found=0.0):
        """
        定位元素，如果不存在就间隔若干秒后重试，直到元素定位成功或超时
        :param param: xpath字符串 或 元素对象
        :param timeout: 超时, 默认30秒
        :param retry_interval: 间隔时间, 默认2秒
        :param wait_after_found: 找到元素后，原地等待时间
        :return:
        """
        element = self.d.xpath(param) if isinstance(param, str) else param
        max_time = time.time() + timeout
        while True:
            try:
                assert element.exists
                if wait_after_found:
                    logger.info("Element found，then sleep {} seconds".format(wait_after_found))
                time.sleep(wait_after_found)
                return element
            except AssertionError:
                param = param if isinstance(param, str) else param.selector
                logger.warning("Element 【 {} 】 Not found, Retry...".format(param))
                if time.time() > max_time > 0:
                    raise AssertionError("Element 【 {} 】 located failed after {} timeout".format(param, timeout))
                time.sleep(retry_interval)

    def wait_for_click(self, param, wait_after_click=0.0, **kwargs):
        """
        判断UI元素是否存在, 不存在则等待UI元素在一定时间内出现，再进行点击
        :param param: xpath字符串 或 元素对象
        :param wait_after_click: 点击后等待时间
        :return:
        """
        element = self.wait_until_element_found(param, **kwargs)
        element.click()
        if wait_after_click:
            logger.info("Element found and click，then sleep {} seconds".format(wait_after_click))
        time.sleep(wait_after_click)

    def repeat_click(self, param, times, wait_after_repeat_click=0.0):
        """
        重复多次点击UI元素
        :param param: xpath字符串 或 元素对象
        :param times: 点击次数
        :param wait_after_repeat_click: 重复点击后等待时间，默认为0.0
        :return:
        """
        element = self.wait_until_element_found(param)
        for i in range(times):
            element.click()
        if wait_after_repeat_click:
            logger.info("Element click，then sleep {} seconds".format(wait_after_repeat_click))
        time.sleep(wait_after_repeat_click)

    def swipe_until_element_found(self, param, wait_after_found=0.0, **kwargs):
        """
        检查元素是否存在，若不存在则进行上滑，滑动后再次检查，直到滑动到页面底部
        若找到元素则返回，否则滑动到页面底部后，仍未找到元素，则抛出异常，提示找不到元素
        :param param: xpath字符串 或 元素对象
        :param wait_after_found: 找到元素后，原地等待时间
        :param kwargs:
        :return:
        """
        element = self.d.xpath(param) if isinstance(param, str) else param
        param = param if isinstance(param, str) else param.selector
        while True:
            try:
                assert element.exists
                if wait_after_found:
                    logger.info("Element found，sleep {} seconds".format(wait_after_found))
                time.sleep(wait_after_found)
                return element
            except AssertionError:
                logger.warning("Element 【 {} 】 Not found, Continue to swipe up...".format(param))
                # 获取滑动前页面下半部分的所有元素
                page_content = self.d.dump_hierarchy()[(len(self.d.dump_hierarchy()) // 2):]
                self.up(**kwargs)
                time.sleep(0.5)
                # 获取滑动后页面下半部分的所有元素，并与上一次滑动前的页面元素对比，页面元素没有变化时跳出循环
                if self.d.dump_hierarchy()[(len(self.d.dump_hierarchy()) // 2):] == page_content:
                    break
        if not element.exists:
            raise AssertionError("Element 【 {} 】 located failed in this page".format(param))

    def swipe_for_click(self, param, wait_after_click=0.0, **kwargs):
        """
        判断UI元素是否存在, 不存在则持续向上滑动到底部，直到UI元素在页面内出现，再进行点击
        :param param: xpath字符串 或 元素对象
        :param wait_after_click: 点击后等待时间
        :return:
        """
        element = self.swipe_until_element_found(param, **kwargs)
        element.click()
        if wait_after_click:
            logger.info("Element found and click，then sleep {} seconds".format(wait_after_click))
        time.sleep(wait_after_click)

    def click_advance(self, element_list):
        """
        根据绝对坐标点击 包含坐标和坐标描述
        例：{"location":(0.848, 0.91),"description":"修改"}
        :param element_list:
        :return:
        """
        x = element_list["location"][0]
        y = element_list["location"][1]
        self.d.click(x, y)
        logger.info("点击元素「{}」".format(element_list["description"]))

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

    def get_window_size(self):
        """
        获取屏幕尺寸
        :return:
        """
        window_size = self.d.window_size()
        width = int(window_size[0])
        height = int(window_size[1])
        return width, height

    def direction_swipe(self, direction, element, steps=200):
        """
        方向滑动
        :param direction: 方向
        :param element:  元素
        :param steps:  1 steps is about 5ms, so 20 steps is about 0.1s
        :return:
        """
        self.d(text=element).swipe(direction, steps=steps)

    def swipe_to_element(self, element1, element2, duration=0.25):
        """
        滑动到某个元素
        :param element1: 起始元素
        :param element2: 目标元素
        :param duration: 滑动时间
        :return:
        """
        self.d(text=element1).drag_to(text=element2, duration=duration)
        logger.info("拖动元素「{}」至元素「{}」处".format(element1, element2))

    def toast_show(self, text, duration=5):
        """
        页面出现弹窗提示时间，默认时间5s
        :param text:弹窗内容
        :param duration:弹窗提示时间
        :return:
        """
        self.d.toast.show(text, duration)
        logger.info("展示文字")

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
                    logger.info("查询到「{}」".format(element))
                    break
                else:
                    timeout -= 1
        except Exception as e:
            logger.error("「{}」查找失败!「{}」".format(element, e))
        finally:
            return is_exist

    def __repr__(self):
        return f'<AndroidDevice {self.name or self.serial}'

    def __eq__(self, other):
        return other and self.serial == other.serial

    def __hash__(self):
        return hash(self.serial)
