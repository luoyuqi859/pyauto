#!/usr/bin/env python
# -*- ecoding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: forward
@Created: 2023/2/25
"""
from collections import namedtuple
from typing import Union

from utils import net

ForwardItem = namedtuple("ForwardItem", ["serial", "local", "remote"])


class Forward:
    def __init__(self, device=None):
        self.device = device

    @property
    def serial(self):
        return self.device.serial

    def forward(self, local, remote, norebind=False):
        if norebind:
            return self.device.adb_fp.adb.run_adb_cmd(f'forward tcp:{local} tcp:{remote} --norebind')
        return self.device.adb_fp.adb.run_adb_cmd(f'forward tcp:{local} tcp:{remote}')

    def clear_forwards(self, local=None):
        if local:
            self.device.run_command(f'forward --remove {local}', serial=None)
        else:
            self.device.run_command('forward --remove-all', serial=None)

    def forward_port(self, remote: Union[int, str]) -> int:
        """ forward remote port to local random port """
        for f in self.forward_list():
            if f.serial == self.serial and f.remote == f'tcp:{remote}' and f.local.startswith("tcp:"):
                return int(f.local[len("tcp:"):])
        local_port = net.get_free_port()
        self.forward(local_port, remote)
        return local_port

    def forward_list(self):
        res = self.device.run_command('forward --list', serial=None)
        for line in res.splitlines():
            parts = line.split()
            if len(parts) != 3:
                continue
            if self.serial and parts[0] != self.serial:
                continue
            yield ForwardItem(*parts)
