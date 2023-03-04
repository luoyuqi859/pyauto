#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: host
@Created: 2023/3/3 17:53
"""
import inspect
import os
import platform
from types import MethodType, FunctionType

from conf import settings
from server.repo import Repo
from utils import py
from utils.errors import InvalidTestError, InvalidRepoError
from utils.net import get_host_ip, get_free_port
from utils.path_fun import Path


def parse_repo_root(path):
    """
    获取仓库根路径
    :param path:
    :return:
    """
    path = os.path.abspath(path)
    path = Path(path)
    root = path.parent if os.path.isfile(str(path)) else path
    if not (root / '__init__.py').exists:
        for _, path, _ in root.walk('__init__.py'):
            return path.parent, path.parent.basename
    else:
        while (root / '__init__.py').exists:
            path = root
            root = root.parent
    return path, path.basename


class Host(dict):
    def __init__(self, ip=None, port=None):
        super().__init__()
        self.name = None
        self.workspace = settings.repos_path
        self.ip = ip or get_host_ip()
        self.port = port or get_free_port()
        self.sys_version = f'{platform.system()} {platform.version()}, {platform.processor()}, python {platform.python_version()}'
        self.repos = []

    def load_repo(self, **extra):
        # 从repo_root加载
        if os.path.exists(self.workspace):
            repo_root = Path(self.workspace)
            for path in repo_root.dirs():
                name = path.basename
                if name.startswith('.'):
                    continue
                self.get_repo(path)
        for name, path in extra.items():
            if path:
                self.get_repo(path)

    def get_repo(self, target, reload=False):
        """获取目标对象所在等仓库"""
        git_path = None
        if isinstance(target, (type, MethodType, FunctionType)):
            target = inspect.getmodule(target)
        if inspect.ismodule(target):
            module_name = target.__name__
            if module_name == '__main__':
                _, root_package = parse_repo_root(target.__file__)
            else:
                root_package = module_name.split('.')[0]
        elif isinstance(target, str):
            if os.path.exists(target):
                git_path = target
                repo_path, root_package = parse_repo_root(target)
                py.insert(repo_path.parent)
            else:
                root_package = target
        else:
            raise InvalidTestError(target)
        for repo in self.repos:
            if repo.name == root_package:
                if reload:
                    repo.reload()
                return repo
        # 如果没有找到，则注册
        if not root_package:
            raise InvalidRepoError(target)
        module = __import__(root_package)
        repo = Repo(module, git_path=git_path)
        self.repos.append(repo)
        repo.name = root_package
        return repo


local_host = Host()

if __name__ == '__main__':
    f = local_host.load_repo()
    a = f
