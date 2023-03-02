#!/usr/bin/env python
# -*- ecoding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: element
@Created: 2023/2/23 20:00
"""
from typing import Text

xpath: Text
resourceId: Text
text: Text
description: Text
className: Text

enter: "resourceId" = "com.gm.teenmode:id/btn_action1"
delete: "resourceId" = "com.gm.teenmode:id/delete_btn"
close: "resourceId" = "com.gm.teenmode:id/icn_close_focus_area"
ok: "xpath" = '//*[@resource-id="com.gm.teenmode:id/button_focus_area"]/android.view.ViewGroup[1]'
add_or_remove_teen_driver_keys: "xpath" = '//*[@resource-id="com.gm.teenmode:id/list_content"]/android.view.ViewGroup[1]/android.widget.LinearLayout[1]'
view_report_card: "xpath" = '//*[@resource-id="com.gm.teenmode:id/list_content"]/android.view.ViewGroup[2]/android.widget.LinearLayout[1]'
teen_driver_settings: "xpath" = '//*[@resource-id="com.gm.teenmode:id/list_content"]/android.view.ViewGroup[3]/android.widget.LinearLayout[1]'
change_pin: "xpath" = '//*[@resource-id="com.gm.teenmode:id/list_content"]/android.view.ViewGroup[4]/android.widget.LinearLayout[1]'
clear_pin_and_teen_driver_keys: "xpath" = '//*[@resource-id="com.gm.teenmode:id/list_content"]/android.view.ViewGroup[5]/android.widget.LinearLayout[1]'
txt_dialog_message: "resourceId" = "com.gm.teenmode:id/txt_dialog_message"
report_card_reset_btn: "resourceId" = "com.gm.teenmode:id/btn_reset_report_card"
back: "resourceId" = "com.gm.teenmode:id/car_ui_toolbar_nav_icon"
vehicle_teen_driver: "xpath" = '//*[@resource-id="com.gm.hmi.settings:id/rv_vehicle_sub_menu"]/android.view.ViewGroup[1]/android.widget.LinearLayout[1]'
btn_volume_increase: "resourceId" = "com.gm.teenmode:id/btn_fab_plus"
btn_volume_decrease: "resourceId" = "com.gm.teenmode:id/btn_fab_minus"
