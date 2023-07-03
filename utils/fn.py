#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: fn
@Created: 2023/6/30 11:11
"""
import inspect
import re
import sys


class _Argument:
    def __init__(self, name, required, default=None):
        self.name = name
        self.required = required
        self.default = default

    def __repr__(self):
        return f'<Arg {self.name}{"" if self.required else "=" + str(self.default)}>'


class ArgumentError(Exception):
    """"""


def run(f, *args, **kwargs):
    if f:
        return Func(f)(*args, **kwargs)


def get_name(func):
    if inspect.isfunction(func):
        name = re.search(r'<function (\S+) at', str(func)).groups()[0]
    elif inspect.ismethod(func):
        name = re.search(r'<bound method (\S+) of', str(func)).groups()[0]
    elif inspect.ismodule(func):
        return func.__name__
    else:
        return func.__class__.__name__
    return name


def get_class(routine, module=None):
    if inspect.isclass(routine):
        return routine
    module = module or inspect.getmodule(routine)
    name = get_name(routine)
    class_name = name[:name.rindex('.')] if '.' in name else None
    if class_name:  # 如果是类方法
        # reload(module)
        cls = getattr(module, class_name, None)
        return cls


class Func:
    def __init__(self, fn):
        self.fn = fn  # 可能是实现了__call__的类
        self.default_kw = {}
        self.called_by_defaults = True  # 是否使用默认值调用，用于恢复执行

    @property
    def name(self):
        if self.cls:
            if inspect.isclass(self.fn):
                return f'{self.cls.__name__}.__init__'
            return f'{self.cls.__name__}.{self.fn.__name__}'
        return get_name(self.fn)

    def __call__(self, *args, **kwargs):
        self.module = inspect.getmodule(self.fn)
        self.cls = get_class(self.fn, module=self.module)

        if inspect.isclass(self.fn):
            full_args = inspect.getfullargspec(self.fn.__init__)
            varargs, varkw = full_args.varargs, full_args.varkw
            if self.fn.__init__ == object.__init__:
                varargs, varkw = None, None
        else:
            full_args = inspect.getfullargspec(self.fn)
            varargs, varkw = full_args.varargs, full_args.varkw
        _args = full_args.args

        if any([
            inspect.ismethod(self.fn), # 如果是实例方法，则忽略掉第一个参数 self
            inspect.isclass(self.fn),  # 如果是类
            (not inspect.ismodule(self.fn) and not inspect.isfunction(self.fn))  # 如果是__call__
        ]):
            _args = full_args.args[1:]

        actual_args, actual_kw, args = [], {}, list(args)
        for i in range(len(_args)):
            name = _args[i]
            required = len(full_args.defaults or []) < len(_args) - i
            index = len(_args) - i
            if not required:
                default = full_args.defaults[-index] if full_args.defaults else None
                self.default_kw[name] = default
            else:
                default = None
            if name in kwargs:
                if required:
                    actual_args.append(kwargs[name])
                else:
                    actual_kw[name] = v = kwargs[name]
                    if default != v:
                        self.called_by_defaults = False
            else:
                if args:
                    v = args.pop(0)
                    if not required and default != v:
                        self.called_by_defaults = False
                    actual_args.append(v)
                else:
                    if required:
                        raise TypeError(f"{self.name}() missing 1 required positional argument: '{name}'")
        return self.fn(*actual_args, **actual_kw)


def get_target_py():
    try:
        raise Exception
    except Exception:
        f_back = sys.exc_info()[2].tb_frame.f_back.f_back
        module = inspect.getmodule(f_back)
        lineno = f_back.f_lineno
        method = f_back.f_code.co_name
        filename = f_back.f_code.co_filename.replace('\\', '/')
        return module, filename, method if method != '<module>' else None, lineno
