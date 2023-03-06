#! /usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: o
@Created: 2023/3/4
"""
import inspect

from server.core.host import local_host


class _TestObject:
    def __init__(self):
        self.category = None

    @property
    def app(self):
        self.category = 'app'
        return self

    def script(self, app_class=None, **attrs):
        """
        将函数或者类标记为测试脚本
        :param app_class:
        :param attrs:
        :return:
        """

        def deco(cls):
            # self._inject_object_caseset(cls, **attrs)  # 注册增加属性,用于筛选用例
            self._inject_object_info(cls, **attrs)
            local_host.add_object(cls, 'script_list')
            cls.status_classes = []
            return cls

        return deco

    def __getattr__(self, item):
        self.category = item
        return self

    @classmethod
    def _inject_object_info(cls, o, **attrs):
        for k, v in attrs.items():
            setattr(o, k, v)
        if not hasattr(o, 'name'):
            o.name = o.__name__
        o.test_name = f'{inspect.getmodule(o).__name__}.{o.__name__}'  # 将来废弃
        o.pytest_name = f'{inspect.getfile(o)}::{o.__name__}'
        # o.source_code = inspect.getsource(o)
        o.doc = o.__doc__.strip() if o.__doc__ else None

    @classmethod
    def _inject_object_caseset(cls, o, **attrs):
        """
        注册类中的用例
        :param o:
        :param attrs:
        :return:
        """
        if isinstance(o, type):
            o.case = {}
            for i in dir(o):
                if i.startswith(('test', 'Test')):
                    fn = getattr(o, i)
                    doc = fn.__doc__
                    source_code = inspect.getsource(fn)
                    o.case[i] = (doc, source_code)

    def __call__(self, **attrs):
        def deco(cls):
            self._inject_object_info(cls, **attrs)
            local_host.add_object(cls, self.category + '_list')
            cls.status_classes = []

            return cls

        return deco


test_object = _TestObject()
