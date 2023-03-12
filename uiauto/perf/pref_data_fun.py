#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: pref_data_fun
@Created: 2023/2/24 16:34
"""
import time

import allure
import pandas as pd
from matplotlib import pyplot as plt, gridspec

from loguru import logger
from utils.path_fun import Path


class PrefDataFun:
    def __init__(self):
        self.df = None

    def read_excel(self, path, **kwargs):
        df = pd.read_excel(path, **kwargs)
        self.df = df
        return df

    def read_csv(self, path, **kwargs):
        df = pd.read_csv(path, **kwargs)
        self.df = df
        return df

    def get_data(self, type="records"):
        data = {}
        try:
            data = self.df.to_dict(type)
        except Exception as e:
            logger.error(e)
        return data

    def save_png(self, path):
        new_path = path.replace("csv", "png")
        plt.savefig(new_path)
        # plt.show()
        return new_path

    def cpu_handle(self, path: Path):
        path = path / "cpuinfo.csv"
        df = self.read_csv(path)
        # 去除pid列为空的数据
        df = df.dropna(axis=0, how="any", subset=["pid"])
        df.drop(df[(df.datetime == "datetime")].index, inplace=True)
        df = pd.DataFrame(df, columns=['datetime', 'device_cpu_rate%', 'user%', 'system%', 'idle%', 'pid_cpu%'])
        for i in ['device_cpu_rate%', 'user%', 'system%', 'idle%', 'pid_cpu%']:
            df[i] = df[i].astype(float)
        df['datetime'] = pd.to_datetime(df['datetime'])
        return df

    def fps_handle(self, path: Path):
        path = path / "fps.csv"
        df = self.read_csv(path)
        df.drop(df[(df.datetime == "datetime")].index, inplace=True)
        df = pd.DataFrame(df, columns=['datetime', 'fps', 'jank'])
        for i in ['fps', 'jank']:
            df[i] = df[i].astype(float)
        df['datetime'] = pd.to_datetime(df['datetime'], format="%Y-%m-%d %H-%M-%S")
        return df

    def mem_handle(self, path: Path):
        path = path / "meminfo.csv"
        df = self.read_csv(path)
        df.drop(df[(df.datatime == "datatime")].index, inplace=True)
        df = df.dropna(axis=0, how="any", subset=["pid"])
        df = pd.DataFrame(df, columns=['datatime', 'total_ram(MB)', 'free_ram(MB)', 'pid_pss(MB)'])
        for i in ['total_ram(MB)', 'free_ram(MB)', 'pid_pss(MB)']:
            df[i] = df[i].astype(float)
        df['datatime'] = pd.to_datetime(df['datatime'], format="%Y-%m-%d %H-%M-%S")
        return df

    def power_handle(self, path: Path):
        path = path / "powerinfo.csv"
        df = self.read_csv(path)
        df.drop(df[(df.datetime == "datetime")].index, inplace=True)
        df = pd.DataFrame(df, columns=['datetime', 'voltage(V)', 'tempreture(C)', 'current(mA)'])
        for i in ['voltage(V)', 'tempreture(C)', 'current(mA)']:
            df[i] = df[i].astype(float)
        df['datetime'] = pd.to_datetime(df['datetime'], format="%Y-%m-%d %H-%M-%S")
        return df

    def pss_handle(self, path: Path):
        path = path / "pss.csv"
        df = self.read_csv(path)
        df.drop(df[(df.datatime == "datatime")].index, inplace=True)
        df = pd.DataFrame(df, columns=['datatime', 'pss', 'java_heap', 'native_heap', 'system'])
        for i in ['pss', 'java_heap', 'native_heap', 'system']:
            df[i] = df[i].astype(float)
        df['datatime'] = pd.to_datetime(df['datatime'], format="%Y-%m-%d %H-%M-%S")
        return df

    def thread_num_handle(self, path: Path):
        path = path / "thread_num.csv"
        df = self.read_csv(path)
        df = df.dropna(axis=0, how="any", subset=["pid"])
        df.drop(df[(df.datatime == "datatime")].index, inplace=True)
        df = pd.DataFrame(df, columns=['datatime', 'thread_num'])
        for i in ['thread_num']:
            df[i] = df[i].astype(float)
        df['datatime'] = pd.to_datetime(df['datatime'], format="%Y-%m-%d %H-%M-%S")
        return df

    def traffic_handle(self, path: Path):
        path = path / "traffic.csv"
        df = self.read_csv(path)
        df.drop(df[(df.datetime == "datetime")].index, inplace=True)
        df = pd.DataFrame(df, columns=['datetime',
                                       'device_total(KB)', 'device_receive(KB)',
                                       'device_transport(KB)',
                                       'pid_rx(KB)', 'pid_tx(KB)', 'pid_total(KB)'])
        for i in ['device_total(KB)', 'device_receive(KB)',
                  'device_transport(KB)',
                  'pid_rx(KB)', 'pid_tx(KB)', 'pid_total(KB)']:
            df[i] = df[i].astype(float)
        df['datetime'] = pd.to_datetime(df['datetime'], format="%Y-%m-%d %H-%M-%S")
        return df

    def all_handle(self, path: Path):
        new_path = path / "perf_statistics.png"
        df1 = self.cpu_handle(path)
        df2 = self.fps_handle(path)
        df3 = self.mem_handle(path)
        # df4 = self.power_handle(path)
        df5 = self.pss_handle(path)
        df6 = self.thread_num_handle(path)
        # df7 = self.traffic_handle(path)
        plt.figure(1, figsize=(19, 16))
        plt.text(3, 12, 'I', fontsize=20)
        gs = gridspec.GridSpec(5, 3)
        ax1 = plt.subplot(gs[0, :])
        ax2 = plt.subplot(gs[1, 0])
        ax3 = plt.subplot(gs[1, 1])
        # ax4 = plt.subplot(gs[1, 2])
        ax5 = plt.subplot(gs[2, :])
        ax6 = plt.subplot(gs[3, :])
        # ax7 = plt.subplot(gs[4, :])
        ax1.axes.xaxis.set_ticklabels([])
        ax2.axes.xaxis.set_ticklabels([])
        ax3.axes.xaxis.set_ticklabels([])
        # ax4.axes.xaxis.set_ticklabels([])
        ax5.axes.xaxis.set_ticklabels([])
        ax6.axes.xaxis.set_ticklabels([])
        df1.plot(x="datetime", kind="line", title="CPU", ax=ax1, xlabel="")
        df2.plot(x="datetime", kind="line", title="FPS", ax=ax2, xlabel="")
        df3.plot(x="datatime", kind="line", title="MEM", ax=ax3, xlabel="")
        # df4.plot(x="datetime", kind="line", title="Power", ax=ax4, xlabel="")
        df5.plot(x="datatime", kind="line", title="PSS", ax=ax5, xlabel="")
        df6.plot(x="datatime", kind="line", title="Thread Num", ax=ax6, xlabel="")
        # df7.plot(x="datetime", kind="line", title="Traffic", ax=ax7)
        # plt.show()
        plt.savefig(new_path)
        # time.sleep(10)
        file_png = open(new_path, mode='rb').read()
        allure.attach(file_png, 'pref_png', allure.attachment_type.PNG)
        return f"[性能数据]({new_path})\n"
