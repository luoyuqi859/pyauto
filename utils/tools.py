#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: tools
@Created: 2023/3/2 14:33
"""
import os
import time
import zipfile


class TimeUtils(object):
    UnderLineFormatter = "%Y_%m_%d_%H_%M_%S"
    NormalFormatter = "%Y-%m-%d %H-%M-%S"
    ColonFormatter = "%Y-%m-%d %H:%M:%S"

    # 文件路径要用这个，mac有空格，很麻烦
    @staticmethod
    def getCurrentTimeUnderline():
        return time.strftime(TimeUtils.UnderLineFormatter, time.localtime(time.time()))

    @staticmethod
    def getCurrentTime():
        return time.strftime(TimeUtils.NormalFormatter, time.localtime(time.time()))

    @staticmethod
    def formatTimeStamp(timestamp):
        return time.strftime(TimeUtils.NormalFormatter, time.localtime(timestamp))

    @staticmethod
    def getTimeStamp(time_str, format):
        timeArray = time.strptime(time_str, format)
        # 转换成时间戳
        return time.mktime(timeArray)

    @staticmethod
    def is_between_times(timestamp, begin_timestamp, end_timestamp):
        if begin_timestamp < timestamp and timestamp < end_timestamp:
            return True
        else:
            return False

    @staticmethod
    def get_interval(begin_timestamp, end_timestamp):
        '''
        :param begin_timestamp:
        :param end_timestamp:
        :return:求起止时间戳之间的时间间隔 ，返回H,浮点数
        '''
        interval = end_timestamp - begin_timestamp
        return round(float(interval) / (60 * 60))


def ms2s(value):
    return round(value / 1000.0, 2)


def transfer_temp(temp):
    return round(temp / 10.0, 1)


def mV2V(v):
    return round(v / 1000.0, 2)


def uA2mA(c):
    return round(c / 1000.0, 2)
