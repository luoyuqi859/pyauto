#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: views_task
@Created: 2023/3/17 17:23
"""
import asyncio
import os
from typing import List
import subprocess
from fastapi import APIRouter, BackgroundTasks, WebSocket
from pydantic import BaseModel

from conf import settings
from utils import GetYamlData, net
from utils.path_fun import Path, ensure_path_sep

router = APIRouter(prefix="/task")


# @router.post("/run-tasks")
# async def run_tasks(background_tasks: BackgroundTasks):
#     import subprocess
#     # 获取包含 run.py 脚本的目录
#     script_dir = Path(__file__).parent.parent
#     # 将当前工作目录设置为脚本目录
#     os.chdir(script_dir)
#
#     async def notify_complete():
#         subprocess.call(['python', f'{settings.root_path}/run.py'])
#
#     background_tasks.add_task(notify_complete)
#     return {"message": "PyAuto is running in the background."}


# async def run_script():
#     try:
#         # 使用 subprocess.Popen() 来启动子进程并执行脚本
#         proc = subprocess.Popen(['python', f'{settings.root_path}/run.py'], stdout=subprocess.PIPE,
#                                 stderr=subprocess.PIPE)
#         out, err = proc.communicate()  # 获取脚本的标准输出和标准错误流
#         if err:
#             # 如果脚本有错误输出，则向客户端发送错误消息
#             raise Exception(f"Script execution failed: {err.decode('utf-8')}")
#     except Exception as e:
#         # 发生任何异常时，向客户端发送错误消息
#         raise Exception(f"Error executing script: {str(e)}")
#
#
# async def notify_complete(websocket: WebSocket):
#     try:
#         await run_script()
#         # 任务执行完成后向前端发送消息
#         print('task_finished')
#         await websocket.send_text('task_finished')
#     except Exception as e:
#         # 如果运行脚本时出现任何异常，则向客户端发送错误消息
#         await websocket.send_text(f"Error executing script: {str(e)}")


async def run_script_and_notify(websocket: WebSocket):
    try:
        # 获取包含 run.py 脚本的目录
        script_dir = Path(__file__).parent.parent
        # 将当前工作目录设置为脚本目录
        os.chdir(script_dir)
        subprocess.call(['python', f'{settings.root_path}/run.py'])
        await websocket.send_text('task_finished')
    except Exception as e:
        await websocket.send_text(f"Error executing script: {str(e)}")


@router.websocket("/ws")
async def task_run(websocket: WebSocket):
    await websocket.accept()

    while True:
        data = await websocket.receive_text()
        if data == 'task_start':
            # 获取包含 run.py 脚本的目录
            script_dir = Path(__file__).parent.parent
            # 将当前工作目录设置为脚本目录
            os.chdir(script_dir)
            subprocess.call(['python', f'{settings.root_path}/run.py'])
            # 任务执行完成后，发送标识消息并关闭 WebSocket 连接
            await websocket.send_text('task_finished')
            await websocket.close()
            break


@router.get("/report")
async def view_report():
    folder_path = settings.project_path
    if os.path.exists(folder_path):
        items = os.listdir(folder_path)
        folders = [item for item in items if os.path.isdir(os.path.join(folder_path, item))]
        if not folders:
            return {"message": "没有找到报告文件,请先执行用例"}
        folders.sort(key=lambda x: os.path.getmtime(os.path.join(folder_path, x)))
        last_folder_path = Path(folder_path) / folders[-1] / "html"
        if not os.path.exists(last_folder_path):
            return {"message": "没有找到报告文件,请先执行用例"}
        ip = net.get_host_ip()
        port = net.get_free_port()
        cmd = f"{settings.allure_bat} open {last_folder_path} -p {port}"
        os.popen(cmd)
        return {"message": f"报告已生成!如没有自动打开,请手动在浏览器输入:{ip}:{port}"}
    else:
        return {"message": "没有找到报告文件,请先执行用例"}


class Item(BaseModel):
    args: List[str] = []


@router.post("/create")
async def create_tasks(item: Item):
    args = item.args
    GetYamlData(ensure_path_sep("\\conf\\config.yaml")).write_yaml_data("pytest", args)
    return {"message": "PyAuto tasks create successful"}
