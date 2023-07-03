#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: client
@Created: 2023/4/26 15:19
"""
import asyncio
import struct
import subprocess

from bitstring import BitStream
from h26x_extractor.nalutypes import SPS
from loguru import logger

from server.core.adb import adb
from server.core.scrcpy.controller import Controller


class ClientDevice:
    @classmethod
    async def cancel_task(cls, task):
        # If task is already finish, this operation will return False, else return True(mean cancel operation success)
        task.cancel()
        try:
            # Wait task done, Exception inside the task will raise here
            await task
            # [task cancel operation no effect] 1.task already finished
        except asyncio.CancelledError:
            # [task cancel operation success] 2.catch task CancelledError Exception
            print("task is cancelled now")
        except Exception as e:
            # [task cancel operation no effect] 3.task already finished with a normal Exception
            print(f"task await exception {type(e)}, {e}")

    def __init__(self, device_id,
                 max_size=720,
                 bit_rate=1280000,
                 max_fps=25,
                 connect_timeout=300):
        self.device_id = device_id
        # scrcpy_server启动参数
        self.max_size = max_size
        self.bit_rate = bit_rate
        self.max_fps = max_fps
        # adb socket连接超时时间
        self.connect_timeout = connect_timeout
        # scrcpy连接
        self.deploy_shell_socket = None
        # 连接设备的socket, 监听设备socket的video_task任务
        self.video_socket = None
        self.control_socket = None
        self.video_task = None
        # 设备型号和分辨率
        self.device_name = None
        self.resolution = None
        # 设备并发锁
        self.device_lock = asyncio.Lock()
        # 设备控制器
        self.controller = Controller(self)
        # 需要推流得ws_client
        self.ws_client_list = list()
        # 需要推操作失败的ws_client
        self.ws_touch_list = list()

    async def prepare_server(self):
        commands2 = [
            "adb", "-s", self.device_id, "shell",
            "CLASSPATH=/data/local/tmp/scrcpy-server",  # 设置环境变量，指定 scrcpy-server 的路径。
            "app_process",
            "/",
            "com.genymobile.scrcpy.Server",  # 启动名为 com.genymobile.scrcpy.Server 的应用程序。
            "1.24",  # 指定 scrcpy-server 的版本号
            f"log_level=info",  # 设置日志级别为 info
            f"max_size={self.max_size}",  # 设置屏幕分辨率的最大值。
            f"bit_rate={self.bit_rate}",  # 设置视频编码的比特率。
            f"max_fps={self.max_fps}",  # 设置视频的最大帧率。
            f"lock_video_orientation=-1",  # 锁定屏幕方向
            "tunnel_forward=true",  # 启用网络隧道
            f"control=true",  # 启用控制模式。
            f"display_id=0",  # 指定显示器 ID
            f"show_touches=true",  # 在屏幕上显示触摸点
            f"stay_awake=false",  # 让 scrcpy-server 在设备不活动时进入休眠状态。
            f"codec_options=profile=1,level=2",  # 设置视频编码器选项。
            f"encoder_name=OMX.google.h264.encoder",  # 指定编码器的名称。
            f"power_off_on_close=false",  # 关闭 scrcpy-server 时不自动关闭设备屏幕电源。
            "clipboard_autosync=false",  # 禁用剪贴板自动同步。
            f"downsize_on_error=true",  # 在视频编码错误时缩小画面并重试
            "cleanup=true",  # 启用清理线程
            f"power_on=true",  # 启动设备时开启屏幕电源。
            "send_device_meta=true",  # 在视频套接字连接时发送设备名称和分辨率信息
            f"send_frame_meta=false",  # 不接收视频帧数据。
            "send_dummy_byte=true",  # 在视频套接字连接时发送虚拟字节。
            "raw_video_stream=false",  # 接收经过编码的视频流。
        ]
        self.deploy_shell_socket = subprocess.Popen(commands2, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        res = self.deploy_shell_socket.stdout.readlines(3)
        if len(res) == 1 and "Device" in res[0].decode():
            logger.info("[%s] start scrcpy success" % self.device_id)
        else:
            logger.info("[%s] start scrcpy error" % self.device_id)
            self.deploy_shell_socket = None
            for ws_client in self.ws_client_list:
                ws_client.close()
            raise ConnectionError("启动scrcpy服务失败")

    async def prepare_socket(self):
        # 1.video_socket
        self.video_socket = await self.create_socket('localabstract:scrcpy', timeout=self.connect_timeout)
        dummy_byte = await self.video_socket.read_exactly(1)
        if not len(dummy_byte) or dummy_byte != b"\x00":
            raise ConnectionError("not receive Dummy Byte")
        # 2.control_socket
        self.control_socket = await self.create_socket('localabstract:scrcpy', timeout=self.connect_timeout)
        # 3.device information
        self.device_name = (await self.video_socket.read_exactly(64)).decode("utf-8").rstrip("\x00")
        if not len(self.device_name):
            raise ConnectionError("not receive Device Name")
        self.resolution = struct.unpack(">HH", await self.video_socket.read_exactly(4))

    async def _video_task(self):
        while True:
            try:
                data = await self.video_socket.read_until(b'\x00\x00\x00\x01')
                current_nal_data = b'\x00\x00\x00\x01' + data.rstrip(b'\x00\x00\x00\x01')
                self.update_resolution(current_nal_data)
                for ws_client in self.ws_client_list:
                    await ws_client.send_bytes(current_nal_data)
            except (asyncio.exceptions.IncompleteReadError, AttributeError):
                logger.info("[%s] scrcpy error" % self.device_id)
                break

    def update_resolution(self, current_nal_data):
        # when read a sps frame, change origin resolution
        if current_nal_data.startswith(b'\x00\x00\x00\x01g'):
            # sps resolution not equal device resolution, so reuse and transform original resolution
            sps = SPS(BitStream(current_nal_data[5:]), False)
            width = (sps.pic_width_in_mbs_minus_1 + 1) * 16
            height = (2 - sps.frame_mbs_only_flag) * (sps.pic_height_in_map_units_minus_1 + 1) * 16
            if width > height:
                resolution = (max(self.resolution), min(self.resolution))
            else:
                resolution = (min(self.resolution), max(self.resolution))
            self.resolution = resolution

    async def start(self):
        await self.prepare_server()
        await self.prepare_socket()
        self.video_task = asyncio.create_task(self._video_task())

    async def stop(self):
        if self.video_socket:
            await self.video_socket.disconnect()
            self.video_socket = None
        if self.video_task:
            await self.cancel_task(self.video_task)
            self.video_task = None
        if self.control_socket:
            await self.control_socket.disconnect()
            self.control_socket = None
        if self.deploy_shell_socket:
            try:
                self.deploy_shell_socket.terminate()
            except:
                pass
            self.deploy_shell_socket = None

    async def create_socket(self, connect_name, timeout=300):
        socket = adb.connect()
        for _ in range(timeout):
            try:
                await socket.connect()
                await socket.send_cmd(f'host:transport:{self.device_id}')
                await socket.check_okay()
                await socket.send_cmd(connect_name)
                await socket.check_okay()
                return socket
            except Exception as e:
                await socket.disconnect()
            await asyncio.sleep(0.01)
        else:
            raise ConnectionError(f"{self.device_id} create_connection to {connect_name} error!!")
