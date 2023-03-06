#! /usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: page
@Created: 2023/2/25
"""

from xml.sax import parseString

from uiauto.android.parse import Handler
from uiauto.android.parse import Bounds, AndroidPageParser
from uiauto.android.u2.element import AndroidElement
from utils.check import Check
from utils.errors import RootError, ElementNotFoundError


class AndroidPage:
    def __init__(self, source=None, device=None):
        super().__init__()
        self._source = source
        self.device = device  # 这里的设备对象可以是adb或者AndroidDevice
        self._root = None
        self.__display_bounds = None

    @property
    def source(self):
        source = self._source or self.device.d.dump_hierarchy()
        if not source:
            raise RootError(f'无法获取设备页面内容，请root设备或者恢复出厂设置，如果还不能解决，可考虑刷机！')
        return source

    @property
    def display_bounds(self):
        if not self.__display_bounds:
            try:
                f = "com.android.systemui:id/gm_car_status_bar"
                d = "com.android.systemui:id/status_bar"
                status_bar_bounds = self.device(resourceId=f, timeout=0).bounds
            except ElementNotFoundError:
                status_bar_bounds = Bounds(0, 0, 0, 0)
            try:
                nav_bar_bounds = self.device(resourceId='com.android.systemui:id/navigation_bar_frame',
                                             timeout=0).bounds
            except ElementNotFoundError:
                nav_bar_bounds = Bounds(0, self.device.window_size[1], 0, 0)
            self.__display_bounds = Bounds(0, status_bar_bounds.bottom, self.device.info.width, nav_bar_bounds.top)

        return self.__display_bounds

    def select(self, **kwargs):
        attr_expression = ''.join(["[@" + k + '="' + v + '"]' for k, v in kwargs.items()])
        xpath = f'//*{attr_expression}'
        parser = AndroidPageParser(self.source)
        node = parser.one(xpath)
        if node:
            ele = AndroidElement(device=self.device)
            ele.info.update(**node)
            return ele

    def parse_page(self):
        pass

    def find(self, **kwargs) -> 'AndroidElement':
        def _find_node(node):
            if Check(node).test(**kwargs):
                node._adb = self.device
                result['result'] = node
                raise Exception('found!')

        result = {}
        handler = Handler(_find_node)
        try:
            parseString(self.source, handler)
        except:
            pass
        return result.get('result')

    def parse(self, x, y):
        return self.find_element(x, y)

    def find_element(self, x, y):
        """
        解析获取位于 (x, y) 坐标的元素
        :param x:
        :param y:
        :return: AndroidElement
        """
        node = self.__parse_pos(x, y)
        ele = AndroidElement(device=self.device)
        ele.info.update(**node)
        return ele

    def parse_selector(self, x, y):
        # 解析到位于该坐标的元素之后，尝试得到选择器
        node = self.__parse_pos(x, y)
        if node.text:
            if self.source.count(f'text="{node.text}"') < 2:
                return dict(text=node.text)
        if node['description']:
            if self.source.count(f'description="{node["description"]}"') < 2:
                return dict(content=node['description'])
        if node['resourceId']:
            if self.source.count(f'resourceId="{node["resourceId"]}"') < 2:
                return dict(resourceId=node['resourceId'])

        # 如果无法获得有效的常规选择器，则从上下文解析，比如利用子元素或者父元素
        pass

    def __parse_pos(self, x, y):
        x, y = self.device.abs_pos(x, y)
        parser = AndroidPageParser(self.source)
        node = parser.find_node(x, y)
        if not node:
            raise ElementNotFoundError(f'{x}, {y}')
        return node

    def crawl(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self

    def __str__(self):
        return self._source
