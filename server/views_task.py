#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: views_task
@Created: 2023/3/17 17:23
"""
import os
from typing import List

from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel

from conf import settings
from utils import GetYamlData
from utils.path_fun import Path, ensure_path_sep

router = APIRouter(prefix="/task")


@router.post("/run-tasks")
async def run_tasks(background_tasks: BackgroundTasks):
    import subprocess
    # 获取包含 run.py 脚本的目录
    script_dir = Path(__file__).parent.parent
    # 将当前工作目录设置为脚本目录
    os.chdir(script_dir)

    def notify_complete():
        subprocess.call(['python', f'{settings.root_path}/run.py'])

    background_tasks.add_task(notify_complete)
    return {"message": "PyAuto is running in the background."}


class Item(BaseModel):
    args: List[str] = []


@router.post("/create")
async def create_tasks(item: Item):
    args = item.args
    GetYamlData(ensure_path_sep("\\conf\\config.yaml")).write_yaml_data("pytest", args)
    return {"message": "PyAuto tasks create successful"}
