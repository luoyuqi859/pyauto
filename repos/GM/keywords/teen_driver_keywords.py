#!/usr/bin/env python
# -*- ecoding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: teen_driver_keywords
@Created: 2023/2/24 13:43
"""
import allure

from repos.GM.keywords.gm_vehicle_sim import GMS


@allure.step("Send No Action Request Signal")
def send_no_action_request_signal():
    GMS.sendSignal(Signal='TeenDrvReq', Value=0, Type='Signal', Mode='HS')


@allure.step("Send No Action Response Signal")
def send_no_action_response_signal():
    GMS.sendSignal(Signal='TeenDrvRsp', Value=0, Type='Signal', Mode='HS')


@allure.step("Send TEEN DRIVER ACTIVE AUTHENTICATED - FALSE Signal")
def send_teen_driver_active_authenticated_signal_false():
    GMS.sendSignal(Signal='TDAP_TeenDrvrActvAuth', Value=0, Type='Signal', Mode='HS')


@allure.step("Send Teen Driver Feature Unavailable Signal")
def send_teen_driver_feature_signal_unavailable():
    GMS.sendSignal(Signal='TeenDrvFtrAvl', Value=0, Type='Signal', Mode='HS')


@allure.step("Send TEEN DRIVER PIN STORED - FALSE Signal")
def send_teen_driver_pin_stored_signal_false():
    GMS.sendSignal(Signal='TnDrvPINStrd', Value=0, Type='Signal', Mode='HS')


@allure.step("Reset Teen Driver Signals used")
def reset_teen_driver_signals_used():
    send_no_action_request_signal()
    send_no_action_response_signal()
    send_teen_driver_active_authenticated_signal_false()
    send_teen_driver_feature_signal_unavailable()
    send_teen_driver_pin_stored_signal_false()
