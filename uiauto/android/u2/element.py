#! /usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: element
@Created: 2023/2/27 9:44
"""
import os
import time
from functools import wraps

import requests
from PIL.Image import Image
from PIL import Image
from uiautomator2 import UiObject

from conf import settings
from uiauto.android.parse import Bounds
from uiauto.android.plugins.watch import Watcher
from uiauto.android.u2.selector import Selector
from utils import image
from utils.dict import Dict
from utils.errors import ElementNotFoundError, TestFailedError, TestError, AdbError
from utils.log import logger


def cvt_bool(value):
    if isinstance(value, bool):
        return value
    return True if value.lower() == 'true' else False


def wait_exists(func):
    @wraps(func)
    def wrapper(ele, *args, **kwargs):
        try:
            return func(ele, *args, **kwargs)
        except ElementNotFoundError:
            ele.wait()
            return func(ele, *args, **kwargs)

    return wrapper


class Alignment(object):
    NONE = -1
    CENTER = 0
    LEFT = 1
    RIGHT = 2
    TOP = 3
    BOTTOM = 4
    TOP_LEFT = 5
    TOP_RIGHT = 6
    BOTTOM_LEFT = 7
    BOTTOM_RIGHT = 8


class AndroidElement:
    def __init__(self, name=None, device=None, selector=None, **kwargs):
        super().__init__()
        self._info = {}
        self._name = name or kwargs.pop('name', None)
        self.device = device

        self.timeout = kwargs.pop('timeout', settings.ELEMENT_WAIT_TIMEOUT)
        self.__scroll = kwargs.pop('scroll', None)
        # self.index = kwargs.pop('index', None)
        self.selector = selector or (Selector(**kwargs) if kwargs else None)
        self.u2obj = UiObject(self.device.d, self.selector)

    @property
    @wait_exists
    def info(self):
        """
        元素属性信息

        :return:
        """
        if not self._info:
            if isinstance(self.selector, Selector):
                self._info = self.u2obj.info
        return self._info

    @property
    def name(self):
        """
        元素名称，优先顺序：自定义名称，text，content-desc，选择器，xpath，如果这些都取不到，则为空

        :return:
        """
        return self._name or self._info.get('text', None) or self._info.get('contentDescription', '') or self._info.get(
            'content-desc', '') or self.selector or ''

    @property
    def resource_id(self):
        return self.info.get('resource-id', '') or self.info.get('resourceName', '')

    @property
    def content_desc(self):
        return self.info.get('contentDescription', '') or self.info.get('content-desc', '')

    @property
    def text(self):
        return self.info.get('text', '')

    @property
    def bounds(self):
        """
        元素矩形框
        :return: tuple, (left, top, right, bottom)
        """
        bounds = self.info.get('bounds')
        if isinstance(bounds, str):
            return Bounds.parse(bounds)
        elif isinstance(bounds, dict):
            return Bounds(bounds.get('left'), bounds.get('top'), bounds.get('right'), bounds.get('bottom'))
        return bounds

    @property
    def position(self):
        """
        坐标

        :return:
        """
        return self.bounds.center

    @property
    def rel_pos(self):
        """
        相对坐标

        :return:
        """
        x, y = self.position
        return self.device.rel_pos(x, y)

    @property
    def class_name(self):
        return self.info.get('className', '') or self.info.get('class', '')

    @property
    def selectable(self):
        return cvt_bool(self.info.get('selectable', False))

    @property
    def selected(self):
        return cvt_bool(self.info.get('selected', False))

    @property
    def checked(self):
        return cvt_bool(self.info.get('checked', False))

    @property
    def checkable(self):
        """
        是否可选中

        :return:
        """
        return cvt_bool(self.info.get('checkable', False))

    @property
    def focused(self):
        """
        是否拥有焦点

        :return:
        """
        return cvt_bool(self.info.get('focused', False))

    @property
    def focusable(self):
        return cvt_bool(self.info.get('focusable', False))

    @property
    def clickable(self):
        return cvt_bool(self.info.get('clickable', False))

    @property
    def long_clickable(self):
        return self.info.get('longClickable', False) or cvt_bool(self.info.get('long-clickable', False))

    @property
    def enabled(self):
        return cvt_bool(self.info.get('enabled', False))

    @property
    def exists(self):
        """
        注意它不会自动滑动，主要是因为避免做否判断时，页面被滑动导致后续操作全部失败

        :return:
        """
        return self.u2obj.exists

    @property
    def count(self):
        """
        注意使用时，如果需要滑动，请先调用 display() 确保其显示
        :return:
        """
        return self.u2obj.count

    def click(self, times=1, auto_scroll=True, raise_exception=True):
        if auto_scroll:
            self.scroll()

        @wait_exists
        def _click(ele):
            if self._info:
                x, y = self.position
                for i in range(times):
                    self.u2obj.jsonrpc.click(x, y)
            elif isinstance(self.selector, Selector):
                for i in range(times):
                    self.u2obj.jsonrpc.click(self.selector)

        try:
            _click(self)
            logger.success(f'Click element: {self.name or self.selector}')
            return True
        except ElementNotFoundError:
            if raise_exception:
                raise
            return False

    def try_click(self, times=1, auto_scroll=True, **kwargs):
        if kwargs:
            if self.check_info(**kwargs):
                return self.click(times, auto_scroll=auto_scroll, raise_exception=False)
            return False
        return self.click(times, auto_scroll, raise_exception=False)

    @wait_exists
    def long_click(self, duration=None, use_pos=False):
        """
        长按元素
        :param duration: 按下时长，单位为s
        :param use_pos: 强制使用坐标操作
        :return:
        """
        self.scroll()
        if self.long_clickable and not use_pos:
            if isinstance(self.selector, Selector):
                self.u2obj.jsonrpc.longClick(self.selector)
        else:
            x, y = self.position
            self.device.touch.down(x, y).move(x, y).sleep(duration or settings.LONG_CLICK_DURATION).up(x, y)
        logger.info(f'Long click element: {self.name}')

    def try_long_click(self, duration=None, use_pos=False):
        """
        尝试长按元素

        :param duration: 按下时长，单位为s
        :param use_pos: 是否强制使用坐标
        :return:
        """
        try:
            self.long_click(duration, use_pos)
            return True
        except ElementNotFoundError:
            logger.info(f'Ignore long-clicking non-existent element: {self.name}')
            return False

    def input(self, value, append=False):
        """
        输入给定值

        :param value:
        :param append: 是否追加输入
        :return:
        """
        if self._info:
            x, y = self.position
            self.u2obj.jsonrpc.click(x, y)
            self.device.input(value, append)
        elif isinstance(self.selector, Selector):
            if append:
                value = self.u2obj.jsonrpc.getText(self.selector) + value
            self.u2obj.jsonrpc.setText(self.selector, value)
        else:
            raise ElementNotFoundError(self.name)
        if not value:
            logger.info(f'Clear value: {self.name}')
        elif not append:
            logger.info(f'Input into element "{self.name}": {value}')
        else:
            logger.info(f'Append text for element "{self.name}": {value}')

    def clear_text(self):
        """
        清空输入框文本

        :return:
        """
        return self.input("")

    def swipe_up(self):
        left, top, right, bottom = self.bounds.unpack()
        cx, cy = (left + right) // 2, (top + bottom) // 2
        swipe_distance = max(settings.MIN_SWIPE, bottom - top)
        self.u2obj.jsonrpc.swipe(cx, cy, cx, cy - swipe_distance, 10)
        return cx, cy - swipe_distance

    def swipe_down(self):
        left, top, right, bottom = self.bounds.unpack()
        cx = (left + right) // 2
        swipe_distance = max(settings.MIN_SWIPE, bottom - top)
        self.u2obj.jsonrpc.swipe(cx, bottom, cx, bottom + swipe_distance, 10)
        return cx, bottom + swipe_distance

    def swipe_left(self):
        left, top, right, bottom = self.bounds.unpack()
        cx, cy = (left + right) // 2, (top + bottom) // 2
        swipe_distance = max(settings.MIN_SWIPE, right - left)
        self.u2obj.jsonrpc.swipe(cx, cy, cx - swipe_distance, cy, 10)
        return cx - swipe_distance, cy

    def swipe_right(self):
        left, top, right, bottom = self.bounds.unpack()
        cx, cy = (left + right) // 2, (top + bottom) // 2
        swipe_distance = max(settings.MIN_SWIPE, right - left)
        self.u2obj.jsonrpc.swipe(cx + swipe_distance, cy, cx, cy, 10)
        return cx + swipe_distance, cy

    def drag_to(self, *args, **kwargs):
        """
        拖动元素

        用法：

        1. 拖动到坐标：ele.drag_to(0.5, 0.5) 坐标推荐使用相对值

        2. 拖动到元素：ele.drag_to(text='container') 可接受多个属性参数

        允许传入duration参数（默认0.5）来控制拖动速度，值越小速度越快

        :param args:
        :param kwargs:
        :return:
        """
        self.scroll()
        ele_name = self.name
        duration = kwargs.pop('duration', 0.5)
        steps = int(duration * 200)
        if len(args) >= 2 or "x" in kwargs or "y" in kwargs:
            def drag2xy(x, y):
                x, y = self.device.abs_pos(x, y)
                self.u2obj.jsonrpc.dragTo(self.selector, x, y, steps)
                logger.info(f'drag element "{ele_name}" to ({x}, {y})')

            return drag2xy(*args, **kwargs)
        target_ele = Selector(**kwargs)
        self.u2obj.jsonrpc.dragTo(self.selector, target_ele, steps)
        logger.info(f'drag element "{ele_name}" to {target_ele}')

    def offset_drag(self, x=None, y=None, ox=None, oy=None, align=Alignment.CENTER):
        """偏移拖动"""
        pos = self.offset_pos(x=x, y=y, ox=ox, oy=oy, align=align)
        self.device.click(*pos)

    def scroll(self):
        if self.__scroll:
            self.device(scrollable=True).scroll_to(**self.selector, vertical=self.__scroll == 'v')
            self.update_info()

    def scroll_to(self, vertical=True, ele_name=None, **kwargs):
        assert self.selector
        s = Selector(**kwargs)
        r = self.u2obj.jsonrpc.scrollTo(self.selector, s, vertical)
        if not r:
            raise ElementNotFoundError(ele_name or s)
        logger.info(f'Scroll {self.name} to {ele_name or s}')

    def scroll_to_text(self, text, **kwargs):
        self.scroll_to(text=text, **kwargs)

    def check_info(self, **conditions):
        """
        检查元素属性信息

        :param conditions: 属性期望值，如 checked=True, enabled=False 可能希望复选框默认选中且不可取消
        :return: True/False
        """
        result = True
        for k, v in conditions.items():
            actual = getattr(self, k)
            result = result and actual == v
            if not result:
                break
        return result

    def update_info(self):
        """
        更新元素信息

        :return:
        """
        if self.selector:
            self._info = self.u2obj.jsonrpc.objInfo(self.selector)

    def display(self):
        """
        确保元素完全可见，如果元素被系统状态栏或者导航栏部分挡住，会微微滑动使元素完全可见

        :return:
        """
        try:
            self.scroll()
        except ElementNotFoundError:
            pass
        self.update_info()
        l, t, r, b = self.bounds.unpack()
        x, y = None, None
        if b >= self.device.display_bounds.bottom:
            x, y = self.swipe_up()
        elif 0 < t < self.device.display_bounds.top:
            x, y = self.swipe_down()
        elif 0 < l < self.device.display_bounds.left:
            x, y = self.swipe_right()
        elif r >= self.device.display_bounds.right:
            x, y = self.swipe_left()
        if not self.selector and x is not None and y is not None:
            self._info = self.device.page.parse(x, y).info
        else:
            self.update_info()

    def display_top(self):
        """
        使元素显示在屏幕上半区域 0.2 ~ 0.5，注意与display不同

        :return:
        """
        try:
            self.scroll()
        except ElementNotFoundError:
            pass
        self.update_info()
        l, t, r, b = self.bounds.unpack()
        if b / self.device.height >= 0.5:
            self.swipe_up()
            return
        elif t / self.device.height <= 0.2:
            self.device.swipe()  # TODO

    def display_bottom(self):
        """
        使元素显示在屏幕下半区域 0.5 ~ 0.8，注意与display不同

        :return:
        """

    def watch(self, name):
        """
        监听当前元素，如果出现自动执行点击操作，用于处理意外弹框

        :param name:
        :return:
        """
        watcher = Watcher(self.device, name)
        watcher.when_exists(self).click(self)

    def display_top(self):
        """
        使元素显示在屏幕上半区域 0.2 ~ 0.5，注意与display不同

        :return:
        """
        try:
            self.scroll()
        except ElementNotFoundError:
            pass
        self.update_info()
        l, t, r, b = self.bounds.unpack()
        if b / self.device.height >= 0.5:
            self.swipe_up()
            return
        elif t / self.device.height <= 0.2:
            self.device.swipe()  # TODO

    def screenshot(self, filename=None, fmt='pillow'):
        """
        元素截图

        :param filename: 保存的文件名称
        :param fmt: 输出格式：pillow/opencv/base64
        :return:
        """
        # self.display()
        img = self.device.screenshot(fmt='pillow')  # TODO
        l, t, r, b = self.bounds.unpack()
        ele_img = img.crop((l, t, r, b))
        if filename:
            ele_img.save(filename)
        if fmt == 'pillow':
            return ele_img
        elif fmt == 'base64':
            return image.pillow2base64(ele_img)
        return ele_img

    def save_image(self, name):
        """
        保存图片

        :param name:
        :return:
        """
        # self.display()
        time.sleep(0.5)
        img = self.device.screenshot.pillow
        l, t, r, b = self.bounds.unpack()
        ele_img = img.crop((l, t, r, b))
        ele_img.save(name)

    def offset(self, **kwargs):
        """
        根据偏移量解析并获取页面元素

        用法：

            1. d(text='Switch').offset(x=0.9, ele_name='{} icon').click()
            表示找到text显示为“Switch”元素后，将其x坐标替换为0.9，根据新得到的坐标找到目标元素并点击，
            新找到的元素命名为ele_name （支持格式化），这里会显示为 Switch icon

        :param kwargs: 支持的参数同 offset_pos, 额外支持 ele_name
        :return:
        """
        if not kwargs:
            return self
        kwargs['relative'] = False
        self.scroll()
        time.sleep(1)
        x, y = self.device(selector=self.selector).offset_pos(**kwargs)
        ele = self.device.page.parse(x, y)
        if not ele:
            ele = AndroidElement(device=self.device)
        ele.device = self.device
        ele._beacon = self
        ele_name = kwargs.pop('ele_name', None)
        if ele_name:
            ele_name = ele_name.format(self._name or self.text or self.content_desc)
        ele._name = ele_name or ele.text or ele.content_desc or self.name
        return ele

    def offset_pos(self, **kwargs):
        """
        根据偏移量得到新的坐标值，一般来配合页面解析来处理不容易定位的元素

        用法：

        1、 重设坐标：p = ele.offset_pos(x=0.9) 一般传入x 或者 y 重设并获得新的坐标

        2、 坐标偏移：p = ele.offset_pos(ox=-0.3, oy=0.01, align=Alignment.TOP_LEFT) 相对于元素左上角左偏0.3，右偏0.01，
        align默认为Alignment.CENTER

        3、 偏移和重设混合：p = ele.offset_pos(x=0.3, oy=0.01, align=Alignment.TOP_LEFT)

        :param kwargs:
        :return:
        """
        x, y = self.position
        _x, _y = kwargs.pop('x', None), kwargs.pop('y', None)
        _x, _y = self.device.abs_pos(_x, _y)
        align = kwargs.pop('align', Alignment.CENTER)
        _ox, _oy = kwargs.pop('ox', 0) or 0, kwargs.pop('oy', 0) or 0
        _ox, _oy = self.device.abs_pos(_ox, _oy)
        left, top, right, bottom = self.bounds.unpack()
        if align == Alignment.CENTER:
            x, y = x + _ox, y + _oy
        elif align == Alignment.LEFT:
            x, y = left + _ox, y + _oy
        elif align == Alignment.RIGHT:
            x, y = right + _ox, y + _oy
        elif align == Alignment.TOP:
            x, y = x + _ox, top + _oy
        elif align == Alignment.BOTTOM:
            x, y = x + _ox, bottom + _oy
        elif align == Alignment.TOP_LEFT:
            x, y = left + _ox, top + _oy
        elif align == Alignment.TOP_RIGHT:
            x, y = right + _ox, top + _oy
        elif align == Alignment.BOTTOM_LEFT:
            x, y = left + _ox, bottom + _oy
        elif align == Alignment.BOTTOM_RIGHT:
            x, y = right + _ox, bottom + _oy

        x, y = _x or x, _y or y
        relative = kwargs.pop('relative', False)
        return self.device.rel_pos(x, y) if relative else self.device.abs_pos(x, y)

    def from_parent(self, **kwargs):
        """
        用于获取当前元素的兄弟节点元素

        :param kwargs: 定位字典
        :return:
        """
        child_id = self.u2obj.jsonrpc.getFromParent(self.selector, Selector(**kwargs))
        obj_info = self.u2obj.jsonrpc.objInfo(child_id)
        return AndroidElement(info=obj_info, device=self.device)

    def sibling(self, **kwargs):
        """
        与from_parent本质一样

        :param kwargs:
        :return:
        """
        return AndroidElement(selector=self.selector.clone().sibling(**kwargs), device=self.device)

    def child_by_text(self, text, **kwargs):
        """
        获取text属性为给定值的子元素

        :param text:
        :param kwargs:
        :return:
        """
        if "allow_scroll_search" in kwargs:
            allow_scroll_search = kwargs.pop("allow_scroll_search")
            name = self.u2obj.jsonrpc.childByText(self.selector, Selector(**kwargs), text, allow_scroll_search)
        else:
            name = self.u2obj.jsonrpc.childByText(self.selector, Selector(**kwargs), text)
        return AndroidElement(name, device=self.device)

    def child_by_description(self, txt, **kwargs):
        if "allow_scroll_search" in kwargs:
            allow_scroll_search = kwargs.pop("allow_scroll_search")
            name = self.u2obj.jsonrpc.childByDescription(self.selector,
                                                         Selector(**kwargs), txt,
                                                         allow_scroll_search)
        else:
            name = self.u2obj.jsonrpc.childByDescription(self.selector,
                                                         Selector(**kwargs), txt)
        return AndroidElement(name, device=self.device)  # TODO  原生支持以字符串作为selector，有矛盾需要处理

    def child_by_instance(self, inst, **kwargs):
        # need test
        ele_name = kwargs.pop('ele_name', None)
        _id = self.u2obj.jsonrpc.childByInstance(self.selector, Selector(**kwargs), inst)
        info = self.u2obj.jsonrpc.objInfo(_id)
        return AndroidElement(device=self.device, info=info, name=ele_name)

    def child(self, **kwargs):
        """
        获取子元素

        :param kwargs:
        :return:
        """
        return self.device(selector=self.selector.clone().child(**kwargs))

    def pinch_in(self, percent=100, steps=50):
        """
        缩小手势

        :param percent:
        :param steps:
        :return:
        """
        if self._info:
            _dict = {}
            if self.text:
                _dict['text'] = self.text
            if self.content_desc:
                _dict['content'] = self.content_desc
            if self.resource_id:
                _dict['id'] = self.resource_id
            if not _dict:
                AndroidElement(name=self.name, **_dict).pinch_in(percent, steps)
            else:
                raise AdbError('Cannot pinch this element right now! Please wait new version!')
        elif isinstance(self.selector, Selector):
            self.u2obj.jsonrpc.pinchIn(self.selector, percent, steps)
            logger.info(f'Pinch in: {self.name}')
        else:
            raise ElementNotFoundError(self.name)

    def pinch_out(self, percent=100, steps=50):
        """
        放大手势，比如对某个图片

        :param percent:
        :param steps:
        :return:
        """
        if self._info:
            _dict = {}
            if self.text:
                _dict['text'] = self.text
            if self.content_desc:
                _dict['content'] = self.content_desc
            if self.resource_id:
                _dict['id'] = self.resource_id
            if not _dict:
                AndroidElement(name=self.name, **_dict).pinch_out(percent, steps)
            else:
                raise AdbError('Cannot pinch this element right now! Please wait new version!')

        elif isinstance(self.selector, Selector):
            self.u2obj.jsonrpc.pinchOut(self.selector, percent, steps)
            logger.info(f'Pinch out: {self.name}')
        else:
            raise ElementNotFoundError(self.name)

    def wait(self, exists=True, timeout=None):
        """
        等待元素出现或消失，此方法不会自动滑动，使用时请注意

        :param exists: True, 等待出现；False, 等待消失；默认为True
        :param timeout: 超时时间，单位秒
        :return: True/False, 如果超时，返回 False
        """
        if isinstance(self.selector, Selector):
            if timeout is None:
                timeout = self.timeout or 0
            http_wait = timeout + 10
            if exists:
                try:
                    return self.u2obj.jsonrpc.waitForExists(self.selector, int(timeout * 1000), http_timeout=http_wait)
                except requests.ReadTimeout as e:
                    logger.warning(f"waitForExists readTimeout: {str(e)}")
                    return False
            else:
                try:
                    return self.u2obj.jsonrpc.waitUntilGone(self.selector, int(timeout * 1000), http_timeout=http_wait)
                except requests.ReadTimeout as e:
                    logger.warning(f"waitForExists readTimeout: {str(e)}")
                    return False
        else:
            logger.debug(f'abnormal element????????!!!!!!!!!')

    def wait_gone(self, timeout=None):
        """
        等待元素消失

        :param timeout: 超时时间
        :return:
        """
        timeout = timeout or self.timeout or settings.ELEMENT_WAIT_TIMEOUT
        return self.wait(exists=False, timeout=timeout)

    def assert_info(self, **kwargs):
        """
        断言元素属性信息

        :param kwargs: 属性期望值，如 checked=True, enabled=False 可能希望复选框默认选中且不可取消
        :return:
        """
        result = True
        actual_info = {}
        for k, v in kwargs.items():
            actual = getattr(self, k)
            actual_info[k] = actual
            result = result and actual == v
        expected, actual = Dict(**kwargs).to_query_str(), Dict(**actual_info).to_query_str()
        if not result:
            raise TestFailedError(f'Assert info of {self.name}, expected: {expected}, actual: {actual}')
        logger.info(f'Element info of "{self.name}" is as expected: {expected}')

    def assert_exist(self):
        """
        断言元素是否存在

        :return:
        """
        if self.__scroll:
            self.scroll()
        else:
            if not self.exists:
                raise ElementNotFoundError(self.selector)
        logger.info(f'Assert element exists: {self.name}')

    def assert_image(self, expected_image, similarity=0.8):
        """
        断言图片相似度

        :param expected_image: 对比图片，路径或者opencv对象
        :param similarity: 相似度，默认0.8
        :return:
        """
        # self.display()
        time.sleep(0.5)
        img = self.device.screenshot.pillow
        l, t, r, b = self.bounds.unpack()
        ele_img = img.crop((l, t, r, b))  # TODO
        if isinstance(expected_image, str):
            logger.info(f'Found expected image: {expected_image}')
            target_image = Image.open(expected_image)
        elif isinstance(expected_image, Image):
            target_image = expected_image
        else:
            raise TestError("不合法的期望图片！")
        result = image.calc_similarity(ele_img, target_image)
        expected_image_name = os.path.basename(expected_image)
        if result < similarity:
            data = {
                f'{self.device.name}-actual': ele_img,
                f'{self.device.name}-expected': target_image
            }
            raise TestFailedError(f'Image assertion failed. Element: {self.name}, '
                                  f'expected: {expected_image_name}, '
                                  f'the similarity is expected {similarity} but got {result}',
                                  data=data)
        logger.info(f'[{self.device.serial} ({self.device.name})] '
                    f'Assert image of element "{self.name}" with {expected_image_name}, '
                    f'expected similarity is {similarity}, '
                    f'actual similarity is {result}.')

    def assert_not_exist(self):
        """
        断言元素不存在

        :return:
        """
        if self.__scroll:
            try:
                self.scroll()
                raise TestFailedError(f'Element "{self.name}" exists actually.')
            except (ElementNotFoundError, AssertionError):
                pass
        else:
            assert not self.exists, f'Element "{self.name}" exists actually.'
        logger.info(f'Assert element not exist: {self.name}')

    def __getitem__(self, index):
        if isinstance(index, str):
            raise IndexError("Index is not supported when UiObject returned by child_by_xxx")
        selector = self.selector.clone()
        if index < 0:
            index = self.count
        selector.update_instance(index)
        return AndroidElement(device=self.device, selector=selector, name=self._name)

    def __iter__(self):
        length = self.count
        for i in range(length):
            yield self[i + 1]
