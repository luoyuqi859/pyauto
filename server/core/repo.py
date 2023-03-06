#! /usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: repo
@Created: 2023/3/3 17:57
"""
import inspect
from importlib import reload

from conf import config
from utils.path_fun import Path


class Repo(dict):
    """
    脚本仓库
    """

    def __init__(self, module, git_path=None):
        super().__init__()
        assert module
        self.__module = module
        self.path = Path(module.__file__).parent
        self.name = module.__name__

    @property
    def git_path(self):
        if not self._git_path:
            self._git_path = Path(str(self.path))
            while not (self._git_path / '.git').exists:
                self._git_path = self._git_path.parent
        return self._git_path

    def add(self, o, category=None):
        if inspect.isclass(o):
            category = category or getattr(o, 'category', None)
        elif inspect.isfunction(o):
            pass
        elif inspect.ismodule(o):
            category = category or getattr(o, 'category', 'module')

        if category and not category.startswith('_'):
            if category not in self:
                self[category] = set()
            self.get(category).add(o)

    def reload(self):
        if self.__module:
            self.__module = reload(self.__module)

    def __getattr__(self, item):
        return self[item]

    def __getitem__(self, item):
        if item.startswith('_'):
            return super().__getattribute__(item)
        v = dict.get(self, item)
        if not v:
            v = getattr(self.__module, item, None)
        if not v:
            return getattr(config, item, None)
        return v

    def __eq__(self, other):
        if inspect.ismodule(other):
            return hash(self) == hash(other.__file__)
        return hash(self) == hash(other)

    def __hash__(self):
        return hash(self.path)

    def __repr__(self):
        return f'<Repo {self.name}>'
