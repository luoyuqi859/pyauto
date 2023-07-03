#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: ocr
@Created: 2023/3/1 9:55
"""

import ddddocr


class Ocr:
    def __init__(self, device=None):
        self.device = device
        self.ocr = ddddocr.DdddOcr()

    def magic_ocr(self, img_path):
        with open(img_path, "rb") as f:
            image_bytes = f.read()
        return self.ocr.classification(image_bytes)


if __name__ == '__main__':
    ocr = Ocr()
