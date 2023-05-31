#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: ws
@Created: 2023/3/17 15:15
"""

import typing

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        # 存放激活的ws连接对象
        self.active_connections: typing.List[WebSocket] = []

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


websocket_manager = ConnectionManager()
