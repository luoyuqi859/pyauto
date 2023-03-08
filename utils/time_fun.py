#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: time_fun.py
@Created: 2023/2/22 16:40
"""
import random
import time
import datetime
import calendar


class TimeOperator:
    @property
    def now(self):
        """
        返回当前时间戳
        :return:
        """
        return time.time()

    @property
    def now1(self):
        """
        以 年-月-日 时:分:秒 格式返回当前时间
        :return:
        """
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    @property
    def now2(self):
        """
        以 年-月-日 格式返回当前时间
        :return:
        """
        return time.strftime("%Y-%m-%d", time.localtime())

    @property
    def now3(self):
        """
        以 年月日时分秒 格式返回当前时间
        :return:
        """
        return time.strftime("%Y%m%d%H%M%S", time.localtime())

    @property
    def now4(self):
        """
        13位时间戳
        :return:
        """
        return int(time.time() * 1000)

    def strftime_now(self, strf, d=None):
        """
        以 指定格式 格式返回当前时间
        :return:
        """
        if d:
            return time.strftime(strf, time.localtime(d))
        else:
            return time.strftime(strf, time.localtime())

    def s_to_hms(self, s):
        """秒转时分秒格式"""
        return time.strftime("%H:%M:%S", time.gmtime(s))

    @property
    def now_month(self):
        """
        以 年-月 格式返回当前时间
        :return:
        """
        return time.strftime("%Y-%m", time.localtime())

    def other_month(self, add_num=0):
        """
        当前月份的n个月后的 年-月
        """
        y_m = self.now_month
        y, m = [int(i) for i in y_m.split("-")]
        m += add_num
        if m > 12:
            m -= 12
            y += 1
        return f'{y}-{m:02d}'

    def other_day(self, day):
        """
        以 年-月-日 时:分:秒 格式返回当前时间+偏移时间
        :return:
        """
        return str(datetime.datetime.today() + datetime.timedelta(days=day)).split(".")[0]

    def other_day_num(self, day):
        """
        以时间戳格式返回 当前时间+偏移时间
        @param day:
        @return:
        """
        return int(time.time() * 1000) + 24 * 3600 * day

    def get_age(self, birthday):
        """

        :param birthday: 年-月-日
        :return:
        """
        y, m, d = [int(i) for i in birthday.split('-')]
        birthday = datetime.date(y, m, d)
        today = datetime.date.today()
        return today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))

    def get_year_month(self, year=0, month=0):
        now = datetime.datetime.now()
        if year == 0:
            year = now.year
        if month == 0:
            month = now.month
        return year, month

    def get_month_day(self, year=0, month=0):
        """
        获取指定月份第一天和最后一天
        """
        year, month = self.get_year_month(year, month)
        month_first_day, month_last_day = calendar.monthrange(year, month)
        return month_first_day, month_last_day

    def get_random_day(self, year=0, month=0):
        """
        获取指定年月的随机的一天
        """
        year, month = self.get_year_month(year, month)
        month_first_day, month_last_day = self.get_month_day(year, month)
        day = random.randint(month_first_day, month_last_day)
        return f'{year}-{month}-{day:02d}'

    def get_random_time(self):
        """
        获取随机 时:分:秒
        """
        h = random.randint(0, 23)
        m = random.randint(0, 59)
        s = random.randint(0, 59)
        return f'{h:02d}:{m:02d}:{s:02d}'

    def get_other_m_d(self, n=0, t=None):
        """
        获取n个月后的年月日范围
        """
        if t:
            y, m = t.split("-")
        else:
            y, m, _ = self.now2.split("-")
        y = int(y)
        m = int(m) + n
        d1, d2 = self.get_month_day(int(y), m)
        return f'{y:04d}-{m:02d}-{1:02d}', f'{y:04d}-{m:02d}-{d2:02d}'

    def get_localtime(self, time_stamp, time_format='%Y-%m-%d %H:%M:%S'):
        """
        时间戳转化
        @param time_stamp:
        @return:
        """
        if len(str(time_stamp)) == 13:
            time_stamp = time_stamp / 1000
        time_array = time.localtime(time_stamp)
        return time.strftime(time_format, time_array)

    def get_time_stamp(self, time_str, format):
        """
        将指定格式时间转化成时间戳
        @param time_str:
        @param format:
        @return:
        """
        return time.mktime(time.strptime(time_str, format))


timeoperator = TimeOperator()


class TimeManager():
    """时间转换工具"""

    @staticmethod
    def timestamp_to_str(timestamp, fmt="%Y-%m-%d %H:%M:%S"):
        """13位转字符串"""
        if isinstance(timestamp, int) or isinstance(timestamp, float):
            if len(str(int(timestamp))) >= 12:
                timestamp = float(timestamp / 1000)
            fmt_time = time.strftime(fmt, time.localtime(timestamp))
            return fmt_time
        else:
            return TimeManager.now(is_str=True)

    @staticmethod
    def str_to_timestamp(time_str, digit=13):
        """转时间戳,默认13位"""
        timestamp = (
            int(time.mktime(time.strptime(time_str, "%Y-%m-%d %H:%M:%S"))) * 1000
            if digit == 13
            else int(time.mktime(time.strptime(time_str, "%Y-%m-%d %H:%M:%S")))
        )
        return timestamp

    @staticmethod
    def convert_str(time_str, fmt_from="%Y-%m-%d %H:%M:%S", fmt_to="%Y-%m-%d %H_%M_%S"):
        """时间字符串的格式转换"""
        return datetime.datetime.strptime(time_str, fmt_from).strftime(fmt_to)

    @staticmethod
    def now(is_str=False, digit=13, format="%Y-%m-%d %H:%M:%S"):
        """获取当前的时间"""
        now_time = datetime.datetime.now()
        time_str = now_time.strftime(format)
        timestamp = (
            int(round(time.mktime(now_time.timetuple()) * 1000))
            if digit == 13
            else int(round(time.mktime(now_time.timetuple())))
        )
        return time_str if is_str else timestamp

    @staticmethod
    def last_24_hour(is_str=False, digit=13, days=1, now=None):
        """获取过去n天"""
        if now is None:
            now = datetime.datetime.now()
        if isinstance(now, str):
            now = datetime.datetime.strptime(now, "%Y-%m-%d %H:%M:%S")
        if isinstance(now, int):
            now = (
                time.strftime("%Y-%m-%d %H:%M:%S",
                              time.localtime(float(now / 1000)))
                if len(str(now)) == 13
                else time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now))
            )
            now = datetime.datetime.strptime(now, "%Y-%m-%d %H:%M:%S")
        yesterday = now - datetime.timedelta(days=days)
        time_str = yesterday.strftime("%Y-%m-%d %H:%M:%S")
        timestamp = (
            int(time.mktime(yesterday.timetuple()) * 1000)
            if digit == 13
            else int(time.mktime(yesterday.timetuple()))
        )
        return time_str if is_str else timestamp

    @staticmethod
    def past_time(unit, num, is_str=False, now_time=None):
        if now_time is None:
            now_time = datetime.datetime.now()
        if unit == "seconds":
            past_time = now_time - datetime.timedelta(seconds=num)
        elif unit == "days":
            past_time = now_time - datetime.timedelta(days=num)
        elif unit == "minutes":
            past_time = now_time - datetime.timedelta(minutes=num)
        elif unit == "hours":
            past_time = now_time - datetime.timedelta(hours=num)
        else:
            raise NotImplementedError
        time_str = past_time.strftime("%Y-%m-%d %H:%M:%S")
        timestamp = int(round(time.mktime(past_time.timetuple()) * 1000))
        return time_str if is_str else timestamp

    @staticmethod
    def get_current_timestamp():
        return int(round(time.time() * 1000))

    @staticmethod
    def timestamp_to_datetime(timestamp):
        return datetime.datetime.fromtimestamp(timestamp / 1000)

    @staticmethod
    def split_time(time_str):
        year = month = day = hour = minute = second = 0
        if "-" in time_str:
            year, month, day = time_str.split(" ")[0].split("-")
            hour, minute, second = time_str.split(" ")[1].split(":")
        else:
            if time_str.count(":") == 2:
                hour, minute, second = time_str.split(":")
            else:
                hour, minute = time_str.split(":")
        return int(year), int(month), int(day), int(hour), int(minute), int(second)

    @staticmethod
    def month_first_day(next_month=False):
        now_date = datetime.date.today()
        first_day = datetime.date(now_date.year, now_date.month, 1)
        if next_month:
            days_num = calendar.monthrange(first_day.year, first_day.month)[1]
            return first_day + datetime.timedelta(days=days_num)
        else:
            return first_day

    @staticmethod
    def month_last_day(next_month=False):
        month_first_day = TimeManager.month_first_day(next_month)
        month_days = calendar.monthrange(
            month_first_day.year, month_first_day.month)[1]
        month_last_day = month_first_day + \
                         datetime.timedelta(days=month_days - 1)
        return month_last_day

    @staticmethod
    def utcstr_to_str(utcstr, format="%Y-%m-%dT%H:%M:%S.%f+0800"):
        """
            处理utc类型的时间字符串
        :param utcstr: utc时间字符串
        :param format: utc格式
        :return:
        """
        utc_time = datetime.datetime.strptime(utcstr, format)
        local_str = utc_time.strftime("%Y-%m-%d %H:%M:%S")
        return local_str

    @staticmethod
    def datetime_plus_datetime(time_obj, day):
        datetime_obj = (time_obj + datetime.timedelta(days=day))
        return datetime_obj

    @staticmethod
    def datetime_forward_between(days=None, now=None, fmt=None, order=0):
        if fmt is None:
            _format = '%Y-%m-%d'

        _times = list()
        if order == 1:  # 正序
            i = days - 1
            while i >= 0:
                _times.append(TimeManager.datetime_forward(days=i, fmt=fmt))
                i = i - 1
        else:  # 倒序
            i = 0
            while i < days:
                _times.append(TimeManager.datetime_forward(days=i, fmt=fmt))
                i = i + 1

        return _times

    @staticmethod
    def datetime_forward(days=None, now=None, fmt=None):
        if now is None:
            now = datetime.datetime.now()

        delta = datetime.timedelta(days=days)
        n_days_forward = now - delta

        if fmt:
            ret_time = n_days_forward.strftime(fmt)
            # print("向前推{}天的日期：{}".format(days, ret_time))
            return ret_time
        else:
            return int(round(time.mktime(n_days_forward.timetuple()) * 1000))

    @staticmethod
    def datetime_after(days=None, now=None, fmt=None):
        if now is None:
            now = datetime.datetime.now()

        delta = datetime.timedelta(days=days)
        n_days_forward = now + delta

        if fmt:
            ret_time = n_days_forward.strftime(fmt)
            # print("向后推{}天的日期：{}".format(days, ret_time))
            return ret_time
        else:
            return int(round(time.mktime(n_days_forward.timetuple()) * 1000))


if __name__ == '__main__':
    print()
