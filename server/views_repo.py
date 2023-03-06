#! /usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: views_repo
@Created: 2023/3/6 10:06
"""
from fastapi import APIRouter

from server.core.host import local_host
from server.core.loader import TestLoader

router = APIRouter(prefix="/repo")


@router.get("/api/list")
def get_repos():
    """
    获取所有脚本仓库
    :param request:
    :return:
    """
    data = []
    for repo in local_host.repos:
        info = dict(
            name=repo.name,
        )
        data.append(info)
    return {"data": data}


@router.get("/api/{repo_name}/scripts")
def get_repo_scripts(repo_name):
    """
    获取指定仓库中的所有测试脚本
    :param request:
    :param repo_name:
    :return:
    """
    repo = local_host.get_repo(repo_name)
    loader = TestLoader()
    loader.load_path(repo.path, include_objects=True)
    data = []
    for s in repo.script_list or []:
        info = dict(
            test_name=s.test_name,
            pytest_name=s.pytest_name,
        )
        data.append(info)
    return {"data": data}
