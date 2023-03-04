#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: yaml_fun
@Created: 2023/2/17 17:19
"""
import os

import yaml.scanner


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

    def write_yaml_data(self, key: str, value) -> int:
        """
        更改 yaml 文件中的值, 并且保留注释内容
        :param key: 字典的key
        :param value: 写入的值
        :return:
        """
        with open(self.file_dir, 'r', encoding='utf-8') as file:
            # 创建了一个空列表，里面没有元素
            lines = []
            for line in file.readlines():
                if line != '\n':
                    lines.append(line)
            file.close()

        with open(self.file_dir, 'w', encoding='utf-8') as file:
            flag = 0
            for line in lines:
                left_str = line.split(":")[0]
                if key == left_str and '#' not in line:
                    newline = f"{left_str}: {value}"
                    line = newline
                    file.write(f'{line}\n')
                    flag = 1
                else:
                    file.write(f'{line}')
            file.close()
            return flag


if __name__ == '__main__':
    f = GetYamlData("E:\py-runner\pyAuto\conf\config.yaml").get_yaml_data()
    print(f)
