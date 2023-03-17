#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: GMVehicleSim_Auto
@Created: 2023/3/9 11:01
"""
import time

from uiauto.windows.core import AiUiAutomation


def gm_my23_vcu_ecomate_open(path):
    AiUiAutomation.openApplication(path)
    time.sleep(1)
    simulator = AiUiAutomation.PaneControl(Name='GM Vehicle Simulator')
    simulator.ButtonControl(Name='VCU').Click()
    time.sleep(5)
    vcu = AiUiAutomation.WindowControl(Name='VCU')
    time.sleep(1)
    vcu.CheckBoxControl(Name="DisableVIN").Click()
    menuStrip = vcu.MenuBarControl(Name='menuStrip2')
    connect = menuStrip.MenuItemControl(Name="Connect")
    connect.Click()
    time.sleep(1)
    connectDropDown = vcu.MenuControl(Name="ConnectDropDown")
    connectDropDown.MoveCursorToInnerPos(y=-100)
    time.sleep(1)
    ecomateDropDown = vcu.MenuControl(Name="ECOMateDropDown")
    time.sleep(1)
    ecomateDropDown.MoveCursorToInnerPos(y=-70)
    time.sleep(1)
    ecomateDropDown.Click(20, 20)
    time.sleep(1)
    vcu.RadioButtonControl(Name="Run").Click()


def gm_my23_vcu_ecomate_open1():
    vcu = AiUiAutomation.WindowControl(Name='VCU')
    vcu.SetActive()
    vcu.RadioButtonControl(Name="Acc").Click()


def gm_my23_vcu_close():
    vcu = AiUiAutomation.WindowControl(Name='VCU')
    AiUiAutomation.setWindowActive(vcu)
    vcu.RadioButtonControl(Name="Off").Click()
    AiUiAutomation.closeApplication("GMVehicleSim.exe")


if __name__ == '__main__':
    gm_my23_vcu_ecomate_open(r'D:\vcu\GMVehicleSimulator\GMVehicleSim.exe')
    # gm_my23_vcu_close()
    # gm_my23_vcu_ecomate_open1()
