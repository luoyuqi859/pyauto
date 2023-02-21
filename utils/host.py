#!/usr/bin/env python
# -*- ecoding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: host
@Created: 2023/2/21 13:17
"""
import inspect
import os
import platform
from types import MethodType, FunctionType

from conf import settings
from utils import py
from utils.errors import InvalidTestError
from utils.net import get_host_ip, get_free_port
from utils.path_fun import Path
from utils.repo import InvalidRepoError, Repo


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
        self.workspace = settings.root_path / "repos"
        self.ip = ip or get_host_ip()
        self.port = port or get_free_port()
        self.sys_version = f'{platform.system()} {platform.version()}, {platform.processor()}, python {platform.python_version()}'
        # self.remote = Remote()
        self.servers = {}  # host.ini中的server配置节
        self.repos = []
        self.load_repo()
        # self.__read_config()

    # def switch_server(self, name):
    #     f = self.servers.get(name)
    #     self.remote = Remote(**self.servers.get(name))

    # def register(self, server):
    #     self.switch_server(server)
    #     self._register_host()
    #     self._register_devices()
    #     self._register_repos()

    # def _register_host(self):
    #     """
    #     注册执行主机
    #     """
    #     data = dict(name=self.name, ip=self.ip, port=self.port, category=self.category, sys_version=self.sys_version)
    #     json_data = self.remote.register_host(**data)
    #     self.update(**json_data)
    #     return json_data

    # def _register_devices(self):
    #     settings.DEVICE_LISTENERS.append('panda.django.listener')
    #     # 从数据库获取隶属于本主机的所有设备，并更新其状态
    #     devices = self.remote.get_registered_devices(self.id)
    #     for device in devices:
    #         serial = device.get('serial')
    #         # device['phone_numb'] = 'test'
    #         if serial and serial not in device_pool.devices:
    #             device['status'] = 'offline'
    #             device['host'] = self.id
    #             self.remote.register_device(device)

    # def _register_repos(self):
    #     # self._load_repos()
    #     for repo in self.repos:
    #         project = self.remote.get_project(repo.project)
    #         commit_time, commit_message = repo.get_last_commit_info()
    #         data = self.remote.register_repo(
    #             name=repo.name,
    #             project_branch=repo.project_branch,
    #             git_url=repo.git_url,
    #             project=project.id,
    #             project_name=project.name,
    #             last_commit_time=commit_time.strftime('%Y-%m-%d %H:%M:%S') if commit_time else None,
    #             last_commit_message=commit_message,
    #             host_ip=self.ip
    #         )
    #         repo.update(**data.data)

    # def __read_config(self):
    #     config_file = self.workspace / 'host.ini'
    #     if os.path.exists(self.workspace) and os.path.exists(config_file):
    #         config = cfg.read_ini(config_file)
    #         for section, data in config.items():
    #             if section.startswith('server:'):
    #                 data['name'] = name = section[7:]
    #                 self.servers[name] = data
    #         self.name = config.host.name
    #         self.category = config.host.category
    #         repo_root = config.host.repo_root
    #         self.repo_root = repo_root.replace('$workspace', self.workspace)
    #         self.load_repo(**config.repo.data)

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

    def add_object(self, o, category=None):
        repo = self.get_repo(o)
        repo.add(o, category=category)

    def __getattr__(self, item):
        return self.get(item)

    def __repr__(self):
        return f'<Host {self.name}>'


local_host = Host()
