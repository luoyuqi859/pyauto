#!/usr/bin/env python
# -*- ecoding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: ocr
@Created: 2023/3/1 9:55
"""

from paddleocr import PaddleOCR

from conf import settings


class Ocr:
    def __init__(self, device=None):
        self.device = device
        self.ocr = PaddleOCR(use_angle_cls=True, lang="ch", det_model_dir=settings.ocr_det,
                             rec_model_dir=settings.ocr_rec,
                             cls_model_dir=settings.ocr_cls)

    def image_to_text(self, img_path):
        result = self.ocr.ocr(img_path, cls=True)
        text = []
        for line in result:
            text.append(line[0][-1][0])
        return text
