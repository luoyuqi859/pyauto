#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: proxy
@Created: 2023/6/30 11:12
"""
from utils import fn


class Proxy:
    def __init__(self, o):
        self._o = o
        self._method = None

    def __getattr__(self, item):
        v = getattr(self._o, item, None)
        if callable(v):
            self._method = v
            return self
        return v

    def __call__(self, *args, **kwargs):
        if self._method:
            return fn.run(self._method, *args, **kwargs)

    def __repr__(self):
        return f'<Proxy {self._o}>'
