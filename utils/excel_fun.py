#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: excel_fun
@Created: 2023/2/20 9:48
"""
import shutil

import xlwings

from conf import settings
from utils.allure_fun import AllureDataCollect
from utils.path_fun import Path


class ErrorCaseExcel:
    """ 收集运行失败的用例，整理成excel报告 """

    def __init__(self, file_path):
        _excel_template = settings.root_path / "utils" / "abnormal_case.xlsx"
        shutil.copy(src=_excel_template, dst=file_path)
        self.case_file = Path(file_path) / "abnormal_case.xlsx"
        # 打开程序（只打开不新建)
        self.app = xlwings.App(visible=False, add_book=False)
        self.w_book = self.app.books.open(self.case_file, read_only=False)

        # 选取工作表：
        self.sheet = self.w_book.sheets['异常用例']  # 或通过索引选取
        self.case_data = AllureDataCollect(file_path)

    def background_color(self, position: str, rgb: tuple):
        """
        excel 单元格设置背景色
        @param rgb: rgb 颜色 rgb=(0，255，0)
        @param position: 位置，如 A1, B1...
        @return:
        """
        # 定位到单元格位置
        rng = self.sheet.range(position)
        excel_rgb = rng.color = rgb
        return excel_rgb

    def column_width(self, position: str, width: int):
        """
        设置列宽
        @return:
        """
        rng = self.sheet.range(position)
        # 列宽
        excel_column_width = rng.column_width = width
        return excel_column_width

    def row_height(self, position, height):
        """
        设置行高
        @param position:
        @param height:
        @return:
        """
        rng = self.sheet.range(position)
        excel_row_height = rng.row_height = height
        return excel_row_height

    def column_width_adaptation(self, position):
        """
        excel 所有列宽度自适应
        @return:
        """
        rng = self.sheet.range(position)
        auto_fit = rng.columns.autofit()
        return auto_fit

    def row_width_adaptation(self, position):
        """
        excel 设置所有行宽自适应
        @return:
        """
        rng = self.sheet.range(position)
        row_adaptation = rng.rows.autofit()
        return row_adaptation

    def write_excel_content(self, position: str, value: str):
        """
        excel 中写入内容
        @param value:
        @param position:
        @return:
        """
        self.sheet.range(position).value = value

    def write_case(self):
        """
        用例中写入失败用例数据
        @return:
        """

        _data = self.case_data.get_failed_case()
        # 判断有数据才进行写入
        if len(_data) > 0:
            num = 2
            for data in _data:
                self.write_excel_content(position="A" + str(num), value=str(self.case_data.get_uid(data)))
                self.write_excel_content(position='B' + str(num), value=str(self.case_data.get_case_name(data)))
                self.write_excel_content(position="C" + str(num), value=str(self.case_data.get_case_full_name(data)))
                self.write_excel_content(position="D" + str(num), value=str(self.case_data.get_case_start(data)))
                self.write_excel_content(position="E" + str(num), value=str(self.case_data.get_case_stop(data)))
                self.write_excel_content(position="F" + str(num), value=str(self.case_data.get_case_time(data)))
                self.write_excel_content(position="G" + str(num), value=str(self.case_data.get_case_status(data)))
                self.write_excel_content(position="H" + str(num), value=str(self.case_data.get_case_status_trace(data)))

                num += 1
        self.w_book.save()
        self.w_book.close()
        self.app.quit()


if __name__ == '__main__':
    path = settings.root_path / "report" / "2023-02-20-09-39-36"
    excel = ErrorCaseExcel(path).write_case()
