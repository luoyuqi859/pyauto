#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: views_repo
@Created: 2023/3/6 10:06
"""

from fastapi import APIRouter

from conf import settings
from server.core.collector import MyCollector
from server.core.host import local_host
from pydantic import BaseModel

router = APIRouter(prefix="/repo")


@router.get("/list")
async def get_repos():
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


@router.get("/scripts")
async def get_scripts():
    """
    获取repos中所有脚本
    :param request:
    :return:
    """
    local_collect = MyCollector(settings.repos_path)
    local_collect.collect()
    collections = local_collect.items
    data = []
    for address, _ in collections.items():
        data.append(address)
    return {
        "data": data,
        "total": len(data)
    }


@router.get("/scripts/{repo_name}")
async def get_scripts_repo(repo_name: str):
    """
    获取指定仓库中的所有测试脚本
    :param request:
    :param repo_name:
    :return:
    """
    local_collect = MyCollector(settings.repos_path / repo_name)
    local_collect.collect()
    collections = local_collect.items
    data = []
    for address, _ in collections.items():
        data.append(address)
    return {
        "data": data,
        "total": len(data)
    }


@router.get("/code")
async def get_repo_file_code():
    """
    获取code
    :param request:
    :param repo_name:
    :return:
    """
    path = settings.config_path / "config.yaml"
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


class SaveCodeRequestBody(BaseModel):
    code: str


@router.post("/save/code")
async def get_repo_file_code(requestBody: SaveCodeRequestBody):
    """
    获取code
    :param request:
    :param repo_name:
    :return:
    """
    data = requestBody.code
    path = settings.config_path / "config.yaml"
    with open(path, 'w+', encoding='utf-8') as f:
        f.write(data)
        return f.read()

# @router.post("/scripts/add")
# async def add_test_path():
#     """
#     获取指定仓库中的所有测试脚本
#     :param request:
#     :param repo_name:
#     :return:
#     """
#     # local_collect = MyCollector(settings.repos_path / repo_name)
#     return {
#         "data": data,
#         "total": len(data)
#     }
