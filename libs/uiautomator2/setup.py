#!/usr/bin/env python
# coding: utf-8
#
# Licensed under MIT
#
import os
import platform

from setuptools import setup

setup_info = {}
packages = []
package_data = {}

system = platform.system()


def load_package_data(path, package):
    """获取指定包内需要包含的数据文件"""
    data = []
    for root, dirs, files in os.walk(path):
        rel_root = root.replace(path, os.path.basename(path))
        for f in files:
            if f.endswith(('.exe', '.dll')) and system == 'Linux':
                continue
            data.append(os.path.join(rel_root, f))

    return {
        package: data
    }


def get_packages(path='.'):
    """获取需要处理的包目录(通常为包含 init.py 的文件夹)"""
    for d in os.listdir(path):
        if d.startswith(('.', '_')) or d in ['build', 'dist'] or d.endswith('.egg-info'):
            continue
        d_path = os.path.join(path, d)
        if os.path.isfile(d_path):
            continue

        _init_file = os.path.join(d_path, '__init__.py')
        if not os.path.exists(_init_file):
            # 如果不存在，则作为资源文件夹
            pkg_name = f'{path[1:]}'.replace(os.sep, '.').strip('.')
            package_data.update(load_package_data(d_path, pkg_name))
            continue
        else:
            pkg_name = f'{path[1:]}.{d}'.replace(os.sep, '.').strip('.')
            packages.append(pkg_name)

        get_packages(d_path)


def get_requires():
    """获取依赖"""
    root = os.path.dirname(__file__)
    require_txt = os.path.join(root, 'requirements.txt')
    with open(require_txt, 'r', encoding='utf-8') as f:
        return f.read().splitlines()


get_packages()
requires = get_requires()

setup(
    packages=packages,
    package_data=package_data,
    install_requires=requires,  # 自动安装依赖
)


