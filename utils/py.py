#! /usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: py
@Created: 2023/2/21 13:22
"""
import os
import re
import sys
import traceback
from types import FunctionType, MethodType, ModuleType

from utils.path_fun import Path


def get_info(o):
    if isinstance(o, type):
        return (
            o.__name__,
            f"{getattr(o, '__module__')}.{o.__name__}",
            o.__doc__
        )
    elif isinstance(o, FunctionType):
        name = re.search(r'<function (\S+) at', str(o)).groups()[0]
        return (
            name,
            f"{getattr(o, '__module__')}.{name}",
            o.__doc__
        )
    elif isinstance(o, MethodType):
        caller = getattr(o, '__self__')
        name = f"{caller.__class__.__name__}.{o.__name__}"
        return (
            name,
            f"{getattr(caller.__class__, '__module__')}.{name}",
            o.__doc__
        )
    elif isinstance(o, ModuleType):
        return o.__name__, o.__name__, o.__doc__
    else:
        if os.path.exists(str(o)):
            name = os.path.basename(str(o))
        else:
            name = getattr(o, 'name', str(o))
        return name, name, getattr(o, 'doc', None)


def find_root(path):
    """
    查找py工程根目录
    :param path:
    :return:
    """
    path = os.path.abspath(path)
    path = Path(path)
    root = path.parent if os.path.isfile(str(path)) else path
    while os.path.exists(os.path.join(root, '__init__.py')):
        root = root.parent
    return root


def insert(root):
    if root in sys.path:
        sys.path.remove(root)
    sys.path.insert(0, root)
    return root


def load_file(path):
    assert path.endswith('.py'), 'Can only load py!'
    root = find_root(path)
    insert(root)
    nodes = re.sub(r'[/\\]', '.', path[:-3].replace(root, '')).strip('.')
    name = '.'.join(nodes)
    return get_object(name)


def get_module(name):
    module = __import__(name)
    nodes = name.split('.')
    for node in nodes[1:]:
        module = getattr(module, node)
    return module


def get_object(name: str):
    """
    根据名称获取对象
    :param name: 对象全名称，比如 demo.test.TestClass.my_method
    :return: module/type/function
    """
    if not name:
        return
    if os.path.exists(name) and os.path.isabs(name):
        root = find_root(name)
        insert(root)
        if os.path.isfile(name):
            name = re.sub(r'[/\\]', '.', name[:-3][len(root) + 1:])
        else:
            name = re.sub(r'[/\\]', '.', name[len(root) + 1:])
        return get_object(name)
    else:
        nodes = name.split('.')
        o, module_name = None, ''
        for i in range(len(nodes)):
            module_name = '.'.join(nodes[:i + 1])
            try:
                o = __import__(module_name)
                i += 1
            except ModuleNotFoundError as e:
                break
        if o:
            for node in nodes[1:]:
                o = getattr(o, node)
        if not o:
            raise ModuleNotFoundError(module_name)
        return o


def load_path(path):
    """
    加载指定路径的python，并返回其中的错误
    :return: 脚本错误
    """
    errors = []
    path = Path(path)
    root = find_root(path)
    if root in sys.path:
        sys.path.remove(root)
    sys.path.insert(0, root)
    for name, file in path.walk_files('*.py'):
        if name == '__init__.py':
            package_name = re.sub(r'[/\\]', '.', file.parent.replace(root, '')).strip('.')
        else:
            package_name = re.sub(r'[/\\]', '.', file[:-3].replace(root, '')).strip('.')
        try:
            __import__(package_name)
        except (ModuleNotFoundError, SyntaxError):
            errors.append(traceback.format_exc())
        except Exception:
            pass  # 忽略其他错误
    return errors


class ObjectNotFoundError(Exception):
    """"""

    def __init__(self, o):
        super().__init__(str(o))
