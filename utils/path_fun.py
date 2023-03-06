#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: path_fun
@Created: 2023/2/17 14:37
"""

import fnmatch
import os
import re
import shutil
import sys
from datetime import datetime
from typing import Text


class Path(str):
    def __new__(cls, o, *args, **kwargs):  # 重写 __new__ 否则无法正常重写 __init__
        return super().__new__(cls, o)

    @property
    def basename(self):
        return os.path.basename(self)

    @property
    def extension(self):
        basename = self.basename
        try:
            dot_index = basename.rindex('.')
        except ValueError:
            dot_index = None
        return basename[dot_index:] if dot_index else None

    @property
    def name_without_extension(self):
        """名称（不包含扩展名）"""
        return self.basename.rsplit('.', maxsplit=1)[0]

    @property
    def size(self):
        return os.path.getsize(self)

    @property
    def create_time(self):
        return datetime.fromtimestamp(os.path.getctime(self))

    @property
    def mod_time(self):
        return datetime.fromtimestamp(os.path.getmtime(self))

    @property
    def last_access_time(self):
        return datetime.fromtimestamp(os.path.getatime(self))

    @property
    def isfile(self):
        return os.path.isfile(self)

    @property
    def isdir(self):
        return os.path.isdir(self)

    @property
    def ismount(self):
        """是否盘符"""
        return os.path.ismount(self)

    @property
    def parent(self):
        return self.__class__(os.path.dirname(str(self))) if not self.ismount else None

    @property
    def exists(self):
        return os.path.exists(self)

    @property
    def nodes(self):
        """将路径拆分成节点列表"""
        return re.split(r'[\\/]', self)

    def info(self, related: str = None):
        info = dict(name=self.basename,
                    path=self,
                    size=self.size,
                    create_time=self.create_time,
                    mod_time=self.mod_time,
                    last_access_time=self.last_access_time)
        if self.isfile:
            info['size'] = self.size
            info['type'] = 'file'
        else:
            info['type'] = 'dir'
        if related:
            related = related.strip(os.sep)
            info['relative_path'] = self.replace(related, '')
        return info

    def search(self, pattern):
        if not pattern:
            raise PathError('Pattern for searching is required!')
        for name, item in self.list():
            if item.isfile and fnmatch.fnmatch(item.basename, pattern):
                yield item
            if item.isdir:
                for f in item.search(pattern):
                    yield f

    def list(self, pattern=None):
        for name in os.listdir(self):
            if pattern is None or (pattern and fnmatch.fnmatch(name, pattern)):
                yield name, self.__class__(os.path.join(self, name))

    def files(self, pattern=None):
        for _, item in self.list(pattern):
            if item.isfile:
                yield item

    def dirs(self, pattern=None):
        for _, item in self.list(pattern):
            if item.isdir:
                yield item

    def walk_files(self, pattern=None, ):
        for root, dirs, files in os.walk(self):
            for file in files:
                if pattern is None or (pattern and fnmatch.fnmatch(file, pattern)):
                    yield file, self.__class__(root) / file

    def walk(self, pattern=None):
        for root, dirs, files in os.walk(self):
            for d in dirs:
                if pattern is None or (pattern and fnmatch.fnmatch(d, pattern)):
                    yield d, self.__class__(root) / d, 'dir'
            for file in files:
                if pattern is None or (pattern and fnmatch.fnmatch(file, pattern)):
                    yield file, self.__class__(root) / file, 'file'

    def upstream_search(self, pattern):
        if not pattern:
            raise PathError('Pattern for searching is required!')
        if self.isfile:
            for name, f in self.parent.upstream_search(pattern):
                yield name, f
        else:
            for name, f in self.list(pattern):
                yield name, f
            if self.parent:
                for name, f in self.parent.upstream_search(pattern):
                    yield name, f

    def open(self):
        if self.isfile:
            return open(self)
        else:
            raise PathError('Can not open a dir!')

    def mkdir(self, raise_exception=False):
        try:
            os.makedirs(self)
        except FileExistsError:
            if raise_exception:
                raise
        return self

    def copy(self, dest):
        if self.isfile:
            shutil.copy(self, dest)
        else:
            shutil.copytree(self, dest)

    def move(self, dest, overwrite=False):
        """

        :param dest:
        :param overwrite:
        :return:
        """
        _dest = Path(dest)
        if _dest.isfile and _dest.basename != self.basename:
            dest = os.path.dirname(dest)
        try:
            shutil.move(self, dest)
            return True
        except shutil.Error as e:
            if 'already exists' in str(e) and overwrite:
                os.remove(os.path.join(dest, self.basename))
                return self.move(dest)
            return False

    def delete(self):
        if not self.exists:
            return
        if self.isfile:
            os.remove(self)
        else:
            os.removedirs(self)

    def rename(self, new):
        """
        Rename a file or a directory.

        :param new: new name
        :return:
        """
        shutil.move(self, os.path.join(self.parent, new))

    @staticmethod
    def abspath(rel_path: str, base_dir=None):
        if os.path.isabs(rel_path):
            return rel_path
        if not base_dir:
            try:
                raise Exception
            except Exception:
                frame_str = str(sys.exc_info()[2].tb_frame.f_back)
                base_dir = os.path.normpath(re.findall(r'(?<=file \')(.+)(?=\', line)', frame_str)[0])
        if os.path.isfile(base_dir):
            base_dir = os.path.dirname(base_dir)
        cur_dir_parts = base_dir.split(os.sep)
        parts = re.split(r'[\\/]', rel_path)
        for part in parts:
            if part == '':
                parts = parts[1:]
            elif part == '..':
                cur_dir_parts = cur_dir_parts[:-1]
                parts = parts[1:]
            elif part == '.':
                parts = parts[1:]
            else:
                cur_dir_parts.extend([part])
        return Path(os.sep.join(cur_dir_parts))

    def join(self, *paths):
        return self.expend(*paths)

    def expend(self, *paths):
        result = self
        for path in paths:
            result = result / path if result else Path(path)
        return result

    def __truediv__(self, other):
        if other:
            return self.__class__(os.path.join(self, other))
        return self


class PathError(Exception):
    """

    """


def root_path():
    """ 获取 根路径 """
    return Path(__file__).parent.parent


def ensure_path_sep(path: Text) -> Text:
    """兼容 windows 和 linux 不同环境的操作系统路径 """
    if "/" in path:
        path = os.sep.join(path.split("/"))

    if "\\" in path:
        path = os.sep.join(path.split("\\"))

    return root_path() + path


def get_all_files(file_path, yaml_data_switch=False) -> list:
    """
    获取文件路径
    :param file_path: 目录路径
    :param yaml_data_switch: 是否过滤文件为 yaml格式， True则过滤
    :return:
    """
    filename = []
    # 获取所有文件下的子文件名称
    for root, dirs, files in os.walk(file_path):
        for _file_path in files:
            path = os.path.join(root, _file_path)
            if yaml_data_switch:
                if 'yaml' in path or '.yml' in path:
                    filename.append(path)
            else:
                filename.append(path)
    return filename


def del_file(path):
    """删除目录下的文件"""
    list_path = os.listdir(path)
    for i in list_path:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            del_file(c_path)
        else:
            os.remove(c_path)
