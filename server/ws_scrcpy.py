#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: ws_scrcpy
@Created: 2023/4/27 16:08
"""
import asyncio
import json

from fastapi import WebSocket, WebSocketDisconnect

from server.core.scrcpy.client import ClientDevice

DEVICE_ID = "b9f24c2d"


class ScrcpyWSHandler:
    """scrcpy投屏"""
    DEVICE_CLIENT_DICT = dict()

    def __init__(self, websocket: WebSocket):
        self.websocket = websocket
        self.device_id = DEVICE_ID
        self.device_client = None

    async def connect(self):
        # 获取当前连接对应的device_client
        old_device_client = self.DEVICE_CLIENT_DICT.get(self.device_id, None)
        if old_device_client:
            self.device_client = old_device_client
        else:
            self.device_client = self.DEVICE_CLIENT_DICT[self.device_id] = ClientDevice(self.device_id)
        if "screen" in self.websocket.url.path:
            self.device_client.ws_client_list.append(self.websocket)
            # 重新启动scrcpy 重新开始任务
            async with self.device_client.device_lock:
                await self.device_client.stop()
                await self.device_client.start()
        else:
            self.device_client.ws_touch_list.append(self.websocket)

    def disconnect(self):
        if self.websocket in self.device_client.ws_client_list:
            self.device_client.ws_client_list.remove(self.websocket)
        if self.websocket in self.device_client.ws_touch_list:
            self.device_client.ws_touch_list.remove(self.websocket)

    async def receive(self):
        try:
            while True:
                text_data = await self.websocket.receive_text()
                data = json.loads(text_data)
                if data['msg_type'] == 2:
                    await asyncio.sleep(1)
                    # await self.device_client.controller.inject_touch_event(x=data['x'], y=data['y'],
                    #                                                        action=data['action'])
                elif data['msg_type'] == 3:
                    await self.device_client.controller.inject_scroll_event(x=data['x'], y=data['y'],
                                                                            distance_x=data['distance_x'],
                                                                            distance_y=data['distance_y'])
                elif data['msg_type'] == 30:
                    await self.device_client.controller.swipe(x=data['x'], y=data['y'], end_x=data['end_x'],
                                                              end_y=data['end_y'],
                                                              unit=data['unit'], delay=data['delay'])
        except WebSocketDisconnect:
            self.disconnect()
