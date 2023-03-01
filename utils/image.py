#!/usr/bin/env python
# -*- ecoding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: image
@Created: 2023/2/27 10:30
"""
import base64
import math
from io import BytesIO
from os import path

import numpy
from PIL import Image, ImageChops
from skimage.metrics import structural_similarity as compare_similarity


def pillow2base64(pillow_image):
    output_buffer = BytesIO()
    pillow_image.save(output_buffer, format='png')
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data).decode()
    return base64_str


def pillow2raw(image):
    output_buffer = BytesIO()
    image.save(output_buffer, format='png')
    byte_data = output_buffer.getvalue()
    return byte_data


def save_diff(src, target, filename=None):
    """

    :param src:
    :param target:
    :param filename:
    :return:
    """
    src_image, target_image = src, target
    if isinstance(src, str):
        src_image = Image.open(src)
    if isinstance(target, str):
        target_image = Image.open(target)
    try:
        diff = ImageChops.difference(src_image, target_image)

        if diff.getbbox() and filename:
            if not path.isabs(filename):
                filename = path.join(path.curdir, filename)
            diff.save(filename)
        else:
            return diff
    except ValueError as e:
        '''
        表示图片大小和box对应的宽度不一致，参考API说明：Pastes another image into this image
        The box argument is either a 2-tuple giving the upper left corner, a 4-tuple defining the left, upper,
        right, and lower pixel coordinate, or None (same as (0, 0)). If a 4-tuple is given, the size of the pasted 
        image must match the size of the region.使用2纬的box避免上述问题
        '''
        print(str(e))


def calc_similarity(src, target):
    if isinstance(src, str):
        src = Image.open(src)
    if isinstance(target, str):
        target = Image.open(target)
    src_w, src_h = src.size
    target_w, target_h = target.size
    if src_h != target_h or src_w != target_w:
        w, h = min(src_w, target_w), min(src_h, target_h)

        def resize(img, img_h, img_w):
            _h = abs(img_h - h) / 2
            _w = abs(img_w - w) / 2
            return img.crop((math.floor(_w), math.floor(_h), img_w - math.ceil(_w), img_h - math.ceil(_h)))

        src = resize(src, src_h, src_w)
        target = resize(target, target_h, target_w)
    try:
        src_gray, target_gray = src.convert('L'), target.convert('L')  # 灰度转换
        src_ndarray = numpy.asarray(src_gray)  # 转换为ndarray数据
        target_ndarray = numpy.asarray(target_gray)
        return compare_similarity(src_ndarray, target_ndarray)
    except Exception:
        return 0
