#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: atx_uninstall
@Created: 2023/3/2 17:26
"""
from uiauto.android.adb import ADB
from loguru import logger

adb = ADB()
adb_devices = {item[0]: item[1] for item in adb.adb.devices()}


def uninstall_atx():
    for serial, _ in adb_devices.items():
        adb = ADB(serial)
        adb.adb.shell("/data/local/tmp/atx-agent server --stop")
        adb.adb.shell("rm /data/local/tmp/atx-agent")
        logger.debug("atx-agent stopped and removed")
        adb.adb.shell("rm /data/local/tmp/minicap")
        adb.adb.shell("rm /data/local/tmp/minicap.so")
        adb.adb.shell("rm /data/local/tmp/minitouch")
        # adb.adb.shell(["rm", "/data/local/tmp/minicap"])
        # adb.adb.shell(["rm", "/data/local/tmp/minicap.so"])
        # adb.adb.shell(["rm", "/data/local/tmp/minitouch"])
        # adb.adb.shell("rm /data/local/tmp/minitouch")
        logger.debug("minicap, minitouch removed")
        adb.adb.shell("pm uninstall com.github.uiautomator")
        adb.adb.shell("pm uninstall com.github.uiautomator.test")
        logger.debug("com.github.uiautomator uninstalled, all done !!!")


if __name__ == '__main__':
    uninstall_atx()
