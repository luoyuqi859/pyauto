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


class BaseError(Exception):
    """Base class for exceptions in this module."""

    def __init__(self, message=""):
        self.message = message

    def __repr__(self):
        return repr(self.message)


class RootError(BaseError):
    """"""


class FileNotExistError(BaseError):
    """file does not exist."""


class InvalidMatchingMethodError(BaseError):
    """
        This is InvalidMatchingMethodError BaseError
        When an invalid matching method is used in settings.
    """


class AdbError(BaseError):
    """"""


class ElementNotFoundError(BaseError):
    """element not found"""


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
