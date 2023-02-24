#!/usr/bin/env python
# -*- ecoding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: ddd
@Created: 2023/2/23 17:42
"""
import time

import allure
import pytest

from repos.GM.TeenDriver import element
from repos.GM.keywords.gm_vehicle_sim import GMS
from uiauto.android.device import AndroidDevice


@allure.title('Launch the "Teen Driver" app with Android Intent.')
def test_323313(d_obj: AndroidDevice):
    with allure.step("1. Press Home button."):
        d_obj.press("home")
    with allure.step("2.adb shell am start -a com.gm.teenmode.app.LAUNCH"):
        d_obj.adb_fp.adb.run_adb_cmd("shell am start -a com.gm.teenmode.app.LAUNCH")
        time.sleep(1)
        d_obj.assert_exist(
            text="Teen Driver")
        d_obj.assert_exist(
            text="Set a key with custom restrictions and alerts that can help your teen make good driving decisions. See your Owner’s Manual for details.")


@allure.title('To verify if user can enter 4-digit PIN to set Teen Driver code')
def test_329112(d_obj: AndroidDevice):
    with allure.step("1. Launch Settings"):
        d_obj.click(text="Settings")
    with allure.step("2. Select Vehicle"):
        d_obj.click(text="Vehicle")
    with allure.step("3. Look for the Teen Driver option in the list."):
        d_obj.assert_exist(text="Teen Driver")
    with allure.step('4. Select Teen Driver option'):
        d_obj.click(text="Teen Driver")
    with allure.step('5. Select Continue to create a 4-digit PIN'):
        d_obj.click(text="Continue")
        d_obj.assert_exist(text="Enter a 4-digit PIN to set up Teen Driver.")
    with allure.step('6. Enter 4 digits of PIN'):
        d_obj.click(text="1").click(text="2").click(text="3").click(text="4")
        assert d_obj.d(resourceId=element.enter).info.get("focusable", None) == True, "校验元素聚焦失败"
    with allure.step('7. Select Enter button'):
        d_obj.click(resourceId=element.enter)
        d_obj.assert_exist(text="Confirm your 4-digit PIN.")


@allure.title('To verify the Continue button functionality from the Info Page')
def test_333196(d_obj: AndroidDevice):
    with allure.step(
            '1. Open the "Info" page by tapping "Teen Driver" option or by command such as "adb shell am start -a com.gm.teenmode.app.LAUNCH" '):
        d_obj.adb_fp.adb.run_adb_cmd("shell am start -a com.gm.teenmode.app.LAUNCH")
    with allure.step('2. click on the "Continue" button'):
        d_obj.click(text="Continue")
        d_obj.assert_exist(text="Enter a 4-digit PIN to set up Teen Driver.")


@allure.title(
    'Confirm Code Screen : Enter 4 digits and check the behaviour of "Delete", "Set" and  "Number Pad" Option')
def test_350854(d_obj: AndroidDevice):
    with allure.step('1. Click Settings --> Vehicle -->Teen Driver.'):
        d_obj.click(text="Settings").click(text="Vehicle").click(text="Teen Driver")
        d_obj.assert_exist(text="Teen Driver")
    with allure.step('2.Select Continue to create a 4-digit PIN'):
        d_obj.click(text="Continue")
        d_obj.assert_exist(text="Enter a 4-digit PIN to set up Teen Driver.")
    with allure.step('3. Enter 4-digit number and click on "Enter".'):
        d_obj.click(text="1").click(text="2").click(text="3").click(text="4")
        d_obj.click(resourceId=element.enter)
        d_obj.assert_exist(text="Confirm your 4-digit PIN.")
    with allure.step('4. Enter 4 digits using the Keypad and check the "Delete","Set" and Number pad options.'):
        d_obj.click(text="1").click(text="2").click(text="3").click(text="4")
        assert d_obj.d(text="1").info.get("enabled", None) == False, "校验数字键盘不可用失败"
        assert d_obj.d(resourceId=element.enter).info.get("enabled", None) == True, "校验删除键可用失败"
        assert d_obj.d(resourceId=element.delete).info.get("enabled", None) == True, "校验ENTER键可用失败"


@allure.title('To Verify the Code Set')
def test_363660(d_obj: AndroidDevice):
    with allure.step('1. Open Teen Driver Option'):
        d_obj.click(text="Settings").click(text="Vehicle").click(text="Teen Driver")
        d_obj.click(text="Continue")
    with allure.step('2.Enter a 4 digit pin and enter'):
        d_obj.click(text="1").click(text="2").click(text="3").click(text="4")
        d_obj.click(resourceId=element.enter)
    with allure.step('3. Enter a 4 digit pin that is the same the previous one'):
        d_obj.click(text="1").click(text="2").click(text="3").click(text="4")
    with allure.step(
            '4. Send the CAN Signal "TeenDrvRsp"To do this:- Go to GMVehicle Sim -> Tools -> Signal1.TeenDrvRsp : 0 = No_Action2.Click on Set Button and send below signal within 3 seconds3.TeenDrvRsp : 2 = Teen_PIN_Updated'):
        GMS.sendSignal(Signal='TeenDrvRsp', Value=0, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='TeenDrvRsp', Value=2, Type='Signal', Mode='HS')
        d_obj.click(resourceId=element.enter)
        d_obj.assert_exist(xpath=element.ok)


@allure.title('System Locked Screen: "Enter Teen Driver PIN screen" should not show when PIN code has not been set')
def test_364374(d_obj: AndroidDevice):
    with allure.step('1. Click Settings --> Vehicle -->Teen Driver.'):
        d_obj.click(text="Settings").click(text="Vehicle").click(text="Teen Driver")
        d_obj.click(text="Continue")
    with allure.step('2. Enter 4 digit PIN and pres "Enter" to go to next screen.'):
        d_obj.click(text="1").click(text="2").click(text="3").click(text="4")
        d_obj.click(resourceId=element.enter)
    with allure.step('3. Press Home key to return to Home Screen'):
        d_obj.press('home')
    with allure.step('4. Click Settings --> Vehicle -->Teen Driver.'):
        d_obj.click(text="Settings").click(text="Vehicle").click(text="Teen Driver")
    with allure.step('5. Verify if Unlock Screen with "Enter Teen Driver PIN" is displayed.'):
        d_obj.click(text="Settings").click(text="Vehicle").click(text="Teen Driver")
        d_obj.assert_not_exist(text="Enter a 4-digit PIN to set up Teen Driver.")


@allure.title('To Verify clicking on the &#8220;X&#8221; button from the Teen Driver Error Screen')
def test_364474(d_obj: AndroidDevice):
    with allure.step('1. send TnDrvPINStrd --> True, to open Unlock code screen.'):
        GMS.sendSignal(Signal='TnDrvPINStrd', Value=1, Type='Signal', Mode='HS')
    with allure.step('2.Go to Settings -> Vehicle -> Before clicking on Teen Driver menu.'):
        d_obj.click(text="Settings").click(text="Vehicle").click(text="Teen Driver")
    with allure.step('3.enter any 4 digit pin.'):
        d_obj.click(text="1").click(text="2").click(text="3").click(text="4")
    with allure.step('4.Press Unlock button'):
        d_obj.click(resourceId=element.enter)
    with allure.step('5. Wait up to 3 seconds'):
        time.sleep(3)
    with allure.step('6. Click on the "X" button'):
        d_obj.click(resourceId=element.close)
        d_obj.assert_exist(text="Teen Driver")


@allure.title('Incorrect Code Screen : Launch the Screen.')
@pytest.mark.usefixtures("pin_code_save")
def test_364496(d_obj: AndroidDevice):
    with allure.step('1. sendTnDrvPINStrd --> True to open Unlock code screen.'):
        GMS.sendSignal(Signal='TnDrvPINStrd', Value=1, Type='Signal', Mode='HS')
    with allure.step('2.Go to Settings -> Vehicle -> Before clicking on Teen Driver menu.'):
        d_obj.click(text="Settings").click(text="Vehicle").click(text="Teen Driver")
    with allure.step('3.enter any 4 digit pin.'):
        d_obj.click(text="1").click(text="2").click(text="3").click(text="4")
    with allure.step('4. send TeenDrvRsp -->3 =Teen_PIN_Mismatchto open the Incorrect code popup.'):
        GMS.sendSignal(Signal='TeenDrvRsp', Value=3, Type='Signal', Mode='HS')
    with allure.step('5. press unlock'):
        d_obj.click(resourceId=element.enter)
        d_obj.assert_exist(text="Wrong PIN")
        d_obj.assert_exist(text="Enter your Teen Driver PIN. Tap Retry, or visit a dealer to reset your PIN.")


@allure.title('To Verify Teen Pin menu screen - Pin Verify')
def test_372410(d_obj: AndroidDevice):
    with allure.step('1. send TnDrvPINStrd --> False to open Unlock code screen.'):
        GMS.sendSignal(Signal='TnDrvPINStrd', Value=0, Type='Signal', Mode='HS')
    with allure.step('2. Enter teen dricver screen'):
        d_obj.click(text="Settings").click(text="Vehicle").click(text="Teen Driver")
        d_obj.click(text="Continue")
    with allure.step('3. Enter pin'):
        d_obj.click(text="1").click(text="2").click(text="3").click(text="4")
    with allure.step('4. Press enter'):
        d_obj.click(resourceId=element.enter)
    with allure.step('5. Enter same pin'):
        d_obj.click(text="1").click(text="2").click(text="3").click(text="4")
    with allure.step('6. Pess set and send TeenDrvRsp --> 2 = Teen_PIN_updated'):
        GMS.sendSignal(Signal='TeenDrvRsp', Value=2, Type='Signal', Mode='HS')
    with allure.step('7. Teen driver pin set pop-up display'):
        d_obj.click(resourceId=element.enter)
    with allure.step('8. Press Ok'):
        d_obj.click(xpath=element.ok)
    with allure.step('9. Teen pin menu screen will display'):
        d_obj.assert_exist(xpath=element.add_or_remove_teen_driver_keys)
        d_obj.assert_exist(xpath=element.view_report_card)
        d_obj.assert_exist(xpath=element.teen_driver_settings)
        d_obj.assert_exist(xpath=element.change_pin)


# @allure.title(
#     'To verify status of radio button in "Buckle to Drive" tertiary screen is matched with the "Buckle to Drive" switch under Teen Driver Settings‎')
# def test_382854(d_obj: AndroidDevice):
#     with allure.step('1. Navigate to Teen driver'):
#         d_obj.click(text="Settings").click(text="Vehicle").click(text="Teen Driver")
#     with allure.step('2. Send Teen Driver Seat Belt Shift Interlock Available'):
#         GMS.sendSignal(Signal='TnDrvStBltShfIntlkCstSetAval', Value=1, Type='Signal', Mode='HS')
#     with allure.step('3. Send Teen Driver Seat Belt Shift Interlock Value'):
#         GMS.sendSignal(Signal='TnDrvStBltShfIntlkCstCurrSetVal', Value=1, Type='Signal', Mode='HS')
#     with allure.step('4. Click Teen driver settings option'):
#         d_obj.click(resourceId=element.enter)

@allure.title('To verify whether user is able to change the already set PIN')
def test_385117(d_obj: AndroidDevice):
    with allure.step('1. Open Settings Application'):
        d_obj.click(text="Settings")
    with allure.step('2. Send Teen Driver available signal'):
        GMS.sendSignal(Signal='TeenDrvFtrAvl', Value=1, Type='Signal', Mode='HS')
    with allure.step('3. Select Vehicle '):
        d_obj.click(text="Vehicle")
    with allure.step('4. Select Teen Driver'):
        d_obj.click(text="Teen Driver")
    with allure.step('5. Click continue'):
        d_obj.click(text="Continue")
    with allure.step('6. Enter a 4 digit PIN to setup Teen Driver'):
        d_obj.click(text="1").click(text="2").click(text="3").click(text="4")
    with allure.step('7. Click Enter  '):
        d_obj.click(resourceId=element.enter)
    with allure.step('8. Confirm your 4 digit PIN'):
        d_obj.click(text="1").click(text="2").click(text="3").click(text="4")
    with allure.step('9. Send TEEN PIN UPDATED signal'):
        GMS.sendSignal(Signal='TeenDrvRsp', Value=2, Type='Signal', Mode='HS')
    with allure.step('10. Click Set'):
        d_obj.click(resourceId=element.enter)
    with allure.step('11. Click OK in Teen Driver PIN set pop-up'):
        d_obj.click(xpath=element.ok)
    with allure.step('12. Click Back button to go to Vehicle Menu'):
        d_obj.press('back')
    with allure.step('13. Send TEEN PIN STORED signal'):
        GMS.sendSignal(Signal='TnDrvPINStrd', Value=1, Type='Signal', Mode='HS')
    with allure.step('14. Select Teen Driver'):
        d_obj.click(text="Teen Driver")
    with allure.step('15. Enter your 4 digit Teen Driver PIN'):
        d_obj.click(text="1").click(text="2").click(text="3").click(text="4")
    with allure.step('16. Send TEEN PIN VERIFIED signal'):
        GMS.sendSignal(Signal='TeenDrvRsp', Value=1, Type='Signal', Mode='HS')
    with allure.step('17. Click Unlock'):
        d_obj.click(resourceId=element.enter)
    with allure.step('18. Click Change PIN'):
        d_obj.click(xpath=element.change_pin)
    with allure.step('19. Enter a 4 digit PIN to setup Teen Driver'):
        d_obj.click(text="1").click(text="2").click(text="3").click(text="4")
    with allure.step('20. Click Enter'):
        d_obj.click(resourceId=element.enter)
    with allure.step('21. Confirm your 4 digit PIN'):
        d_obj.click(text="1").click(text="2").click(text="3").click(text="4")
    with allure.step('22. Send TEEN PIN UPDATED signal'):
        GMS.sendSignal(Signal='TeenDrvRsp', Value=2, Type='Signal', Mode='HS')
    with allure.step('23. Click Set'):
        d_obj.click(resourceId=element.enter)
        d_obj.assert_exist(
            text="Write down your new PIN. A forgotten PIN can only be reset at your dealer. To activate Teen Driver, you'll need to add the teen's key.")
    with allure.step('24. Click OK in Teen Driver PIN set pop-up'):
        d_obj.click(xpath=element.ok)
        d_obj.assert_exist(xpath=element.add_or_remove_teen_driver_keys)
        d_obj.assert_exist(xpath=element.view_report_card)
        d_obj.assert_exist(xpath=element.teen_driver_settings)
        d_obj.assert_exist(xpath=element.change_pin)


@allure.title("To verify the Retry button functionality in PIN doesn't match error pop while changing the PIN")
def test_385119(d_obj: AndroidDevice):
    with allure.step('1. Open Settings Application'):
        d_obj.click(text="Settings")
    with allure.step('2. Send Teen Driver available signal'):
        GMS.sendSignal(Signal='TeenDrvFtrAvl', Value=1, Type='Signal', Mode='HS')
    with allure.step('3. Select Vehicle '):
        d_obj.click(text="Vehicle")
    with allure.step('4. Select Teen Driver'):
        d_obj.click(text="Teen Driver")
    with allure.step('5. Click continue'):
        d_obj.click(text="Continue")
    with allure.step('6. Enter a 4 digit PIN to setup Teen Driver'):
        d_obj.click(text="1").click(text="2").click(text="3").click(text="4")
    with allure.step('7. Click Enter  '):
        d_obj.click(resourceId=element.enter)
    with allure.step('8. Confirm your 4 digit PIN'):
        d_obj.click(text="1").click(text="2").click(text="3").click(text="4")
    with allure.step('9. Send TEEN PIN UPDATED signal'):
        GMS.sendSignal(Signal='TeenDrvRsp', Value=2, Type='Signal', Mode='HS')
    with allure.step('10. Click Set'):
        d_obj.click(resourceId=element.enter)
    with allure.step('11. Click OK in Teen Driver PIN set pop-up'):
        d_obj.click(xpath=element.ok)
    with allure.step('12. Click Back button to go to Vehicle Menu'):
        d_obj.press('back')
    with allure.step('13. Send TEEN PIN STORED signal'):
        GMS.sendSignal(Signal='TnDrvPINStrd', Value=1, Type='Signal', Mode='HS')
    with allure.step('14. Select Teen Driver'):
        d_obj.click(text="Teen Driver")
    with allure.step('15. Enter your 4 digit Teen Driver PIN'):
        d_obj.click(text="1").click(text="2").click(text="3").click(text="4")
    with allure.step('16. Send TEEN PIN VERIFIED signal'):
        GMS.sendSignal(Signal='TeenDrvRsp', Value=1, Type='Signal', Mode='HS')
    with allure.step('17. Click Unlock'):
        d_obj.click(resourceId=element.enter)
    with allure.step('18. Click Change PIN'):
        d_obj.click(xpath=element.change_pin)
    with allure.step('19. Enter a 4 digit PIN to setup Teen Driver'):
        d_obj.click(text="1").click(text="2").click(text="3").click(text="4")
    with allure.step('20. Click Enter'):
        d_obj.click(resourceId=element.enter)
    with allure.step('21. Confirm your 4 digit PIN'):
        d_obj.click(text="1").click(text="2").click(text="3").click(text="4")
    with allure.step('22. Send TEEN PIN UPDATED signal'):
        GMS.sendSignal(Signal='TeenDrvRsp', Value=2, Type='Signal', Mode='HS')
    with allure.step('23. Click Set'):
        d_obj.click(resourceId=element.enter)
        d_obj.assert_exist(
            text="Write down your new PIN. A forgotten PIN can only be reset at your dealer. To activate Teen Driver, you'll need to add the teen's key.")
    with allure.step('24. Click OK in Teen Driver PIN set pop-up'):
        d_obj.click(xpath=element.ok)
        d_obj.assert_exist(xpath=element.add_or_remove_teen_driver_keys)
        d_obj.assert_exist(xpath=element.view_report_card)
        d_obj.assert_exist(xpath=element.teen_driver_settings)
        d_obj.assert_exist(xpath=element.change_pin)
