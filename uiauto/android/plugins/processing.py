#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: processing
@Created: 2023/2/25
"""
import time

from PIL import Image, ImageFont, ImageDraw

from conf import settings
from loguru import logger


def compress_image(infile):
    """
    不改变图片尺寸压缩到指定大小
    """
    im = Image.open(infile)
    im.save(infile, quality=5)


def screenshots_name(describe=None):
    """
    生成截图的名称
    """
    case_path = settings.report
    this_case_name = case_path.split("/")[-1]
    now_time = int(round(time.time() * 1000))
    tmp_file_name = this_case_name + "::" + str(now_time) + ".jpg"
    print("\n")
    describe = "" if not describe else " => " + describe
    logger.info("截图 📷" + describe + " => " + tmp_file_name)
    snapshot_dir = "" + "/"
    snapshot_name = "{path}{name}".format(path=snapshot_dir, name=tmp_file_name)
    return snapshot_name


def processing(image, w=None, h=None):
    """
    点击截图增加水印
    """
    font_size = 200
    font_dir = settings.root_path / "uiauto" / "android" / "Songti.tcc"
    font = ImageFont.truetype(font_dir, font_size)
    if w is not None and h is not None:
        im1 = Image.open(image)
        w = w - font_size / 2
        h = h - font_size / 2 - 40
        draw = ImageDraw.Draw(im1)
        draw.text((w, h), "⊙", (255, 0, 0, 255), font=font)  # 设置文字位置/内容/颜色/字体
        ImageDraw.Draw(im1)  # Just draw it!
        im1.save(image)

    compress_image(image)
