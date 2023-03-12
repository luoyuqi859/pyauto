#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: command
@Created: 2023/3/11
"""
import subprocess

from loguru import logger


def execute_command(cmd, timeout=None):
    """
    Execute local commands
    :param cmd: Full command text
    :param timeout: Execution timeout
    :return: None
    """
    logger.debug("cmd in: %s" % cmd)
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, stderr=subprocess.PIPE)
    try:
        outs, errs = proc.communicate(timeout=timeout)
        status = proc.wait()
        logger.debug("cmd out: %s cmd status: %s" % (outs.decode(), status))
    except subprocess.TimeoutExpired as tex:
        logger.debug("TimeoutExpired: %s" % tex)
        proc.kill()
        outs, errs = proc.communicate()
        logger.debug("cmd out: %s" % outs.decode())
    except Exception as ex:
        logger.debug("Exception: %s" % ex)
