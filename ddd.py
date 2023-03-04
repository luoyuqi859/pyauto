#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: ddd
@Created: 2023/2/21 17:42
"""
import time

from repos.GM.keywords.gm_vehicle_sim import GMS
# import time
#
# # import uiautomator2 as u2
#
#
# from repos.GM.keywords.gm_vehicle_sim import GMS
# # from uiauto.android.adb import ADB
from uiauto.android.device import connect, AndroidDevice

#
#
# # serial = ADB().adb.serial
# # device = u2.Device(serial)
# # GMS.sendSignal(Signal='TeenDrvFtrAvl', Value=1, Type='Signal', Mode='HS')
conn = connect()
device = AndroidDevice(conn)
# device.minicap.install_minicap()
print(device.d.info)
print("初始化设备成功")
# device.screenshot.save_grid("./test.png")
# f = device.page.find_element(0.12, 0.4)
# f = device.info
# print(device.serial)
# device(text="刷新服务状态").screenshot("./test.png")
# print(device.ocr.image_to_text('./test.png'))
# device.swipe.down()
# device.click(text="我的设备")
# GMS.sendSignal(Signal='TDAP_TeenDrvrActvAuth', Value=1, Type='Signal', Mode='HS')
# GMS.sendSignal(Signal='ORIP_DrvrStBltStsAuth', Value=2, Type='Signal', Mode='HS')
# GMS.sendSignal(Signal='ORIP_DrvrStBltStsAuth_Inv', Value=0, Type='Signal', Mode='HS')
# GMS.sendSignal(Signal='FrntPsSeatbeltStat', Value=2, Type='Signal', Mode='HS')
# GMS.sendSignal(Signal='FrntPsSeatbeltStat_Inv', Value=0, Type='Signal', Mode='HS')
# GMS.sendSignal(Signal='TDAP_TeenDrvrActvAuth', Value=1, Type='Signal', Mode='HS')
# f = device(text="Off").offset(x=0.12)

# print(device.ocr.image_to_text('./menu_unavailable_while_driving.png'))
# GMS.sendSignal(Signal='TnDrvOvSpdWrnCstStAvl', Value=1, Type='Signal', Mode='HS')
# d(reso)
# a = f
# device.screenshot.save_grid('./test.png')
# device(resourceId='com.gm.teenmode:id').child(className="com.android.car.ui.FocusArea").child(resourceId='com.gm.teenmode:id/list_content').screenshot('./test1.png')
# print("截图成功")
# print(device.page.source)
# device.click(text="Settings")
# e = device(resourceId='com.gm.hmi.settings:id/car_ui_list_item_text_container')[1]
# e.click()
# time.sleep(1)
# el = device(resourceId='com.gm.hmi.settings:id/rv_vehicle_sub_menu').child(className="android.view.ViewGroup",
#                                                                           index=3)
# el.screenshot('./menu_unavailable_while_driving.png')
# # #
# # device.minicap.install_minicap()
# # # time.sleep(3)
# # device.screenshot.save('./test.png')
# # a = f
# GMS.sendSignal(Signal='TnDrvOvSpdWrnCstStAvl', Value=1, Type='Signal', Mode='HS')
# GMS.sendSignal(Signal='TDOSWCCSV_CrSetVal', Value=2, Type='Signal', Mode='HS')
# f = device.ocr.image_to_text('./menu_unavailable_while_driving.png')
# print(f)
# GMS.sendSignal(Signal='TnDrvPINStrd', Value=0, Type='Signal', Mode='HS')
# GMS.sendSignal(Signal='TeenDrvReq', Value=0, Type='Signal', Mode='HS')
# GMS.sendSignal(Signal='TeenDrvRsp', Value=2, Type='Signal', Mode='HS')
# GMS.sendSignal(Signal='TDAP_TeenDrvrActvAuth', Value=0, Type='Signal', Mode='HS')
# GMS.sendSignal(Signal='TEGP_TrnsShftLvrPstnAuth', Value=1, Type='Signal', Mode='HS')
# GMS.sendSignal(Signal='TEGP_TrnsShftLvrPstnAuth_Inv', Value=0, Type='Signal', Mode='HS')
# GMS.sendSignal(Signal='VMMP_VehMtnMvmtStatAuth', Value=0, Type='Signal', Mode='HS')
# GMS.sendSignal(Signal='VSADP_VehSpdAvgDrvnAuth', Value=0.0, Type='Signal', Mode='HS')
# GMS.sendSignal(Signal='VSADP_VehSpdAvgDrvnAuth_Inv', Value=0, Type='Signal', Mode='HS')
# # device
# # device.click(xpath='//*[@resource-id="com.gm.hmi.settings:id/rv_vehicle_sub_menu"]/android.view.ViewGroup[4]')
# # print(device.info)
# # f = device.page.display_bounds
# # print(f)
# pass
#
# # device(text="设置").screenshot('./test.png')
# # e = device(resourceId='com.gm.hmi.settings:id/car_ui_list_item_text_container')[1]
# # e.click()
# # print(time.time())
# # time.sleep(1)
# # print(device.page.source)
#
# # print(time.time())
# # time.sleep(1)
# # el = device(resourceId='com.gm.hmi.settings:id/rv_vehicle_sub_menu').child(className="android.view.ViewGroup", index=3)
# #
# # el.screenshot('./test.png')
# # time.sleep(2)
# # f = Ocr.pytesseract_image_to_string('./test.png')
# # print(f)
# # from paddleocr import PaddleOCR, draw_ocr
#
# # ocr = PaddleOCR(enable_mkldnn=True, use_tensorrt=True, use_angle_cls=False, use_gpu=False)
# # ocr = PaddleOCR(use_angle_cls=True, lang="ch", det_model_dir="./inference/det/", rec_model_dir="./inference/rec/",
# #                 cls_model_dir="./inference/cls/")
# # # ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # need to run only once to download and load model into memory
# # img_path = './test.png'
# # result = ocr.ocr(img_path, cls=True)
# # for line in result:
# #     print('dd', line)
# # for idx in range(len(result)):
# #     for line in result:
# #         print(line)
# #     res = result[idx]
# #     for line in res:
# #         print('ddd', line)
# # ocr = PaddleOCR(use_angle_cls=True, lang="ch") # need to run only once to download and load model into memory
# # img_path = './test.png'
# # result = ocr.ocr(img_path, cls=True)
# # for line in result:
# #     print(line)
#
# # q = get_image_text('./test.png')
# # print(q)
# # device.swipe(0.3, 0.7, 0.3, 0.3)
# # device.swipe.down.until_exists(text="System")
# f = "b9f24c2d"
# e = "174d37c1"
# # d = u2.connect_usb(serial="174d37c1")
# # el = d.xpath('//*[@resource-id="com.android.car.settings:id/fragment_container"]/android.widget.FrameLayout[1]').get()
# # xxx = el.bounds # 获取左上角坐标和宽高
# # el = d.xpath('//*[@resource-id="com.android.car.settings:id/fragment_container"]/android.widget.FrameLayout[1]').get()
# # # d.swipe_ext("up", box=(165, 2406, 1158, 327), scale=0.8)
# # # lx, ly, width, height = el.rect # 获取左上角坐标和宽高
# # print(d.window_size())
# # lx, ly, rx, ry = el.bounds  # 左上角与右下角的坐标
# # fx = (ly + ry) / 2
# # fy = (rx - lx) / 2 + lx -400
# # tx = (ly + ry) / 2
# # ty = (rx - lx) / 2 - lx
# # for i in range(5):
# #     d.swipe(fx=fx, fy=fy, tx=tx, ty=ty)
#
# # print(device.d.info)
# # print(d.window_size())
# # GMS.sendSignal(Signal='TeenDrvFtrAvl', Value=1, Type='Signal', Mode='HS')
# # device.swipe.down.until_exists(text="System")
# # GMS.sendSignal(Signal='TDRCADD_WOTEvnts', Value=1, Type='Signal', Mode='HS')
# # GMS.sendSignal(Signal='TeenDrvWOTEvntsRpt', Value=1000, Type='Signal', Mode='HS')
# # device.swipe(661, 1000, 661, 712)
# # device.swipe.down.until_exists(text="更多设置")
# # device.swipe(661, 1000, 661, 712)
# # d.drag(0.45, 0.7, 0.45, 0.2)
# # GMS.sendSignal(Signal='TnDrvOvSpdEvntsRpt', Value=0, Type='Signal', Mode='HS')
# # GMS.sendSignal(Signal='TeenDrvWOTEvntsRpt', Value=0, Type='Signal', Mode='HS')
# # GMS.sendSignal(Signal='TDFwdClnImntAlrtsRpt', Value=0, Type='Signal', Mode='HS')
# # GMS.sendSignal(Signal='TDFwdClnMtgnBrEvRpt', Value=0, Type='Signal', Mode='HS')
# # GMS.sendSignal(Signal='TDRevClnMtgnBrEvRpt', Value=0, Type='Signal', Mode='HS')
# # GMS.sendSignal(Signal='TeenDrvLDWEvntsRpt', Value=0, Type='Signal', Mode='HS')
# # GMS.sendSignal(Signal='TDFwdClnHdwyAlrtsRpt', Value=0, Type='Signal', Mode='HS')
# # GMS.sendSignal(Signal='TnDrvStblCtrlEvntsRpt', Value=0, Type='Signal', Mode='HS')
# # GMS.sendSignal(Signal='TnDrvABSAtvEvntsRpt', Value=0, Type='Signal', Mode='HS')
# # GMS.sendSignal(Signal='TnDrvTrCtrlEvntsRpt', Value=0, Type='Signal', Mode='HS')
# # GMS.sendSignal(Signal='TnDrvDistDrvnRpt', Value=0, Type='Signal', Mode='HS')
# # GMS.sendSignal(Signal='TeenDrvMaxSpdRpt', Value=0, Type='Signal', Mode='HS')
#
# # GMS.sendSignal(Signal='TDRCADD_DistDrvn', Value=0, Type='Signal', Mode='HS')
# # GMS.sendSignal(Signal='TDRCADD_MaxSpd', Value=0, Type='Signal', Mode='HS')
# # GMS.sendSignal(Signal='TDRCADD_OvSpdEvnt', Value=0, Type='Signal', Mode='HS')
# # GMS.sendSignal(Signal='TDRCADD_WOTEvnts', Value=0, Type='Signal', Mode='HS')
# # GMS.sendSignal(Signal='TDRCADD_FCHdwyAlrt', Value=0, Type='Signal', Mode='HS')
# # GMS.sendSignal(Signal='TDRCADD_FCMBrEvts', Value=0, Type='Signal', Mode='HS')
# # GMS.sendSignal(Signal='TDRCADD_RCMBrEvts', Value=0, Type='Signal', Mode='HS')
# # GMS.sendSignal(Signal='TDRCADD_FCImntAlrts', Value=0, Type='Signal', Mode='HS')
# # GMS.sendSignal(Signal='TDRCADD_LDWEvnts', Value=0, Type='Signal', Mode='HS')
# # GMS.sendSignal(Signal='TDRCADD_TrCtrlEvnts', Value=0, Type='Signal', Mode='HS')
# # GMS.sendSignal(Signal='TDRCADD_StCtrlEvnts', Value=0, Type='Signal', Mode='HS')
# # GMS.sendSignal(Signal='TDRCADD_ABSAtvEvt', Value=0, Type='Signal', Mode='HS')
# # time.sleep(3)
# # GMS.sendSignal(Signal='TnDrvPINStrd', Value=0, Type='Signal', Mode='HS')
# # GMS.sendSignal(Signal='TeenDrvRsp', Value=2, Type='Signal', Mode='HS')
# # device.up()
# # GMS.sendSignal(Signal='TDRCADD_DistDrvn', Value=0, Type='Signal', Mode='HS')
# time.sleep(1)
# # GMS.sendSignal(Signal='TDRCADD_MaxSpd', Value=0, Type='Signal', Mode='HS')
# # GMS.sendSignal(Signal='TDRCADD_OvSpdEvnt', Value=0, Type='Signal', Mode='HS')
# # GMS.sendSignal(Signal='TDRCADD_WOTEvnts', Value=0, Type='Signal', Mode='HS')
# # GMS.sendSignal(Signal='TDRCADD_FCHdwyAlrt', Value=0, Type='Signal', Mode='HS')
# # GMS.sendSignal(Signal='TDRCADD_FCMBrEvts', Value=0, Type='Signal', Mode='HS')
# # GMS.sendSignal(Signal='TDRCADD_RCMBrEvts', Value=0, Type='Signal', Mode='HS')
# # GMS.sendSignal(Signal='TDRCADD_FCImntAlrts', Value=0, Type='Signal', Mode='HS')
# # GMS.sendSignal(Signal='TDRCADD_LDWEvnts', Value=0, Type='Signal', Mode='HS')
# # GMS.sendSignal(Signal='TDRCADD_TrCtrlEvnts', Value=0, Type='Signal', Mode='HS')
# # GMS.sendSignal(Signal='TDRCADD_StCtrlEvnts', Value=0, Type='Signal', Mode='HS')
# # GMS.sendSignal(Signal='TDRCADD_ABSAtvEvt', Value=0, Type='Signal', Mode='HS')
# # device.swipe.down.until_exists(text="display")
# # print(device(text="Settings").enabled)
# # print(device)
