#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: collector
@Created: 2023/3/17 12:37
"""

import os
import importlib.util
import inspect


class MyCollector:
    def __init__(self, path):
        self.path = path
        self.items = {}

    def collect(self):
        for root, dirs, files in os.walk(self.path):
            for file in files:
                if file.startswith("test_") and file.endswith(".py"):
                    module_path = os.path.join(root, file)
                    module_name = os.path.splitext(file)[0]
                    spec = importlib.util.spec_from_file_location(module_name, module_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    self._collect_from_module(module)

    def _collect_from_module(self, module):
        for name, obj in inspect.getmembers(module):
            if name.startswith("test_") or name.endswith("_test"):
                if inspect.isfunction(obj) or inspect.ismethod(obj):
                    self.items[f"{module.__file__}::{name}"] = obj
            elif inspect.isclass(obj):
                for method_name, method in inspect.getmembers(obj):
                    if method_name.startswith("test_") or method_name.endswith("_test"):
                        if inspect.isfunction(method) or inspect.ismethod(method):
                            full_name = f"{module.__file__}::{obj.__name__}::{method_name}"
                            self.items[full_name] = method
