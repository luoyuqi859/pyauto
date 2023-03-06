#! /usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: minicap
@Created: 2023/3/1 13:44
"""
import os

from conf import settings
from utils.log import logger


class Minicap:
    def __init__(self, device=None):
        self.device = device

    def install_minicap(self):
        if self.device.adb_fp.adb.path('/data/local/tmp/minicap').exists:
            logger.debug("minicap exists")
            return
        abi = self.device.adb_fp.adb.get_cpu_abi()
        sdk = self.device.adb_fp.adb.sdk_version
        minicap = settings.minicap_path / f"{abi}" / "bin" / "minicap"
        minicap_so = settings.minicap_path / f"{abi}" / "lib" / f"android-{sdk}" / "minicap.so"
        minitouch = settings.minitouch_path / f"{abi}" / "bin" / "minitouch"
        self.device.adb_fp.adb.push(minicap, '/data/local/tmp')
        self.device.adb_fp.adb.push(minitouch, '/data/local/tmp')
        if os.path.exists(minicap_so):
            self.device.adb_fp.adb.push(minicap_so, '/data/local/tmp')
        self.device.adb_fp.adb.path('/data/local/tmp/minicap').chmod(775)
        self.device.adb_fp.adb.path('/data/local/tmp/minitouch').chmod(775)
        logger.debug("minicap minicap.so push successful")
