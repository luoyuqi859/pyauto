#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: views_device
@Created: 2023/4/18 15:18
"""
import asyncio
import base64
import json
from io import BytesIO

from fastapi import APIRouter, WebSocket
from loguru import logger
from starlette.websockets import WebSocketDisconnect

from server.ws_scrcpy import ScrcpyWSHandler
from uiauto.android.device import AndroidDevice, connect

router = APIRouter(prefix="/device")


class ScreenshotSync():
    """设备投影"""

    worker_task = None

    def __init__(self, websocket, serial=None):
        self.websocket = websocket
        self.serial = serial
        self.device = None
        self.closed = False  # 记录 WebSocket 是否已经关闭的标记
        self.message_queue = asyncio.Queue()

    async def __aenter__(self):
        self.device = AndroidDevice(connect(self.serial))
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # 如果已经关闭 WebSocket，则不进行任何操作
        if self.closed:
            return
        # 否则，关闭 WebSocket 连接
        self.device = None
        self.closed = True

    async def send_data(self, data):
        try:
            if not self.closed:
                await self.websocket.send_text(json.dumps(data))
        except WebSocketDisconnect:
            self.closed = True
            await self.stop()

    async def work(self):
        while not self.closed:  # 在每一次工作循环前，检查 WebSocket 的关闭状态

            # 处理WebSocket消息队列中的消息
            if not self.message_queue.empty():
                msg = await self.message_queue.get()
                if msg == "disconnect":
                    self.closed = True
                    await self.stop()
                    break

            w, h = self.device.window_size
            pillow_image = self.device.screenshot.pillow

            # 缩小图片尺寸
            new_size = (int(w * 0.5), int(h * 0.5))  # 设置新的大小为原始大小的一半
            resized_image = pillow_image.resize(new_size)
            #
            # 将图片转换为JPEG格式，并压缩质量
            output_buffer = BytesIO()
            resized_image.save(output_buffer, format='jpeg', quality=50)
            byte_data = output_buffer.getvalue()
            base64_str = base64.b64encode(byte_data).decode()

            data = {
                'image': base64_str,
                'width': w,
                'height': h
            }

            await self.send_data(data)
            await asyncio.sleep(0.1)

    async def stop(self):
        logger.info("断开ws连接")
        if self.websocket and not self.closed:
            await self.websocket.close()
            if self.worker_task:
                self.worker_task.cancel()


async def run_background_task(websocket: WebSocket) -> None:
    data = await websocket.receive_text()
    logger.info(data)
    if data:
        if isinstance(data, bytes):
            data = data.decode()
        json_msg = json.loads(data)
        serial = json_msg.get('serial')
        logger.info(serial)
        if not serial:
            await websocket.send_json({'message': 'need serial'})
            return
        async with ScreenshotSync(websocket=websocket, serial=serial) as screenshot_sync:
            screenshot_sync.worker_task = asyncio.create_task(screenshot_sync.work())
            try:
                while not screenshot_sync.closed:
                    msg = await websocket.receive_text()
                    logger.info(msg)
                    # 将WebSocket消息添加到队列中，以便在下一个轮询周期中处理
                    await screenshot_sync.message_queue.put(msg)
            except WebSocketDisconnect:
                # 如果发生 WebSocketDisconnect 异常，说明 WebSocket 连接被关闭
                pass


@router.websocket("/ws")
async def task_run(websocket: WebSocket):
    await websocket.accept()
    task = asyncio.create_task(run_background_task(websocket))
    await task


@router.websocket("/ws/scrcpy/screen")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    handler = ScrcpyWSHandler(websocket)

    await handler.connect()
    try:
        await handler.receive()
    except:
        handler.disconnect()
