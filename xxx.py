#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: xxx
@Created: 2023/3/8 14:29
"""

import subprocess
import time

from win32api import mouse_event

from uiauto.windows.core import AiUiAutomation

# subprocess.Popen(r'D:\vcu\GMVehicleSimulator\GMVehicleSim.exe')
# time.sleep(2)
# simulator = auto.PaneControl(Name='GM Vehicle Simulator')
# simulator.ButtonControl(Name='VCU').Click()
# time.sleep(7)
# vcu = auto.WindowControl(Name='VCU')
# time.sleep(2)
# vcu.CheckBoxControl(Name="DisableVIN").Click()
# menuStrip = vcu.MenuBarControl(Name='menuStrip2')
# connect = menuStrip.MenuItemControl(Name="Connect")
# connect.Click()
# time.sleep(2)
# connectDropDown = vcu.MenuControl(Name="ConnectDropDown")
# connectDropDown.MoveCursorToInnerPos(y=-100)
# time.sleep(2)
# ecomateDropDown = vcu.MenuControl(Name="ECOMateDropDown")
# time.sleep(2)
# ecomateDropDown.MoveCursorToInnerPos(y=-70)
# time.sleep(2)
# ecomateDropDown.Click(20, 20)
# time.sleep(2)
# vcu.RadioButtonControl(Name="Run").Click()

AiUiAutomation.openApplication(r'D:\vcu\GMVehicleSimulator\GMVehicleSim.exe')
time.sleep(2)
simulator = AiUiAutomation.PaneControl(Name='GM Vehicle Simulator')
simulator.ButtonControl(Name='VCU').Click()
time.sleep(5)
vcu = AiUiAutomation.WindowControl(Name='VCU')
time.sleep(2)
vcu.CheckBoxControl(Name="DisableVIN").Click()
menuStrip = vcu.MenuBarControl(Name='menuStrip2')
connect = menuStrip.MenuItemControl(Name="Connect")
connect.Click()
time.sleep(2)
connectDropDown = vcu.MenuControl(Name="ConnectDropDown")
connectDropDown.MoveCursorToInnerPos(y=-100)
time.sleep(2)
ecomateDropDown = vcu.MenuControl(Name="ECOMateDropDown")
time.sleep(2)
ecomateDropDown.MoveCursorToInnerPos(y=-70)
time.sleep(2)
ecomateDropDown.Click(20, 20)
time.sleep(2)
vcu.RadioButtonControl(Name="Run").Click()


vcu = AiUiAutomation.WindowControl(Name='VCU')
AiUiAutomation.setWindowActive(vcu)
vcu.RadioButtonControl(Name="Off").Click()
AiUiAutomation.closeApplication("GMVehicleSim.exe")

# vcu = auto.WindowControl(Name='VCU')
# vcu.WheelUp()
# vcu.RadioButtonControl(Name="Acc").Click()
# vcu.Show(0)

# print(connectDropDown.GetChildren())
# ecomate = vcu.MenuControl(Name="ECOMateDropDown")
# ecomate.Click()

# print(windows.SetTopmost())
# print(uiautomation.GetRootControl())
# task = uiautomation.ButtonControl(Name='GMVehicleSimulator')#search 2 times
# gmVehicleSimulatorWindow = uiautomation.ButtonControl(searchDepth=4, Name='GMVehicleSimulator')
# print(task.Name)
# f = windows.RadioButtonControl(Name="Acc").Click()
# pass
# gmVehicleSimulatorWindow.
# print(notepadWindow.Name)
# print(gmWindow.GetPosition())
# edit = notepadWindow.EditControl()
# edit.SetValue('Hello')
# edit.SendKeys('{Ctrl}{End}{Enter}World')
