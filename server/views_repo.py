#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: views_repo
@Created: 2023/3/6 10:06
"""
import asyncio
import os
import re
from datetime import datetime
from typing import Optional, List

from fastapi import APIRouter, Request

from conf import settings
from server.core.collector import MyCollector
from server.core.host import local_host
from pydantic import BaseModel

from utils import net
from utils.path_fun import Path

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


class FileItem(BaseModel):
    path: str
    name: str
    is_dir: bool
    size: int
    create_time: str  # 格式化的创建时间
    children: Optional[List['FileItem']] = None


def traverse_folder(folder_path: str, ignore_patterns: Optional[List[str]] = None) -> List[FileItem]:
    if ignore_patterns:
        ignore_regex = re.compile('|'.join(ignore_patterns))
    else:
        ignore_regex = None

    items = []
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if ignore_regex and ignore_regex.search(item_path):
            continue
        if os.path.isdir(item_path):
            item_size = 0
            is_dir = True
            children = traverse_folder(item_path, ignore_patterns)
        else:
            ext = os.path.splitext(item_path)[1].lower()
            if ext not in ('.py', '.ini', '.yaml'):
                continue
            item_size = os.path.getsize(item_path)
            is_dir = False
            children = None
        create_time = datetime.fromtimestamp(os.path.getctime(item_path)).strftime("%Y-%m-%d %H:%M:%S")
        items.append(FileItem(path=item_path, name=item, is_dir=is_dir, size=item_size, create_time=create_time,
                              children=children))
    return items


@router.get("/report")
async def get_files_list():
    # 遍历目录路径 dir_path 下的所有文件和子目录
    folder_path = settings.root_path / "report"
    ignore_patterns = ['.git', '__pycache__', '.idea', '.pytest_cache', 'libs']
    items = traverse_folder(folder_path, ignore_patterns)
    return {"items": items}


@router.post("/report/display")
async def view_report(request: Request):
    body = await request.json()
    folder_path = body.get("path")
    if not folder_path:
        return {"message": "缺少必要参数 path，请检查后重试"}
    if os.path.exists(folder_path):
        last_folder_path = Path(folder_path) / "html"
        if not os.path.exists(last_folder_path):
            return {"message": "没有找到报告文件,请先执行用例"}
        ip = net.get_host_ip()
        port = net.get_free_port()
        cmd = f"{settings.allure_bat} open {last_folder_path} -h {ip} -p {port}"
        await asyncio.create_subprocess_shell(cmd)
        # os.popen(cmd)
        return {"message": f"报告已生成!如没有自动打开,请手动在浏览器输入:{ip}:{port}"}
    else:
        return {"message": "没有找到报告文件,请先执行用例"}

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
