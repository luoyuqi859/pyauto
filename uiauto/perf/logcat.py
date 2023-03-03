#!/usr/bin/env python
# -*- ecoding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: logcat
@Created: 2023/3/2 14:23
"""
import csv
import os
import threading
import time
import traceback

from conf import settings
from uiauto.android.adb import ADB
from utils.log import logger
from utils.time_fun import timeoperator
from utils.tools import TimeUtils, ms2s


class LogcatCollector(object):

    def __init__(self, device, path=None):
        self.device = device
        self._path = path
        self._logcat_handle = []

    def start(self, process_list=None, params=None):
        '''运行logcat进程

        :param list process_list: 要捕获日志的进程名或进程ID列表，为空则捕获所有进程,输入 ['system_server']可捕获系统进程的日志
        :param str params: 参数
        '''
        if hasattr(self, '_logcat_running') and self._logcat_running == True:
            logger.warning('logcat process have started,not need start')
            return
        # sdk 26一下可以执行logcat -c的操作， 8.0以上的系统不能执行，会报"failed to clear the 'main' log"的错 图兰朵没问题
        # if self.get_sdk_version() <  26:
        try:  # 有些机型上会报permmison denied，但是logcat -c的代码仍会部分执行，所以加try 保护
            self.device.adb.run_shell_cmd('logcat -c ' + params)  # 清除缓冲区
        except RuntimeError as e:
            logger.warning(e)
        self._logcat_running = True  # logcat进程是否启动
        self._log_pipe = self.device.adb.run_shell_cmd('logcat -v threadtime ' + params, sync=False)
        self._logcat_thread = threading.Thread(target=self.logcat_thread_func, args=[self._path, process_list, params])
        self._logcat_thread.setDaemon(True)
        self._logcat_thread.start()

    def stop(self):
        '''停止logcat进程
        '''
        self._logcat_running = False
        logger.debug("stop logcat")
        if hasattr(self, '_log_pipe'):
            if self._log_pipe.poll() == None:  # 判断logcat进程是否存在
                self._log_pipe.terminate()

    def logcat_thread_func(self, save_dir, process_list, params=""):
        '''获取logcat线程
                '''
        self.append_log_line_num = 0
        self.file_log_line_num = 0
        self.log_file_create_time = None
        logs = []
        logger.debug("logcat_thread_func")
        log_is_none = 0
        while self._logcat_running:
            try:
                log = self._log_pipe.stdout.readline().strip()
                if not isinstance(log, str):
                    try:
                        log = str(log, "utf8")
                    except Exception as e:
                        log = repr(log)
                        logger.error('str error:' + log)
                        logger.error(e)
                if log:
                    log_is_none = 0
                    # logger.debug(log)
                    logs.append(log)
                    # if self._log_pipe.poll() != None:
                    #     logger.debug('process:%s have exited' % self._log_pipe.pid)
                    #     if self._logcat_running :
                    #         self._log_pipe = self.run_shell_cmd('logcat ' + params, sync=False)
                    #     else :
                    #         break
                    for _handle in self._logcat_handle:
                        try:
                            _handle(log)
                        except Exception as e:
                            logger.error("an exception happen in logcat handle log , reason unkown!, e:")
                            logger.error(e)

                    self.append_log_line_num = self.append_log_line_num + 1
                    self.file_log_line_num = self.file_log_line_num + 1
                    # if self.append_log_line_num > 1000:
                    if self.append_log_line_num > 100:
                        if not self.log_file_create_time:
                            self.log_file_create_time = TimeUtils.getCurrentTimeUnderline()
                        logcat_file = os.path.join(save_dir,
                                                   'logcat_%s.log' % self.log_file_create_time)
                        self.append_log_line_num = 0
                        self.save(logcat_file, logs)
                        logs = []
                    # 新建文件
                    if self.file_log_line_num > 600000:
                        # if self.file_log_line_num > 200:
                        self.file_log_line_num = 0
                        self.log_file_create_time = TimeUtils.getCurrentTimeUnderline()
                        logcat_file = os.path.join(save_dir, 'logcat_%s.log' % self.log_file_create_time)
                        self.save(logcat_file, logs)
                        logs = []
                else:
                    log_is_none = log_is_none + 1
                    if log_is_none % 1000 == 0:
                        logger.info("log is none")
                        self._log_pipe = self.device.adb.run_shell_cmd('logcat -v threadtime ' + params, sync=False)
            except:
                logger.error("an exception hanpend in logcat thread, reason unkown!")
                s = traceback.format_exc()
                logger.debug(s)

    def save(self, save_file_path, loglist):
        logcat_file = os.path.join(save_file_path)
        with open(logcat_file, 'a+', encoding="utf-8") as logcat_f:
            for log in loglist:
                logcat_f.write(log + "\n")


class LaunchTime(object):

    def __init__(self, deviceid, packagename=None, path=None):
        # 列表的容积应该不用担心，与系统有一定关系，一般存几十万条数据没问题的
        self.launch_list = [("datetime", "packagenme/activity", "this_time(s)", "total_time(s)", "launchtype")]
        self.packagename = packagename
        self.path = path

    def handle_launchtime(self, log_line):
        '''
        这个方法在每次一个启动时间的log产生时回调
        :param log_line:最近一条的log 内容
        :param tag:启动的方式，是normal的启动，还是自定义方式的启动：fullydrawnlaunch
        #如果监控到到fully drawn这样的log，则优先统计这种log，它表示了到起始界面自定义界面的启动时间
        :return:void
        '''
        # logger.debug(log_line)
        # 08-28 10:57:30.229 18882 19137 D IC5: CLogProducer == > code = 0, uuid = 4FE71E350379C64611CCD905938C10CA, eventType = performance, eventName = am_activity_launch_timeme, \
        #    log_time = 2019-08-28 10:57:30.229, contextInfo = {"tag": "am_activity_launch_time", "start_time": "2019-08-28 10:57:16",
        #                              "activity_name_original": "com.android.settings\/.FallbackHome",
        #                              "activity_name": "com.android.settings#com.android.settings.FallbackHome",
        #                              "this_time": "916", "total_time": "916", "start_type": "code_start",
        #                              "gmt_create": "2019-08-28 10:57:16.742", "uploadtime": "2019-08-28 10:57:30.173",
        #                              "boottime": "2019-08-28 10:57:18.502", "firstupload": "2019-08-28 10:57:25.733"}
        ltag = ""
        if ("am_activity_launch_time" in log_line or "am_activity_fully_drawn_time" in log_line):
            # 最近增加的一条如果是启动时间相关的log，那么回调所有注册的_handle
            if "am_activity_launch_time" in log_line:
                ltag = "normal launch"
            elif "am_activity_fully_drawn_time" in log_line:
                ltag = "fullydrawn launch"
            logger.debug("launchtime log:" + log_line)
        if ltag:
            content = []
            timestamp = time.time()
            content.append(TimeUtils.formatTimeStamp(timestamp))
            temp_list = log_line.split()[-1].replace("[", "").replace("]", "").split(',')[2:5]
            for i in range(len(temp_list)):
                content.append(temp_list[i])
            content.append(ltag)
            logger.debug("Launch Info: " + str(content))
            if len(content) == 5:
                content = self.trim_value(content)
                if content:
                    self.update_launch_list(content, timestamp)

    def trim_value(self, content):
        try:
            content[2] = ms2s(float(content[2]))  # 将this_time转化单位转化为s
            content[3] = ms2s(float(content[3]))  # 将total_time 转化为s
        except Exception as e:
            logger.error(e)
            return []
        return content

    def update_launch_list(self, content, timestamp):
        # if self.packagename in content[1]:
        self.launch_list.append(content)
        tmp_file = os.path.join(self.path, 'launch_logcat.csv')
        perf_data = {"task_id": "", 'launch_time': [], 'cpu': [], "mem": [],
                     'traffic': [], "fluency": [], 'power': [], }
        dic = {"time": timestamp,
               "act_name": content[1],
               "this_time": content[2],
               "total_time": content[3],
               "launch_type": content[4]}
        perf_data['launch_time'].append(dic)
        # perf_queue.put(perf_data)

        with open(tmp_file, "a+", encoding="utf-8") as f:
            csvwriter = csv.writer(f, lineterminator='\n')  # 这种方式可以去除csv的空行
            logger.debug("save launchtime data to csv: " + str(self.launch_list))
            csvwriter.writerows(self.launch_list)
            del self.launch_list[:]


class LogcatMonitor(object):
    '''logcat监控器
    '''

    def __init__(self, path=None, device_id=None, package=None, **regx_config):
        '''构造器

        :param str device_id: 设备id
        :param list package : 监控的进程列表，列表为空时，监控所有进程
        :param dict regx_config : 日志匹配配置项{conf_id = regx}，如：AutoMonitor=ur'AutoMonitor.*:(.*), cost=(\d+)'
        '''
        super(LogcatMonitor, self).__init__(**regx_config)
        self.package = package  # 监控的进程列表
        self.path = path
        self.device_id = device_id
        self.device = ADB(device_id)  # 设备
        self.running = False  # logcat监控器的启动状态(启动/结束)
        self.launchtime = LaunchTime(deviceid=self.device_id, packagename=self.package, path=self.path)
        self.exception_log_list = []
        self.start_time = None

        self.append_log_line_num = 0
        self.file_log_line_num = 0
        self.log_file_create_time = None
        self.logcat_collector = LogcatCollector(device=self.device, path=self.path)

    def start(self, start_time):
        '''启动logcat日志监控器
        '''
        self.start_time = start_time
        # 注册启动日志处理回调函数为handle_lauchtime
        self.add_log_handle(self.launchtime.handle_launchtime)
        logger.debug("=" * 10 + "启动logcat监控器" + "=" * 10)
        # 捕获所有进程日志
        # https://developer.android.com/studio/command-line/logcat #alternativeBuffers
        # 默认缓冲区 main system crash,输出全部缓冲区

        if not self.running:
            self.logcat_collector.start(process_list=[], params="-b all")
            time.sleep(1)
            self.running = True

    def stop(self):
        '''结束logcat日志监控器
        '''
        logger.debug("=" * 10 + "关闭logcat监控器" + "=" * 10)
        self.remove_log_handle(self.launchtime.handle_launchtime)  # 删除回调
        if self.exception_log_list:
            self.remove_log_handle(self.handle_exception)
        self.logcat_collector.stop()
        self.running = False

    def parse(self, file_path):
        pass

    def set_exception_list(self, exception_log_list):
        self.exception_log_list = exception_log_list

    def add_log_handle(self, handle):
        '''添加实时日志处理器，每产生一条日志，就调用一次handle
        '''
        self.logcat_collector._logcat_handle.append(handle)

    def remove_log_handle(self, handle):
        '''删除实时日志处理器
        '''
        self.logcat_collector._logcat_handle.remove(handle)

    def handle_exception(self, log_line):
        '''
        这个方法在每次有log时回调
        :param log_line:最近一条的log 内容
        异常日志写一个文件
        :return:void
        '''

        for tag in self.exception_log_list:
            if tag in log_line:
                logger.debug("exception Info: " + log_line)
                tmp_file = os.path.join(self.path, 'exception.log')
                with open(tmp_file, 'a+', encoding="utf-8") as f:
                    f.write(log_line + '\n')
                #     这个路径 空格会有影响
                # process_stack_log_file = os.path.join(self.path, 'process_stack_%s_%s.log' % (
                #     self.package, TimeUtils.getCurrentTimeUnderline()))
                # 如果进程挂了，pid会变 ，抓变后进程pid的堆栈没有意义
                # self.logmonitor.device.adb.get_process_stack(self.package,process_stack_log_file)
                # if RuntimeData.old_pid:
                #     self.device.adb.get_process_stack_from_pid(RuntimeData.old_pid, process_stack_log_file)


class LogcatTask:
    """为项目任务池准备"""

    def __init__(self, path, device=None):
        self.path = path
        self.device = device
        self.logcat_collector = LogcatCollector(device=self.device, path=self.path)

    def run(self):
        logger.debug("=" * 10 + "启动logcat监控器" + "=" * 10)
        try:  # 有些机型上会报permmison denied，但是logcat -c的代码仍会部分执行，所以加try 保护
            self.device.adb.run_shell_cmd('logcat -c -b all')  # 清除缓冲区
        except RuntimeError as e:
            logger.warning(e)
        self.device.adb.run_shell_cmd('logcat -v threadtime -b all', sync=False)
        self.logcat_collector.logcat_thread_func(save_dir=self.path, process_list=[], params="-b all")


if __name__ == "__main__":
    monitor = LogcatMonitor(path=settings.root_path / "uiauto" / "perf" / "record")
    monitor.start(timeoperator.strftime_now("%Y_%m_%d_%H_%M_%S"))
    time.sleep(20)
    monitor.stop()
