#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: __init__.py
@Created: 2023/2/16 16:58
"""
from utils.model import Config
from utils.path_fun import root_path, ensure_path_sep
from utils.yaml_fun import GetYamlData

_data = GetYamlData(ensure_path_sep("\\conf\\config.yaml")).get_yaml_data()
config = Config(**_data)
pass
