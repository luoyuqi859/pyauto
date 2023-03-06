#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: adb
@Created: 2023/2/22 18:00
"""
import os
import platform
import re
import subprocess
import threading
import time
from typing import List

import whichcraft

from utils.allure_fun import attach_text
from utils.errors import AdbError
from utils.log import logger
from utils.path_fun import Path
from utils.s import Str
from utils.time_fun import timeoperator


class AdbOperator:

    def __init__(self, device_id=None):
        self._adb_path = AdbOperator.location()
        self._device_id = device_id
        self.before_connect = True
        self.after_connect = True
        self._sdk_version = None

    @staticmethod
    def location():
        """获取ADB路径"""
        p = whichcraft.which("adb")
        if p is None:
            os_name = platform.system()
            logger.debug(f"platform : {os_name}")
            if os_name == "Windows":
                adb_dir = Path(__file__).parent / 'sdk' / 'adb.exe'
                return os.path.abspath(adb_dir)
            elif os_name == "Darwin":
                adb_dir = Path(__file__).parent / 'sdk' / 'platform-tools-latest-darwin' / 'platform-tools' / 'adb'
                return os.path.abspath(adb_dir)
            else:
                adb_dir = Path(__file__).parent / 'sdk' / 'platform-tools-latest-linux' / 'platform-tools' / 'adb'
                return os.path.abspath(adb_dir)
        else:
            return "adb"

    @property
    def serial(self):
        if not self._device_id:
            for serial, _ in self.devices():
                return serial
        return self._device_id

    def devices(self):
        """adb devices"""
        try:
            result = self.run_adb_cmd('devices')
            if result:
                lines = result.splitlines()
                for line in lines:
                    arr = line.strip().split('\t')
                    if len(arr) < 2:
                        continue
                    yield arr
        except (TimeoutError, subprocess.TimeoutExpired):
            self.kill_server()
            time.sleep(5)
            self.start_server()

    def connect(self, ip, port):
        """
        远程连接
        @param ip:
        @param port:
        @return:
        """
        self.run_adb_cmd(f"connect {ip}:{port}")

    def disconnect(self, ip, port):
        """
        断开远程连接
        @param ip:
        @param port:
        @return:
        """
        self.run_adb_cmd(f"disconnect {ip}:{port}")

    def start_server(self):
        """开启 adb 服务"""
        return self.run_adb_cmd('start-server')

    def kill_server(self):
        """关闭adb服务进程"""
        return self.run_adb_cmd('kill-server')

    def list_device(self) -> List:
        """
        获取设备列表
        :return:
        """
        proc = subprocess.Popen(f"{self._adb_path} devices", stdout=subprocess.PIPE, shell=True)
        result = proc.stdout.read()
        if not isinstance(result, str):
            result = result.decode('utf-8')
        result = result.replace('\r', '').splitlines()
        logger.debug(f"adb devices:{result}")
        device_list = []
        for device in result[1:]:
            if len(device) <= 1 or not '\t' in device: continue
            if device.split('\t')[1] == 'device':
                # 只获取连接正常的
                device_list.append(device.split('\t')[0])
        return device_list

    def _timer(self, process, timeout):
        """
        进程超时器
        监控adb同步命令执行是否超时，超时强制结束执行
        当timeout<=0时，永不超时

        :param Popen process: 子进程对象
        :param int timeout: 超时时间
        """
        num = 0
        while process.poll() is None and num < timeout * 10:
            num += 1
            time.sleep(0.1)
        if process.poll() is None:
            logger.warning(f"{process.pid}进程超时,强行关闭")
            process.terminate()

    def _run_cmd_once(self, cmd, *argv, **kwds):
        """
        执行一次adb命令

        :param str cmd: 命令字符串
        :param list argv: 可变参数
        :param dict kwds: 可选关键字参数 (超时/异步)
        :return: 执行adb命令的子进程或执行的结果
        :rtype: Popen or str
        """
        if self._device_id:
            cmdlet = [self._adb_path, '-s', self._device_id, cmd]
        else:
            cmdlet = [self._adb_path, cmd]
        for i in range(len(argv)):
            arg = argv[i]
            if not isinstance(argv[i], str):
                arg = arg.decode('utf8')
            cmdlet.append(arg)
        cmdStr = " ".join(cmdlet)
        # logger.debug(f'执行的语句为{cmdStr}')
        process = subprocess.Popen(cmdStr,
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   shell=True)
        if "sync" in kwds and kwds['sync'] == False:
            # 异步执行命令，不等待结果，返回该子进程对象
            return process
        before = time.time()
        timeout = 10
        if "timeout" in kwds:
            timeout = kwds['timeout']
        if timeout is not None and timeout > 0:
            threading.Thread(target=self._timer, args=(process, timeout))
        (out, error) = process.communicate()
        # 执行错误
        # * mac     out无输出  error有输出   返回值非0
        # * windows out有输出  error没有输出  返回值0
        if process.poll() != 0:  # 返回码为非0，表示命令未执行成功返回
            if error and len(error) != 0:
                logger.debug(f"adb执行:\n{error}")
            if "no devices/emulators found" in str(out) or "no devices/emulators found" in str(error):
                logger.error("没有找到设备或模拟器,请重连,检查adb shell是否正常")
                return ""
            # 退出整个进程
            if "killing" in str(out) or "killing" in str(error):
                logger.error("adb默认端口5037被占用")
                return ""
            if "device not found" in str(out) or "device not found" in str(error):
                logger.error("没有找到设备,请重连")
                self.before_connect = False
                self.after_connect = False
                return ""
            if "offline" in str(out) or "offline" in str(error):
                logger.error("设备离线,请重连")
                return ""
            if "more than one" in str(out) or "more than one" in str(error):
                logger.error("设备不止一个,请确认!")
            if "Android Debug Bridge version" in str(out) or "Android Debug Bridge version" in str(error):
                logger.error(f"adb cmd 异常!:{out}")
        if str(out, "utf-8") == '':
            out = error
        self.after_connect = True
        after = time.time()
        time_consume = after - before
        logger.info(f"执行{cmdStr}耗时{time_consume:.2f}秒")
        if not isinstance(out, str):
            try:
                out = str(out, "utf8")
            except Exception:
                out = repr(out)
        return out.strip()

    def is_process_running(self, process_name):
        '''判断进程是否存活
        '''
        process_list = self.list_process()
        for process in process_list:
            if process['proc_name'] == process_name:
                return True
        return False

    def run_adb_cmd(self, cmd, *argv, **kwds):
        """
        尝试执行adb命令

        :param str cmd: 命令字符串
        :param list argv: 可变参数
        :param dict kwds: 可选关键字参数 (超时/异步)
        :return: 执行adb命令的子进程或执行的结果
        :rtype: Popen or str
        """
        retry_count = 3  # 默认最多重试3次
        ret = ""
        if "retry_count" in kwds:
            retry_count = kwds['retry_count']
        for i in range(retry_count):
            ret = self._run_cmd_once(cmd, *argv, **kwds)
            if ret is not None:
                break
        return ret

    def run_shell_cmd(self, cmd, **kwds):
        """
        执行 adb shell 命令
        """
        ret = self.run_adb_cmd('shell', '%s' % cmd, **kwds)
        # 当 adb 命令传入 sync=False时，ret是Poen对象
        if ret is None:
            logger.error(f'执行「{cmd}」异常')
        return ret

    def bugreport(self, save_path=None):
        """
        adb bugreport ~/report/bugreport.zip
        """
        # if not save_path:
        #     save_path = os.path.join(REPORT_PATH, f"bugreport{timeoperator.now4}.zip")
        result = self.run_adb_cmd('bugreport', save_path)
        attach_text(save_path, 'bugreport存放路径')
        return result

    def check_path_size(self, folder_path, ratio):
        """
        检测手机上目录空间占比，超过多少比例
        """
        out = self.run_shell_cmd('df %s' % folder_path)
        logger.debug(out)
        if out:
            lines = out.replace('\r', '').splitlines()
            occupy_ratio = lines[1].split()[4].replace("%", "")
            logger.debug(occupy_ratio)
            if int(occupy_ratio) > ratio:
                return True
        return False

    def get_package_ver(self, package):
        """
        获取应用版本信息
        """
        package_ver = self.run_shell_cmd("dumpsys package " + package)
        if package_ver:
            return package_ver
        else:
            return ""

    @property
    def phone_brand(self):
        """
        获取手机品牌  如：Mi Samsung OnePlus
        """
        return self.run_shell_cmd('getprop ro.product.brand')

    @property
    def phone_model(self):
        """
        获取手机型号  如：A0001 M2S
        """
        return self.run_shell_cmd('getprop ro.product.model')

    @property
    def screen_size(self):
        """
        获取屏幕分辨率  如：Physical size: 1080x2400
        """
        return self.run_shell_cmd('wm size')

    @property
    def sdk_version(self):
        """
        获取SDK版本，如：30
        """
        return int(self.run_shell_cmd('getprop ro.build.version.sdk'))

    def get_sdk_version(self):
        if not self._sdk_version:
            self._sdk_version = self.sdk_version
        return self._sdk_version

    def get_cpu_abi(self):
        """
        获取系统的CPU架构信息

        :return: 返回系统的CPU架构信息 如arm64-v8a
        :rtype: str
        """
        return self.run_shell_cmd('getprop ro.product.cpu.abi')

    def reboot(self, boot_type=None):
        """
        重启手机
        boot_type: "bootloader", "recovery", or "None".
        """
        if boot_type:
            self.run_adb_cmd('reboot ' + boot_type)
        else:
            self.run_adb_cmd('reboot')

    def list_dir(self, dir_path):
        """
        获取目录下文件 文件夹
        返回 文件名 列表
        """
        result = self.run_shell_cmd('ls -l %s' % dir_path)
        if not result:
            return ""
        result = result.replace('\r\r\n', '\n')
        if 'No such file or directory' in result:
            logger.error(f'文件(夹) {dir_path} 不存在')
        file_list = []
        for line in result.split('\n'):
            items = line.split()
            if items[0] != "total" and len(items) != 2:
                file_list.append(items[-1])
        return file_list

    def is_overtime_days(self, filepath, days=7):
        result = self.run_shell_cmd('ls -l %s' % filepath)
        if not result:
            return False
        result = result.replace('\r\r\n', '\n')
        if 'No such file or directory' in result:
            logger.error(f'文件(夹) {filepath} 不存在')
            return False
        re_time = re.compile(r'\S*\s+(\d+-\d+-\d+\s+\d+:\d+)\s+\S+')
        match = re_time.search(result)
        if match:
            last_modify_time = match.group(1)
            logger.debug(last_modify_time)
            last_modify_timestamp = timeoperator.get_time_stamp(last_modify_time, "%Y-%m-%d %H:%M")
            if last_modify_timestamp < (time.time() - days * 24 * 60 * 60):
                logger.debug(f"{filepath}的创建时间大于{days}天")
                logger.debug(filepath + " is overtime days:" + str(days))
                return True
            else:
                logger.debug(f"{filepath}的创建时间小于{days}天")
                return False
        logger.debug(f"{filepath}文件没有找到时间信息")
        return False

    def delete_file(self, file_path):
        """
        删除手机上文件
        """
        self.run_shell_cmd('rm %s' % file_path)

    def delete_folder(self, folder_path):
        """
        删除手机上的目录
        """
        self.run_shell_cmd('rm -R %s' % folder_path)

    def get_top_cmd(self, interval):
        """

        @param interval: 采集的频率
        @return:
        """
        # top可能会有进程名显示不全的问题 加-b即可
        top_cmd = f'top -b -n 1 -d {interval}'
        ret = self.run_shell_cmd(top_cmd)
        if ret and 'Invalid argument "-b"' in ret:
            logger.debug("不允许使用top -b")
            top_cmd = f'top -n 1 -d {interval}'
        return top_cmd

    def get_focus_activity(self):
        """
        通过dumpsys window windows获取activity名称  window名?
        """
        activity_name = ''
        activity_line = ''
        dumpsys_result = self.run_shell_cmd('dumpsys window windows')
        dumpsys_result_list = dumpsys_result.split('\n')
        for line in dumpsys_result_list:
            if line.find('mCurrentFocus') != -1:
                activity_line = line.strip()
        if activity_line:
            activity_line_split = activity_line.split(' ')
        else:
            return activity_name
        logger.debug(f'dumpsys window windows命令结果:{activity_line_split}')
        if len(activity_line_split) > 1:
            if activity_line_split[1] == 'u0':
                activity_name = activity_line_split[2].rstrip('}')
            else:
                activity_name = activity_line_split[1]
        return activity_name

    def pull_file(self, src_path, dst_path):
        """
        从手机中拉取文件
        """
        result = self.run_adb_cmd('pull', src_path, dst_path)
        if result and 'failed to copy' in result:
            logger.error("failed to pull file:" + src_path)
        return result

    def dumpheap(self, package, save_path):
        heapfile = "/data/local/tmp/%s_dumpheap_%s.hprof" % (package, timeoperator.strftime_now("%Y_%m_%d_%H_%M_%S"))
        self.run_shell_cmd("am dumpheap %s %s" % (package, heapfile))
        time.sleep(10)
        self.pull_file(heapfile, save_path)

    def get_pid_from_pck(self, package_name):
        """
        从ps信息中通过匹配包名，获取进程pid号，对于双开应用统计值会返回两个不同的pid后面再优化
        :param pckname: 应用包名
        :return: 该进程的pid
        """
        pckinfo_list = self.get_pckinfo_from_ps(package_name)
        if pckinfo_list:
            return pckinfo_list[0]["pid"]

    def get_pckinfo_from_ps(self, packagename):
        """
        从ps中获取应用的信息:pid,uid,packagename
        :param packagename: 目标包名
        :return: 返回目标包名的列表信息
        """
        ps_list = self.list_process()
        pck_list = []
        for item in ps_list:
            if item["proc_name"] == packagename:
                pck_list.append(item)
        return pck_list

    def get_process_stack_from_pid(self, pid, save_path):
        '''
        :param package_name: 进程名
        :param save_path: 堆栈文件保存路径
        :return: 无
        '''
        return self.run_shell_cmd("debuggerd -b %s > %s" % (pid, save_path))

    def kill_process(self, process_name):
        '''杀死包含指定进程
        '''
        pids = self.get_process_pids(process_name)
        if pids:
            self.run_shell_cmd('kill ' + ' '.join([str(pid) for pid in pids]))
        return len(pids)

    def get_process_pids(self, process_name):
        '''查找包含指定进程名的进程PID
        '''
        pids = []
        process_list = self.list_process()
        for process in process_list:
            if process['proc_name'] == process_name:
                pids.append(process['pid'])
        return pids

    def list_process(self):
        """
        获取进程列表
        """
        # <= 7.0 用ps, >=8.0 用ps -A android8.0 api level 26
        result = None
        if self.get_sdk_version() < 26:
            result = self.run_shell_cmd('ps')  # 不能使用grep
        else:
            result = self.run_shell_cmd('ps -A')  # 不能使用grep
        result = result.replace('\r', '')
        lines = result.split('\n')
        busybox = False
        if lines[0].startswith('PID'): busybox = True

        result_list = []
        for i in range(1, len(lines)):
            items = lines[i].split()
            if not busybox:
                if len(items) < 9:
                    err_msg = "ps命令返回格式错误：\n%s" % lines[i]
                    if len(items) == 8:
                        result_list.append({'uid': items[0], 'pid': int(items[1]), 'ppid': int(items[2]),
                                            'proc_name': items[7], 'status': items[-2]})
                    else:
                        logger.error(err_msg)
                else:
                    result_list.append({'uid': items[0], 'pid': int(items[1]), 'ppid': int(items[2]),
                                        'proc_name': items[8], 'status': items[-2]})
            else:
                idx = 4
                cmd = items[idx]
                if len(cmd) == 1:
                    # 有时候发现此处会有“N”
                    idx += 1
                    cmd = items[idx]
                idx += 1
                if cmd[0] == '{' and cmd[-1] == '}': cmd = items[idx]
                ppid = 0
                if items[1].isdigit(): ppid = int(items[1])  # 有些版本中没有ppid
                result_list.append({'pid': int(items[0]), 'uid': items[1], 'ppid': ppid,
                                    'proc_name': cmd, 'status': items[-2]})
        return result_list

    def push(self, src, dest, reboot=False):
        command = f'push "{src}" "{dest}"'
        result = self.run_adb_cmd(command)
        if reboot:
            self.reboot()
        return result

    def pull(self, src, dest):
        command = f'pull "{src}" "{dest}"'
        result = self.run_adb_cmd(command, self.serial)
        return result

    def path(self, path):
        return AdbAndroidPath(path, self)

    def shell(self, command):
        return self.run_shell_cmd(command)


class AdbAndroidPath(Str):
    def __init__(self, o, adb):
        super().__init__()
        self.adb = adb

    @property
    def size(self):
        return self.adb.shell(f'du -ha {self}').split()[0]

    @property
    def is_dir(self):
        output = self.adb.shell(f'ls -al {self}')
        return output.startswith('total')

    @property
    def is_file(self):
        return not self.is_dir

    @property
    def exists(self):
        try:
            output = self.adb.shell(f'ls {self}')
            if 'No such file or directory' in output:
                return False
            return True
        except AdbError:
            return False

    def cat(self):
        return self.adb.shell(f'cat {self}')

    def ls(self):
        try:
            for f in self.adb.shell(f'ls {self}').splitlines():
                yield self.__class__(self / f, self.adb)
        except AdbError:
            return []

    def mkdir(self, path=None):
        if not path:
            try:
                self.adb.shell(f'mkdir {self}')
                return True
            except Exception as e:
                if 'File exists' in str(e):
                    return
                e.__class__ = AdbError
                raise e
        else:
            return self.__class__(self / path, self.adb).mkdir()

    def chmod(self, auth='777'):
        self.adb.shell(f'chmod {auth} -R {self}')

    def rm(self, path=None, opts=None):
        """移除目录或子目录"""
        if not path:
            if not opts:
                opts = ''
            try:
                self.adb.shell(f'rm {opts} {self}')
                return True
            except Exception as e:
                if 'No such file or directory' in str(e):
                    return
                e.__class__ = AdbError
                raise e
        else:
            return AdbAndroidPath(self / path, self.adb).rm(opts=opts)

    def clear(self, raise_err=False):
        try:
            self.adb.shell(f'rm -r {self}/*')
        except AdbError:
            if raise_err:
                raise

    def pull(self, local_path='.'):
        self.adb.pull(self, local_path)

    def delete_files(self, file_pattern='*'):
        self.adb.shell(f'rm -r {self}/{file_pattern}')

    def __truediv__(self, other):
        if self[-1] == '/':
            return self.__class__(self + other, self.adb)
        else:
            return self.__class__(self + '/' + other, self.adb)


class ADB():
    """
    adb
    """

    def __init__(self, device_id=None):
        self.adb = AdbOperator(device_id)


if __name__ == '__main__':
    a = ADB()
    # a.adb.run_shell_cmd("mkdir /data/local/tmp")
    print(a.adb.path("/data/local/tmp/minicap").exists)
    print(Path(__file__).parent / 'sdk' / 'adb.exe')
    print(a.adb.location())
    print(a.adb.serial)
    print(a.adb.phone_brand)
    print(a.adb.phone_model)
    print(a.adb.screen_size)
    print(a.adb.sdk_version)
    print(a.adb.get_cpu_abi())
    print(a.adb.serial)
