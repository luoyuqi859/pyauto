#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: views_task
@Created: 2023/3/17 17:23
"""
import asyncio
import json
import os
import re
import subprocess
import sys

from typing import List

from fastapi import APIRouter, WebSocket
from loguru import logger
from pydantic import BaseModel

from conf import settings
from utils import GetYamlData, net
from utils.path_fun import Path, ensure_path_sep

router = APIRouter(prefix="/task")


def remove_color_codes(s: str) -> str:
    """
    Remove ANSI color codes from a string.
    """
    return re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', s)


async def run_background_task(websocket: WebSocket) -> None:
    try:
        data = await websocket.receive_text()
        if isinstance(data, bytes):
            data = data.decode()
        json_msg = json.loads(data)
        serial = json_msg.get('serial')
        if not serial:
            await websocket.send_json({'message': 'need serial'})
            return

            # 获取包含 run.py 脚本的目录
        script_dir = Path(__file__).parent.parent
        logger.info(serial)

        # 将当前工作目录设置为脚本目录
        # os.chdir(script_dir)

        # 启动子进程并取得其进程对象
        process = await asyncio.create_subprocess_exec(
            'python', 'run.py', '-s', f'{serial}',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
            cwd=str(script_dir))

        # 读取子进程输出并发送到 WebSocket
        async for line in process.stdout:
            message = line.decode().strip()
            if message:
                await websocket.send_json({'message': remove_color_codes(message)})

        # 等待子进程退出
        rc = await process.wait()

        # 发送消息给客户端表示任务已完成
        await websocket.send_json({'message': f'Task completed with return code {rc}'})

    except Exception as e:
        # 如果发生异常，则将跟踪信息打印到输出缓冲区
        import traceback
        traceback.print_exc(file=sys.stdout)

    finally:
        # 关闭 WebSocket 连接
        await websocket.send_json({'message': 'task_finished'})
        await websocket.close()


@router.websocket("/ws")
async def run_task(websocket: WebSocket):
    await websocket.accept()
    task = asyncio.create_task(run_background_task(websocket))
    await task


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
        cmd = f"{settings.allure_bat} open {last_folder_path} -h {ip} -p {port}"
        await asyncio.create_subprocess_shell(cmd)
        # os.popen(cmd)
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
