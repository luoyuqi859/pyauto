#!/usr/bin/env python
# -*- ecoding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: conftest
@Created: 2023/2/23 19:55
"""
import allure
import pytest

from repos.GM.TeenDriver import element
from repos.GM.keywords.gm_vehicle_sim import GMS
from uiauto.android.device import AndroidDevice


@pytest.fixture(scope="function", params=None, autouse=True, ids=None, name=None)
def teen_driver_start(d_obj: AndroidDevice):
    with allure.step('重置GMVehicleSimulator已发送命令'):
        GMS.sendSignal(Signal='TnDrvPINStrd', Value=0, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='TeenDrvRsp', Value=0, Type='Signal', Mode='HS')
    with allure.step('设置挡位到PARK并设置速度为0.0'):
        GMS.sendSignal(Signal='TEGP_TrnsShftLvrPstnAuth', Value=1, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='TEGP_TrnsShftLvrPstnAuth_Inv', Value=0, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='VMMP_VehMtnMvmtStatAuth', Value=0, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='VSADP_VehSpdAvgDrvnAuth', Value=0.0, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='VSADP_VehSpdAvgDrvnAuth_Inv', Value=0, Type='Signal', Mode='HS')
    with allure.step('开启TeenDriver'):
        d_obj.press("home")
        GMS.sendSignal(Signal='TeenDrvFtrAvl', Value=1, Type='Signal', Mode='HS')
    yield
    with allure.step('关掉TeenDriver'):
        d_obj.press("home")
        GMS.sendSignal(Signal='TeenDrvFtrAvl', Value=0, Type='Signal', Mode='HS')


@pytest.fixture(scope="function", params=None, autouse=False, ids=None, name=None)
def pin_code_save(d_obj: AndroidDevice):
    d_obj.click(text="Settings").click(text="Vehicle").click(text="Teen Driver")
    d_obj.click(text="Continue")
    d_obj.click(text="1").click(text="2").click(text="3").click(text="4")
    d_obj.click(resourceId=element.enter)
    GMS.sendSignal(Signal='TeenDrvRsp', Value=2, Type='Signal', Mode='HS')
    d_obj.click(text="1").click(text="2").click(text="3").click(text="4")
    d_obj.click(resourceId=element.enter)
    d_obj.click(xpath=element.ok)
    d_obj.press("home")
