#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: yaml_fun
@Created: 2023/2/17 17:19
"""
import os
from ruamel.yaml import YAML
import yaml.scanner

from utils import ensure_path_sep


class GetYamlData:
    """ 获取 yaml 文件中的数据 """

    def __init__(self, file_dir):
        self.file_dir = str(file_dir)

    def get_yaml_data(self) -> dict:
        """
        获取 yaml 中的数据
        :param: fileDir:
        :return:
        """
        # 判断文件是否存在
        if os.path.exists(self.file_dir):
            data = open(self.file_dir, 'r', encoding='utf-8')
            res = yaml.load(data, Loader=yaml.FullLoader)
        else:
            raise FileNotFoundError("文件路径不存在")
        return res

    def write_yaml_data(self, key: str, value):
        """
        更改 yaml 文件中的值，并保留注释内容
        :param key: 字典的键
        :param value: 写入的值
        :return:
        """
        yaml = YAML()
        with open(self.file_dir, 'r', encoding='utf-8') as file:
            data = yaml.load(file)

        if key in data:
            # 如果 key 对应的值是一个列表，可以直接对列表进行增删操作
            if isinstance(data[key], list):
                for item in value:
                    if item not in data[key]:
                        data[key].append(item)
                for item in data[key]:
                    if item not in value:
                        data[key].remove(item)
            else:
                data[key] = value

        with open(self.file_dir, 'w', encoding='utf-8') as file:
            yaml.dump(data, file)


if __name__ == '__main__':
    value = [
        "--reruns=3",  # 失败重测次数改为3
        "--reruns-delay=5",  # 失败重测间隔改为5秒
        "--count=2",  # 循环次数改为2
        "--random-order",  # 随机执行
        r"D:\pyauto\repos\lxl\test_xxx.py"  # 脚本选择 注释执行repos目录下所有用例
    ]
    _data = GetYamlData(ensure_path_sep("\\conf\\test.yaml")).write_yaml_data("pytest", value)
    # pytest_condition = _data.get("pytest")
    # new_data = pytest_condition.append("")
    f = _data
