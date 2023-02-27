#!/usr/bin/env python
# -*- ecoding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: screenshot
@Created: 2023/2/27 10:37
"""
import os

from uiauto.android.plugins.rotation import Rotation
from utils import image
from utils.errors import TestFailedError
from utils.image import pillow2base64
from utils.log import logger
from PIL import ImageFont, ImageDraw
from PIL import Image


class ScreenshotBase:
    def __init__(self, device):
        self.device = device

    @property
    def pillow(self):
        raise NotImplementedError

    @property
    def byte64(self):
        raise NotImplementedError

    def compare(self, expected_image):
        return image.calc_similarity(self.pillow, expected_image)

    def assert_similarity(self, expected_image, similarity=0.8):
        logger.info(f'Found expected image: {expected_image}')
        target = Image.open(expected_image)
        actual = image.calc_similarity(self.pillow, expected_image)
        expected_image_name = os.path.basename(expected_image)
        if actual < similarity:
            data = {
                f'{self.device.name}-screenshot-actual': self.pillow,
                f'{self.device.name}-screenshot-expected': target
            }
            msg = f'[assert_screenshot]({expected_image}, similarity={similarity}), ' \
                  f'actual_similarity: {actual}'
            raise TestFailedError(msg, **data)
        logger.success(f'[{self.device.serial} ({self.device.name})] '
                       f'Assert screenshot with {expected_image_name}, '
                       f'expected similarity is {similarity}, '
                       f'actual similarity is {actual}.')

    def save_grid(self, filename='grid_screenshot.png', colors=None):
        """
        截图并在图上绘制网格标注相对坐标，用于快速估算出元素之间的偏移量

        :param filename: 默认在当前路径保存为 grid_screenshot.png
        :param colors: 绘线时所用的颜色，默认['red', 'blue']
        :return:
        """
        if colors is None:
            colors = ['red', 'blue']
        img = self.pillow
        draw = ImageDraw.Draw(img)
        w, h = self.device.window_size
        cw, ch = max(w, h) / 20, min(w, h) / 10
        font = ImageFont.truetype(size=40, font=r'c:\windows\fonts\msyh.ttc')
        if self.device.rotation.status in [Rotation.left, Rotation.right]:
            for i in range(1, 21):
                color = colors[i % 2]
                # cv2.line(self._image, (400, 380), (200, 150), (25, 100, 255))
                draw.line(xy=(cw * i, 0, cw * i, h), fill=color, width=1)
                draw.text(xy=(cw * i, ch), text=str(i / 20), fill=color, font=font)
            for j in range(1, 11):
                color = colors[j % 2]
                draw.line(xy=(0, ch * j, w, ch * j), fill=color, width=1)
                draw.text(xy=(cw * 2, ch * j), text=str(j / 10), fill=color, font=font)
        else:
            for i in range(1, 11):
                color = colors[i % 2]
                draw.line(xy=(ch * i, 0, ch * i, h), fill=color, width=1)

                draw.text(xy=(ch * i, cw * 2), text=str(i / 10), fill=color, font=font)
            for j in range(1, 21):
                color = colors[j % 2]
                draw.line(xy=(0, cw * j, w, cw * j), fill=color, width=1)
                draw.text(xy=(ch, cw * j), text=str(j / 20), fill=color, font=font)
        if not os.path.isabs(filename):
            filename = os.path.join(os.getcwd(), filename)
        img.save(filename)

    def __call__(self, fmt='pillow'):
        if fmt == 'pillow':
            return self.pillow
        elif fmt == 'base64':
            return self.byte64
        elif fmt == 'raw':
            return self.pillow.tobytes()
        else:
            raise RuntimeError("Invalid format " + fmt)


class UiaScreenshot(ScreenshotBase):

    def __call__(self, fmt='pillow'):
        if fmt == 'pillow':
            return self.pillow
        elif fmt == 'opencv':
            return self.opecv
        elif fmt == 'base64':
            return self.byte64
        elif fmt == 'raw':
            return self.pillow.tobytes()
        else:
            raise RuntimeError("Invalid format " + fmt)

    @property
    def pillow(self):
        return self.device.d.screenshot()

    @property
    def byte64(self):
        return pillow2base64(self.pillow)

    @property
    def opecv(self):
        import cv2
        import numpy as np
        r = self.device.uia.request("get", '/screenshot/0')
        nparr = np.fromstring(r.content, np.uint8)
        return cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    def save(self, filename):
        """
        保存图片
        :param filename: 文件名
        :return:
        """
        self.pillow.save(filename)

    def cut(self, left, top, right, bottom):
        """
        裁剪区域
        :param left:
        :param top:
        :param right:
        :param bottom:
        :return:
        """
        _image = self.pillow.crop((left, top, right, bottom))
        return _image
