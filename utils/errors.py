#!/usr/bin/env python
# -*- ecoding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: errors
@Created: 2023/2/21 13:23
"""

import traceback
from contextlib import contextmanager

from utils.log import logger


class TestError(Exception):
    def __init__(self, message, *args, **kwargs):
        self.message = message
        self.data = kwargs.pop('data', None)
        if args or kwargs:
            self.message = message.format(*args, **kwargs)

    # def __str__(self):
    #     return f'{self.__class__.__name__}({self.message})'


class TestFailedError(TestError):
    """"""

    def __init__(self, *args, optional=False, **kwargs):
        self.optional = optional
        super().__init__(*args, **kwargs)


class TestBlockedError(TestError):
    """"""


class TestSkippedError(TestError):
    """"""


class ManualError(TestError):
    """"""


class InvalidTestError(TestError):
    """"""


@contextmanager
def ignore(*errors):
    """
    执行代码块并忽略指定异常
    :param errors: 要忽略的错误类型，不指定则意味着忽略所有的异常
    :return:
    """
    try:
        yield
    except errors or Exception:
        logger.error(traceback.format_exc())
