#! /usr/bin/env python
# -*- coding: utf-8 -*-
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
    while not d_obj(text="Settings").exists:
        d_obj.press("home")
    with allure.step('重置GMVehicleSimulator已发送命令'):
        GMS.sendSignal(Signal='TnDrvPINStrd', Value=0, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='TeenDrvReq', Value=0, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='TeenDrvRsp', Value=0, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='TDAP_TeenDrvrActvAuth', Value=0, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='TDOSWCCSV_CrSetVal', Value=1, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='ORIP_DrvrStBltStsAuth', Value=0, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='FrntPsSeatbeltStat', Value=0, Type='Signal', Mode='HS')
    with allure.step('设置挡位到PARK并设置速度为0.0'):
        GMS.sendSignal(Signal='TEGP_TrnsShftLvrPstnAuth', Value=1, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='TEGP_TrnsShftLvrPstnAuth_Inv', Value=0, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='VMMP_VehMtnMvmtStatAuth', Value=0, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='VSADP_VehSpdAvgDrvnAuth', Value=0.0, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='VSADP_VehSpdAvgDrvnAuth_Inv', Value=0, Type='Signal', Mode='HS')
    with allure.step('开启TeenDriver'):
        GMS.sendSignal(Signal='TeenDrvFtrAvl', Value=1, Type='Signal', Mode='HS')
    yield
    with allure.step('关掉TeenDriver'):
        GMS.sendSignal(Signal='TeenDrvFtrAvl', Value=0, Type='Signal', Mode='HS')
        while not d_obj(text="Settings").exists:
            d_obj.press("home")


@pytest.fixture(scope="function", params=None, autouse=False, ids=None, name=None)
def driver_seat_belts_are_bucked_up():
    GMS.sendSignal(Signal='ORIP_DrvrStBltStsAuth', Value=2, Type='Signal', Mode='HS')
    GMS.sendSignal(Signal='ORIP_DrvrStBltStsAuth_Inv', Value=0, Type='Signal', Mode='HS')
    GMS.sendSignal(Signal='FrntPsSeatbeltStat', Value=2, Type='Signal', Mode='HS')
    GMS.sendSignal(Signal='FrntPsSeatbeltStat_Inv', Value=0, Type='Signal', Mode='HS')

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


@pytest.fixture(scope="function", params=None, autouse=False, ids=None, name=None)
def report_card_close(d_obj: AndroidDevice):
    yield
    GMS.sendSignal(Signal='TDRCADD_DistDrvn', Value=0, Type='Signal', Mode='HS')
    GMS.sendSignal(Signal='TDRCADD_MaxSpd', Value=0, Type='Signal', Mode='HS')
    GMS.sendSignal(Signal='TDRCADD_OvSpdEvnt', Value=0, Type='Signal', Mode='HS')
    GMS.sendSignal(Signal='TDRCADD_WOTEvnts', Value=0, Type='Signal', Mode='HS')
    GMS.sendSignal(Signal='TDRCADD_FCHdwyAlrt', Value=0, Type='Signal', Mode='HS')
    GMS.sendSignal(Signal='TDRCADD_FCMBrEvts', Value=0, Type='Signal', Mode='HS')
    GMS.sendSignal(Signal='TDRCADD_RCMBrEvts', Value=0, Type='Signal', Mode='HS')
    GMS.sendSignal(Signal='TDRCADD_FCImntAlrts', Value=0, Type='Signal', Mode='HS')
    GMS.sendSignal(Signal='TDRCADD_LDWEvnts', Value=0, Type='Signal', Mode='HS')
    GMS.sendSignal(Signal='TDRCADD_TrCtrlEvnts', Value=0, Type='Signal', Mode='HS')
    GMS.sendSignal(Signal='TDRCADD_StCtrlEvnts', Value=0, Type='Signal', Mode='HS')
    GMS.sendSignal(Signal='TDRCADD_ABSAtvEvt', Value=0, Type='Signal', Mode='HS')
    d_obj.click(resourceId=element.back)
