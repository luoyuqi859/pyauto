#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: app
@Created: 2023/2/25
"""
import re
from collections import namedtuple
from datetime import datetime

from adbutils import AdbError

from conf import settings
from utils import net
from utils.errors import UiaError
from utils.log import logger


class App:
    def __init__(self, device):
        self.device = device
        self.package = None
        self.apk = None

    def __call__(self, package=None, activity=None, name=None, apk=None, url=None):
        self.package = package
        self.activity = activity
        self.name = name
        if apk:
            self.apk = apk
        self.url = url
        return self

    def get_info(self):
        """
        获取应用信息
        :return:
        """
        output = self.device.shell(f'dumpsys package {self.package}')
        m = re.compile(r'versionName=(?P<name>[\d.]+)').search(output)
        version_name = m.group('name') if m else ""
        m = re.compile(r'versionCode=(?P<code>\d+)').search(output)
        version_code = m.group('code') if m else ""
        if version_code == "0":
            version_code = ""
        m = re.search(r'PackageSignatures{.*?\[(.*)\]\}', output)
        signature = m.group(1) if m else None
        if not version_name and signature is None:
            return None
        m = re.compile(r"pkgFlags=\[\s*(.*)\s*\]").search(output)
        pkg_flags = m.group(1) if m else ""
        pkg_flags = pkg_flags.split()

        time_regex = r"[-\d]+\s+[:\d]+"
        m = re.compile(f"firstInstallTime=({time_regex})").search(output)
        first_install_time = datetime.strptime(m.group(1), settings.DEFAULT_TIME_FORMAT) if m else None

        m = re.compile(f"lastUpdateTime=({time_regex})").search(output)
        last_update_time = datetime.strptime(m.group(1).strip(),
                                             settings.DEFAULT_TIME_FORMAT) if m else None

        return dict(version_name=version_name,
                    version_code=version_code,
                    flags=pkg_flags,
                    first_install_time=first_install_time,
                    last_update_time=last_update_time,
                    signature=signature)

    def start(self):
        """
        启动应用
        :return:
        """
        if not self.package:
            raise AdbError('Unknown package!')
        if not self.activity:
            self.device.shell(f'am start {self.package} -W')
        else:
            self.device.shell(f'am start -n {self.package}/{self.activity} -W')
        logger.success(f'Start app: {self.name or self.package}')

    def stop(self):
        """
        停止应用
        :return:
        """
        if not self.package:
            raise AdbError('Unknown package!')
        self.device.shell(f'am force-stop {self.package}')

    def install(self, opts=None):
        """
        安装apk

        :param opts: -l 锁定应用程序；
                     -r 卸载安装；
                     -t 允许安装测试包；
                     -d 允许降级覆盖安装；
                     -p 部分应用安装；
                     -g 授权所有运行时权限
        :param timeout: 超时
        :return:
        """
        if opts is None:
            opts = []
        command = f'install {" ".join(opts)} "{self.apk}"'
        return self.device.adb_fp.adb.run_adb_cmd(command)

    def install_url(self, url, opts=None, timeout=None, headers=None):
        apk_path = net.download(url, timeout, headers=headers)
        self.apk = apk_path
        self.install(opts=opts)

    def uninstall(self, opts=None):
        if opts is None:
            opts = ''
        elif isinstance(opts, (list, tuple)):
            opts = ' '.join(opts)
        command = f'pm uninstall {opts} {self.package}'
        return self.device.shell(command)

    def pid(self):
        output = self.device.shell(f'"ps | grep {self.package}"')
        for line in output.splitlines():
            arr = re.split(r'\s+', line)
            pid, pkg = int(arr[1]), arr[-1]
            if self.package == pkg:
                return pid

    def grant(self, *permissions):
        for permission in permissions:
            self.device.shell(f'pm grant {self.package} {permission}')
        return self

    def current(self):
        _focusedRE = re.compile(r'mCurrentFocus=Window{.*\s+(?P<package>[^\s]+)/(?P<activity>[^\s]+)\}')
        s = self.device.shell(['dumpsys', 'window', 'windows'])
        m = _focusedRE.search(s)
        if m:
            return dict(package=m.group('package'), activity=m.group('activity'))

        # try: adb shell dumpsys activity top
        _activityRE = re.compile(r'ACTIVITY (?P<package>[^\s]+)/(?P<activity>[^/\s]+) \w+ pid=(?P<pid>\d+)')
        output = self.device.shell(['dumpsys', 'activity', 'top'])
        ms = _activityRE.finditer(output)
        ret = None
        for m in ms:
            ret = dict(package=m.group('package'), activity=m.group('activity'), pid=int(m.group('pid')))
        if ret:  # get last result
            return ret
        raise EnvironmentError("Couldn't get focused app")

    def list_package(self, opts=None):
        if not opts:
            opts = []
        opts = ' '.join(opts)
        output = self.device.shell(f'pm list package {opts}')
        for line in output.split('\n'):
            yield line.replace('package:', '').strip()

    def installed(self):
        return self.package in list(self.list_package())

    def list_running(self) -> list:
        """
        列出所有运行中的 app
        :return:
        """
        output = self.device.shell('pm list packages')
        packages = re.findall(r'package:([^\s]+)', output)
        process_names = re.findall(r'([^\s]+)$', self.device.shell('ps; ps -A'), re.M)
        return list(set(packages).intersection(process_names))

    def quit_all(self):
        """
        退出测试过程中被打开的应用
        """
        apps = getattr(self.device, '_running_apps', [])
        for pkg in apps:
            self.device.app(pkg).stop()


class UiaApp(App):
    def get_info(self, pkg_name=None):
        """
        获取应用信息，包括 main_activity、label、version_name、version_code、size
        :param pkg_name: 应用包名
        :return:
        """
        pkg_name = pkg_name or self.package
        resp = self.device.request("get", f"/packages/{pkg_name}/info")
        resp.raise_for_status()
        resp = resp.json()
        if not resp.get('success'):
            raise UiaError(resp.get('description', 'unknown'))
        AppInfo = namedtuple('AppInfo', ('main_activity', 'label', 'version_name', 'version_code', 'size'))
        data = resp.get('data')
        return AppInfo(main_activity=data.get('mainActivity'),
                       label=data.get('label'),
                       version_name=data.get('versionName'),
                       version_code=data.get('versionCode'),
                       size=data.get('size'))
