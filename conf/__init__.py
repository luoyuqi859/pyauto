#!/usr/bin/env python
# -*- ecoding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: __init__.py
@Created: 2023/2/16 18:30
"""
from conf import config


class Settings(dict):
    """
    设置
    """

    def __init__(self, settings_module):
        super().__init__()
        self.apply(settings_module)

    def __getattr__(self, item):
        if item.startswith('_'):
            return super().__getattribute__(item)
        value = self.get(item)
        if value is not None:
            return value
        else:
            raise "没有该参数,请检查config.py是否配置"

    def apply(self, settings_module):
        """
        应用配置
        :param settings_module: 配置所在的module
        :return:
        """
        for name in dir(settings_module):
            if name.startswith('_'):
                continue
            v = getattr(settings_module, name)
            self[name] = v
        return self


settings = Settings(config)

if __name__ == '__main__':
    f = settings.root_path
