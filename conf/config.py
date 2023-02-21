#!/usr/bin/env python
# -*- ecoding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: config
@Created: 2023/2/20 10:58
"""
from datetime import datetime

from utils.path_fun import Path

root_path = Path(__file__).parent.parent
allure_bat = root_path / 'libs' / 'allure' / "bin" / "allure"
current_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
