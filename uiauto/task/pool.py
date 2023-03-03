#!/usr/bin/env python
# -*- ecoding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: pool
@Created: 2023/3/3 9:54
"""
import queue
import threading
from concurrent.futures.thread import ThreadPoolExecutor

from uiauto.task.status import FINISHED


class TaskPool:
    """任务池"""

    def __init__(self):
        self.tasks = []
        self.executor = ThreadPoolExecutor(max_workers=10)
        self._running = False
        self.__event = threading.Event()
        self.__event.set()

    def submit_task(self, task):
        """
        提交任务
        :param task: 任务
        :return:
        """
        self.tasks.append(task)

    def remove_task(self, task):
        """
        删除任务
        :param task: 任务
        :return:
        """
        self.tasks.remove(task)

    def stop(self):
        """
        停止任务池线程
        :return:
        """
        self._running = False
        self.__event.set()

    def start(self):
        """开始任务池线程"""

        def _work():
            while self._running:
                for task in self.tasks:
                    self.executor.submit(task.run)
                # for task in self.tasks.qsize():
                #     task.future = future = self.executor.submit(task.run)
                #     setattr(future, 'task_id', task.id)

                # def callback(f):
                #     if not self.has_unfinished_tasks():
                #         self.stop()
                #
                # future.add_done_callback(callback)
                # future.result()
                # time.sleep(1)

        if not self._running:
            self._running = True
            t = threading.Thread(target=_work, daemon=True)
            t.start()


task_pool = TaskPool()
