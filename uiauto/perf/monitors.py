#!/usr/bin/env python
# -*- ecoding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: monitors
@Created: 2023/3/3 11:33
"""
import queue

from conf import settings
from uiauto.perf.cpu import CpuMonitor
from uiauto.perf.fps import FPSMonitor
from uiauto.perf.logcat import LogcatMonitor
from uiauto.perf.memory import MemMonitor
from uiauto.perf.thread_num import ThreadNumMonitor
from utils import config
from utils.log import logger


class Monitors:

    def __init__(self):
        self.monitors = []
        self._init_queue()

    def _init_queue(self):
        self.cpu_queue = queue.Queue()
        self.mem_queue = queue.Queue()
        # self.power_queue = queue.Queue()
        # self.traffic_queue = queue.Queue()
        self.fps_queue = queue.Queue()
        self.thread_queue = queue.Queue()
        self.logcat_queue = queue.Queue()

    def add_monitor(self, monitor):
        self.monitors.append(monitor)

    def remove_monitor(self, monitor):
        self.monitors.remove(monitor)

    def run(self):
        settings.perf_path.mkdir()
        app = config.perf.package
        frequency = config.perf.frequency
        t = settings.current_time
        self.add_monitor(CpuMonitor(packages=[app], interval=frequency, path=settings.perf_path))
        self.add_monitor(FPSMonitor(package_name=app, frequency=frequency, path=settings.perf_path))
        self.add_monitor(MemMonitor(packages=[app], interval=frequency, path=settings.perf_path))
        self.add_monitor(ThreadNumMonitor(packagename=app, interval=frequency, path=settings.perf_path))
        if len(self.monitors):
            for monitor in self.monitors:
                # 启动所有的monitors
                try:
                    monitor.start(t)
                except Exception as e:
                    logger.error(e)

            # logcat的代码可能会引起死锁，拎出来单独处理logcat
            try:
                self.logcat_monitor = LogcatMonitor(path=settings.perf_path)
                self.logcat_monitor.start(t)
            except Exception as e:
                logger.error(e)

    def stop(self):
        for monitor in self.monitors:
            try:
                monitor.stop()
            except Exception as e:  # 捕获所有的异常，防止其中一个monitor的stop操作发生异常退出时，影响其他的monitor的stop操作
                logger.error(e)

        try:
            if self.logcat_monitor:
                self.logcat_monitor.stop()
        except Exception as e:
            logger.error("stop exception for logcat monitor")
            logger.error(e)


monitors = Monitors()
