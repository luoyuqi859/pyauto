#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: ws
@Created: 2023/3/17 15:15
"""
import asyncio
import threading
import time
import traceback
from typing import List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from loguru import logger


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


class WebsocketService:
    def __init__(self):
        self.__subscribers = []
        self._working = False

    def send_message(self, message):
        pass

    def add_subscriber(self, subscriber):
        self.__subscribers.append(subscriber)
        self.start()

    def remove_subscriber(self, subscriber):
        self.__subscribers.remove(subscriber)
        self.start()

    async def start(self):
        async def _work():
            while self._working:
                if not self.__subscribers:
                    self._working = False
                    break
                for subscriber in self.__subscribers:
                    try:
                        await subscriber.work()
                    except Exception:
                        logger.error(traceback.format_exc())
                        pass
                await asyncio.sleep(0.01)

        if self._working:
            return
        logger.info('Start websocket service...')
        self._working = True
        t = threading.Thread(target=_work, daemon=True)
        t.start()

    def stop(self):
        self._working = False


class WebsocketSubscriber:
    """websocket订阅者"""
    category = None  # 订阅消息类型

    def __init__(self, websocket: WebSocket):
        self.websocket = websocket
        wsService.add_subscriber(self)

    def work(self):
        pass


wsService = WebsocketService()
