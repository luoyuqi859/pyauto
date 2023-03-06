#! /usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: qs
@Created: 2023/2/25
"""
from utils.list import List


class QuickSettings:
    """"""

    def __init__(self, device):
        self.device = device

    def get_qs_tiles(self):
        """获取已添加的QS tiles"""
        return [item.replace('(', r'\(').replace(')', r'\)') for item in
                self.device.shell('settings get secure sysui_qs_tiles').split(',')]

    def add_tile(self, tile_code):
        cur_tiles = self.get_qs_tiles()
        tile_code = tile_code.replace('(', r'\(').replace(')', r'\)')
        tiles_arg = ','.join([*List(cur_tiles).prepend(tile_code, dup=False)])
        self.device.shell(f'settings put secure sysui_qs_tiles "{tiles_arg}"')

    def open(self):
        self.device.d.open_quick_settings()
        return self
