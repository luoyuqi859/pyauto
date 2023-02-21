#!/usr/bin/env python
# -*- ecoding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: log
@Created: 2023/2/17 14:26
"""

from functools import wraps
import os
import datetime

import loguru

from conf import settings


# 单例类的装饰器
def singleton_class_decorator(cls):
    """
    装饰器，单例类的装饰器
    """
    # 在装饰器里定义一个字典，用来存放类的实例。
    _instance = {}

    # 装饰器，被装饰的类
    @wraps(cls)
    def wrapper_class(*args, **kwargs):
        # 判断，类实例不在类实例的字典里，就重新创建类实例
        if cls not in _instance:
            # 将新创建的类实例，存入到实例字典中
            _instance[cls] = cls(*args, **kwargs)
        # 如果实例字典中，存在类实例，直接取出返回类实例
        return _instance[cls]

    # 返回，装饰器中，被装饰的类函数
    return wrapper_class


def singleton(o):
    """单例实现，综合装饰器和__new__方式，不会隐匿掉原来的类对象"""
    instances = {}

    old_new = getattr(o, '__new__')

    def __new__(cls, *args, **kwargs):
        if cls not in instances:
            if old_new == object.__new__:
                instance = object.__new__(cls)
            else:
                instance = old_new(cls, *args, **kwargs)
            instances[cls] = instance

        return instances[cls]

    o.__new__ = __new__

    return o


@singleton_class_decorator
class Logger:
    def __init__(self):
        self.logger_add()

    def get_log_path(self):
        # 项目目录
        project_path = settings.root_path
        # 项目日志目录
        project_log_dir = os.path.join(project_path, 'log')
        # 日志文件名
        project_log_filename = 'runtime_{}.log'.format(datetime.date.today())
        # 日志文件路径
        project_log_path = os.path.join(project_log_dir, project_log_filename)
        # 返回日志路径
        return project_log_path

    def logger_add(self):
        loguru.logger.add(
            # 水槽，分流器，可以用来输入路径
            sink=self.get_log_path(),
            # 日志创建周期
            rotation='500MB',
            # 保存
            retention='10 days',
            # 文件的压缩格式
            compression='zip',
            # 编码格式
            encoding="utf-8",
            # 具有使日志记录调用非阻塞的优点
            enqueue=True
        )

    @property
    def get_logger(self):
        return loguru.logger


'''
# 实例化日志类
'''
logger = Logger().get_logger

if __name__ == '__main__':
    logger.debug('调试代码')
    logger.info('输出信息')
    logger.success('输出成功')
    logger.warning('错误警告')
    logger.error('代码错误')
    logger.critical('崩溃输出')

    """
    在其他.py文件中，只需要直接导入已经实例化的logger类即可
    例如导入访视如下：
    from utils.logger import logger
    然后直接使用logger即可
    """
    logger.info('----原始测试----')
