#! /usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: atx_uninstall
@Created: 2023/3/2 17:26
"""
from uiauto.android.adb import ADB

adb = ADB()


def uninstall_atx():
    adb.adb.shell("/data/local/tmp/atx-agent server --stop")
    adb.adb.shell("rm /data/local/tmp/atx-agent")
    print("atx-agent stopped and removed")
    adb.adb.shell("rm /data/local/tmp/minicap")
    adb.adb.shell("rm /data/local/tmp/minicap.so")
    adb.adb.shell("rm /data/local/tmp/minitouch")
    # adb.adb.shell(["rm", "/data/local/tmp/minicap"])
    # adb.adb.shell(["rm", "/data/local/tmp/minicap.so"])
    # adb.adb.shell(["rm", "/data/local/tmp/minitouch"])
    # adb.adb.shell("rm /data/local/tmp/minitouch")
    print("minicap, minitouch removed")
    adb.adb.shell("pm uninstall com.github.uiautomator")
    adb.adb.shell("pm uninstall com.github.uiautomator.test")
    print("com.github.uiautomator uninstalled, all done !!!")


if __name__ == '__main__':
    uninstall_atx()
