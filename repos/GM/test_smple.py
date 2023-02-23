#!/usr/bin/env python
# -*- ecoding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: test_smple.py
@Created: 2023/2/20 13:50
"""
#
# import time
# import allure
# from repos.GM.keywords.gm_vehicle_sim import GMSignal
# from uiauto.android.device import AndroidDevice
#
# GMS = GMSignal()
#
#
# def setup():
#     with allure.step('初始化TeenDriver'):
#         GMS.sendSignal(Signal='TeenDrvFtrAvl', Value=1, Type='Signal', Mode='HS')
#
#
# def test_350853(device: AndroidDevice):
#     with allure.step('step1: Click Settings'):
#         device.d(text="Settings").click()
#     with allure.step('step2: Click Vehicle'):
#         device.d(text="Vehicle").click()
#     with allure.step('step3: Click Teen Driver'):
#         device.d(text="Teen Driver").click()
#     with allure.step('step4: assert Teen Driver'):
#         time.sleep(2)
#         device.assert_exist("Teen Driver")
#     with allure.step('step5: go home --> Vehicle -->Teen Driver.'):
#         device.d.xpath(
#             '//*[@resource-id="com.android.systemui:id/button_container"]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]').click()
#
#
# def teardown():
#     with allure.step('关掉TeenDriver'):
#         GMS.sendSignal(Signal='TeenDrvFtrAvl', Value=0, Type='Signal', Mode='HS')

# if __name__ == '__main__':
#     pytest.main(["test_xxx"])
