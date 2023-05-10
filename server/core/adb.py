#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: adb.py
@Created: 2023/4/26 18:50
"""
import asyncio
import subprocess
from collections import namedtuple

from loguru import logger

OKAY = "OKAY"
FAIL = "FAIL"

DeviceItem = namedtuple("Device", ['serial', 'status'])
DeviceEvent = namedtuple('DeviceEvent', ['present', 'serial', 'status'])
ForwardItem = namedtuple("ForwardItem", ['serial', 'local', 'remote'])


class AdbError(Exception):
    """ adb error """


class AdbStreamConnection:
    """
    Example usage:
        async with AdbStreamConnection(host, port) as c:
            await c.send_cmd("host:kill")
    """

    def __init__(self, host, port, socket_timeout=1):
        self.socket_timeout = socket_timeout
        self.__host = host
        self.__port = port
        self.__reader = None
        self.__writer = None

    async def connect(self):
        try:
            self.__reader, self.__writer = await asyncio.wait_for(asyncio.open_connection(self.__host, self.__port),
                                                                  self.socket_timeout)
        except Exception as e:
            logger.warning(e)
            await self.disconnect()
        return self

    async def disconnect(self):
        if self.__writer:
            self.__writer.close()
            try:
                await self.__writer.wait_closed()
            except ConnectionAbortedError:
                pass
            self.__writer = self.__reader = None

    async def __aenter__(self):
        return await self.connect()

    async def __aexit__(self, exc_type, exc, tb):
        await self.disconnect()

    async def check_okay(self):
        data = (await self.read_exactly(4)).decode()
        if data == FAIL:
            raise AdbError(await self.read_string())
        elif data == OKAY:
            return
        else:
            raise AdbError("Unknown data: %s" % data)

    async def read(self, cnt=-1):
        return await self.__reader.read(cnt)

    async def read_line(self):
        return await self.__reader.readline()

    async def read_exactly(self, num: int):
        return await self.__reader.readexactly(num)

    async def read_until(self, sep):
        return await self.__reader.readuntil(sep)

    async def read_bytes_until(self, delimiter: bytes):
        return await self.__reader.readuntil(delimiter)

    async def read_string(self):
        lenstr = (await self.read_exactly(4)).decode()
        msgsize = int(lenstr, 16)
        return (await self.read_exactly(msgsize)).decode()

    async def send_cmd(self, cmd: str):
        self.__writer.write("{:04x}{}".format(len(cmd), cmd).encode('utf-8'))
        await self.__writer.drain()

    async def write_bytes(self, msg: bytes):
        self.__writer.write(msg)
        await self.__writer.drain()


class AdbClient(object):

    def connect(self, host="127.0.0.1", port=5037):
        return AdbStreamConnection(host, port)

    async def server_version(self) -> int:
        async with AdbStreamConnection(host="127.0.0.1", port=5037) as c:
            await c.send_cmd("host:version")
            await c.check_okay()
            return int(await c.read_string(), 16)

    async def track_devices(self):
        """
        yield DeviceEvent according to track-devices

        Example:
            async for event in track_devices():
                print(event)
                # output: DeviceEvent(present=True, serial='xxxx', status='device')
        """
        orig_devices = []
        while True:
            try:
                async for content in self._unsafe_track_devices():
                    curr_devices = self.output2devices(
                        content, limit_status=['device'])
                    for evt in self._diff_devices(orig_devices, curr_devices):
                        yield evt
                    orig_devices = curr_devices
            except ConnectionResetError:
                # adb server maybe killed
                for evt in self._diff_devices(orig_devices, []):
                    yield evt
                orig_devices = []

                sleep = 1.0
                logger.info(
                    "adb connection is down, retry after %.1fs" % sleep)
                await asyncio.sleep(sleep)
                subprocess.run(['adb', 'start-server'])
                version = await self.server_version()
                logger.info("adb-server started, version: %d", version)

    async def _unsafe_track_devices(self):
        async with self.connect() as conn:
            await conn.send_cmd("host:track-devices")
            await conn.check_okay()
            while True:
                yield await conn.read_string()

    def _diff_devices(self, orig_devices: list, curr_devices: list):
        """ Return iter(DeviceEvent) """
        for d in set(orig_devices).difference(curr_devices):
            yield DeviceEvent(False, d.serial, d.status)
        for d in set(curr_devices).difference(orig_devices):
            yield DeviceEvent(True, d.serial, d.status)

    def output2devices(self, output: str, limit_status=None):
        """
        Args:
            outptu: str of adb devices output

        Returns:
            list of DeviceItem
        """
        if limit_status is None:
            limit_status = []
        results = []
        for line in output.splitlines():
            fields = line.strip().split("\t", maxsplit=1)
            if len(fields) != 2:
                continue
            serial, status = fields[0], fields[1]

            if limit_status:
                if status in limit_status:
                    results.append(DeviceItem(serial, status))
            else:
                results.append(DeviceItem(serial, status))
        return results

    async def shell(self, serial: str, command: str):
        async with self.connect() as conn:
            await conn.send_cmd("host:transport:" + serial)
            await conn.check_okay()
            await conn.send_cmd("shell:" + command)
            await conn.check_okay()
            output = await conn.read()
            return output.decode('utf-8')

    async def forward_list(self):
        async with self.connect() as conn:
            # adb 1.0.40 not support host-local
            await conn.send_cmd("host:list-forward")
            await conn.check_okay()
            content = await conn.read_string()
            for line in content.splitlines():
                parts = line.split()
                if len(parts) != 3:
                    continue
                yield ForwardItem(*parts)

    async def forward(self, serial: str, local: str, remote: str, norebind=False):
        """
        Args:
            serial: device serial
            local, remote (str): tcp:<port> | localabstract:<name>
            norebind(bool): set to true will fail it when
                    there is already a forward connection from <local>
        """
        async with self.connect() as conn:
            cmds = ["host-serial", serial, "forward"]
            if norebind:
                cmds.append('norebind')
            cmds.append(local + ";" + remote)
            await conn.send_cmd(":".join(cmds))
            await conn.check_okay()


adb = AdbClient()
