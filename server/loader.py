#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: loader
@Created: 2023/3/3 18:33
"""
import os
import sys
import traceback

from server import host
from server.host import local_host
from server.repo import Repo
from utils import py


class TestLoader:
    """
    测试加载器
    """
    def __init__(self):
        self.errors = []

    def load_path(self, path, include_objects=False):
        """
        从指定路径加载脚本仓库
        :param path:
        :param include_objects: 是否包括测试对象：app/page/module/function/script...
        :return:
        """
        root, _ = host.parse_repo_root(path)
        if root.parent in sys.path:
            sys.path.remove(root.parent)
            sys.path.insert(0, root.parent)
        with self:
            module = py.get_object(root)
        if include_objects:
            # get_repo(module.__name__)
            for path, dirs, files in os.walk(root):
                for d in dirs:
                    if d.startswith(('_', '.')):
                        continue
                    test_name = os.path.join(path, d)
                    with self:
                        py.get_object(test_name)
                for f in files:
                    if f.startswith(('_', '.')) or not f.endswith('.py'):
                        continue
                    test_name = os.path.join(path, f)
                    with self:
                        py.get_object(test_name)
            for repo in local_host.repos:
                if repo.name == module.__name__:
                    repo.reload()
                    return repo
        else:
            return Repo(module)
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            error = dict(
                err_type=exc_type.__name__,
                err_message=str(exc_val),
                err_detail=traceback.format_tb(exc_tb)
            )
            self.errors.append(error)
        return self
