#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: test_xxx
@Created: 2023/3/4
"""
from server.core.o import test_object


@test_object.script()
def test_xxx():
    print("xxxxxx")


@test_object.script()
def test_xxx1():
    print("xxxxxx")


@test_object.script()
def test_xxx2():
    print("xxxxxx")
