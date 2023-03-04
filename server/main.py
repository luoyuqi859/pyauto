#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: main.py
@Created: 2023/3/3 12:49
"""
import os
from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from conf import settings
from server.host import local_host
from server.loader import TestLoader
from utils.path_fun import Path

app = FastAPI()


# @app.get("/run")
# async def main():
#     import subprocess
#     subprocess.call(['python', f'{settings.root_path}/run.py'])
#     return
#     # {"message": "test finish"}


class ConnectionManager:
    def __init__(self):
        # 存放激活的ws连接对象
        self.active_connections: List[WebSocket] = []

    async def connect(self, ws: WebSocket):
        # 等待连接
        await ws.accept()
        # 存储ws连接对象
        self.active_connections.append(ws)

    def disconnect(self, ws: WebSocket):
        # 关闭时 移除ws对象
        self.active_connections.remove(ws)

    @staticmethod
    async def send_personal_message(message: str, ws: WebSocket):
        # 发送个人消息
        await ws.send_text(message)

    async def broadcast(self, message: str):
        # 广播消息
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.on_event("startup")
def startup_event():
    os.system(f"{settings.root_path}/server/xxx.html")


@app.websocket("/ws/{user}")
async def websocket_endpoint(websocket: WebSocket, user: str):
    await manager.connect(websocket)

    await manager.broadcast(f"用户{user}进入")

    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"你说了: {data}", websocket)
            if data == "start":
                import subprocess
                subprocess.call(['python', f'{settings.server_path}/cli.py', "--case",
                                 r"E:\py_work\pyauto\repos\lxl\test_xxx.py::test_xxx,E:\py_work\pyauto\repos\lxl\test_xxx.py::test_xxx1"])
                await manager.broadcast("通知: 本次测试结束")
            else:
                await manager.broadcast(f"用户{user} 说: {data}")

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"用户-{user}-离开")


@app.get("/api/repo/list")
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


@app.get("/api/repo/{repo_name}/scripts")
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


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=5555, reload=True)
