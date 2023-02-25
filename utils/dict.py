#!/usr/bin/env python
# -*- ecoding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: dict
@Created: 2023/2/25
"""
import inspect
import re
from datetime import datetime


def to_dict(o, fields=None, exclude_fields=None):
    """
    将对象转换为字典
    :param o: 对象
    :param fields: 包含的字段
    :param exclude_fields: 排除字段
    :return:
    """
    if isinstance(o, (int, float, str)):
        return o
    elif isinstance(o, dict):
        _dict = {}
        for k, v in o.items():
            if k.startswith('_') or (fields and k not in fields) or (exclude_fields and k in exclude_fields):
                continue
            elif inspect.isfunction(v):
                continue
            if not getattr(v, '__converted__', False):
                _dict[k] = to_dict(v)
        return _dict
    elif isinstance(o, (list, tuple, set)):
        return [to_dict(item) for item in o]
    elif isinstance(o, datetime):
        return o.strftime('%Y-%m-%d %H:%M:%S')
    elif hasattr(o, '__dict__'):
        setattr(o, '__converted__', True)
        return to_dict(o.__dict__, fields=fields, exclude_fields=exclude_fields)
    else:
        return str(o)


class Dict(dict):
    def __setattr__(self, key, value):
        self[key] = value

    def __getattr__(self, item):
        return self.get(item)

    # @staticmethod
    # def load_xml(file):
    #     tree = etree.parse(file)
    #     root = tree.getroot()
    #     result = Dict(**root.attrib)
    #
    #     def convert_ele(ele, d):
    #         for sub in ele:
    #             tag = sub.tag.lower()
    #             count = len(ele.xpath(f'//{sub.tag}'))
    #             sd = Dict(**sub.attrib)
    #             _list = []
    #             if count > 1:
    #                 _list.append(sd)
    #                 setattr(d, tag + '_list', sd)
    #             else:
    #                 setattr(d, tag, sd)
    #             convert_ele(sub, sd)
    #
    #     convert_ele(root, result)
    #     return result

    def to_query_str(self):
        """
        将字典转换为查询字符串

        :return:
        """
        return '&'.join([k + '=' + str(v) for k, v in self.items()])

    @staticmethod
    def from_query_str(query_str):
        query_str = query_str + '&'
        p = re.compile(r'[^=&]+=[^=]+(?=&)')
        _list = p.findall(query_str)
        d = Dict()
        for item in _list:
            _arr = item.split('=', maxsplit=1)
            d[_arr[0]] = _arr[1]
        return d
