#! /usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: file_fun
@Created: 2023/2/22 16:25
"""
import os

from utils.log import logger


class FileOperator:

    @staticmethod
    def get_file_size(file_path):
        """
        获取文件的大小,结果保留4位小数，单位为MB
        :param file_path:
        :return:
        """
        fsize = os.path.getsize(file_path)
        fsize = fsize / float(1024 * 1024)
        return round(fsize, 4)

    @staticmethod
    def rename_folder(old_folder_path, new_folder_path):
        """
        重命名文件夹
        @param old_folder_path: 旧文件夹路径
        @param new_folder_path: 新文件夹路径
        @return:
        """
        try:
            os.rename(old_folder_path, new_folder_path)
        except Exception:
            logger.error(f"重命名文件夹{old_folder_path}失败")
