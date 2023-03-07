#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: aapt
@Created: 2023/3/7 15:58
"""
import os
import re
import subprocess

from panda.utils.path import Path


def location(v=None):
    android_home = os.getenv('android_home')
    if android_home:
        _dir = os.path.join(android_home, 'build-tools')
    else:
        _dir = Path(__file__).parent / 'sdk' / 'aapt'
    for f in Path(_dir).search('aapt.exe'):
        if v:
            if str(v) in f.replace(_dir, ''):
                return f
        else:
            return f
    return None


class ApkInfo:
    def __init__(self, apk_path):
        self._apk_path = apk_path
        self._size = 0
        self._info = {}

    @property
    def apk_path(self):
        return self._apk_path

    @property
    def size(self):
        """
        size of apk with unit "M"

        :return:
        """
        if not self._size:
            self._size = round(os.path.getsize(self.apk_path) / (1024 * 1000), 2)
        return self._size

    @property
    def name(self):
        if not self._info:
            self.__get_info()
        return self._info.get('name')

    @property
    def package(self):
        if not self._info:
            self.__get_info()
        return self._info.get('package')

    @property
    def activity(self):
        if not self._info:
            self.__get_info()
        return self._info.get('activity')

    @property
    def version(self):
        if not self._info:
            self.__get_info()
        return self._info.get('version')

    @property
    def version_code(self):
        if not self._info:
            pass
        return self._info.get('version_code')

    def __get_info(self):
        p = subprocess.Popen(f'"{location()}" dump badging {self.apk_path}',
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             stdin=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        if err:
            raise Exception(err)
        output = output.decode()
        p = re.compile(r"package: name='(?P<package>\S+)' "
                       r"versionCode='(?P<version_code>\d+)' "
                       r"versionName='(?P<version>\S+)'.*"
                       r"application.{1,5}label[:=]'(?P<name>.*?)'", re.DOTALL)
        match = p.search(output)
        self._info.update(match.groupdict() if match else {})
        p = re.compile(r"launchable-activity: name='(\S+)'")
        match = p.search(output)
        activity = match.groups()[0] if match else None
        self._info['activity'] = activity

    def __str__(self):
        return f'{self.name}, {self.package}, {self.version}'
