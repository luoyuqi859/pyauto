#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Luo Yuqi
@File: ddd
@Created: 2023/2/23 17:42
"""

import time

import allure
import pytest

from conf import settings
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
def test_363660(d_obj:AndroidDevice):
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
        time.sleep(2)
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
        text = d_obj(resourceId=element.txt_dialog_message).text.replace("\n", "")
        assert text == 'Enter your Teen Driver PIN.Tap Retry, or visit a dealer to reset your PIN.', "assert text failed"


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
        text = d_obj(resourceId=element.txt_dialog_message).text.replace("\n", "")
        assert text == "Write down your new PIN. A forgotten PIN can only be reset at your dealer.To activate Teen Driver, you'll need to add the teen's key.", "assert text failed"
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
        text = d_obj(resourceId=element.txt_dialog_message).text.replace("\n", "")
        assert text == "Write down your new PIN. A forgotten PIN can only be reset at your dealer.To activate Teen Driver, you'll need to add the teen's key.", "assert text failed"
    with allure.step('24. Click OK in Teen Driver PIN set pop-up'):
        d_obj.click(xpath=element.ok)
        d_obj.assert_exist(xpath=element.add_or_remove_teen_driver_keys)
        d_obj.assert_exist(xpath=element.view_report_card)
        d_obj.assert_exist(xpath=element.teen_driver_settings)
        d_obj.assert_exist(xpath=element.change_pin)


# @allure.title("To verify seat belt restriction for both driver and front seat passenger with volume changes")
# def test_386643(d_obj: AndroidDevice):

@allure.title("To verify Add button in Add Teen Driver Key process")
def test_391799(d_obj: AndroidDevice):
    with allure.step('1. Open Settings Application'):
        d_obj.click(text="Settings")
    with allure.step('2. Send Teen Driver available signal TRUE - TeenDrvFtrAvl(1)'):
        GMS.sendSignal(Signal='TeenDrvFtrAvl', Value=1, Type='Signal', Mode='HS')
    with allure.step('3. Select Vehicle   '):
        d_obj.click(text="Vehicle")
    with allure.step('4. Select Teen Driver'):
        d_obj.click(text="Teen Driver")
    with allure.step('5. Click continue'):
        d_obj.click(text="Continue")
    with allure.step('6. Enter a 4 digit PIN'):
        d_obj.click(text="1").click(text="2").click(text="3").click(text="4")
    with allure.step('7. Click Enter  '):
        d_obj.click(resourceId=element.enter)
    with allure.step('8. Confirm your 4 digit PIN'):
        d_obj.click(text="1").click(text="2").click(text="3").click(text="4")
    with allure.step('9. Send TeenDrvRsp Signal ==> 2=Teen_PIN_Updated'):
        GMS.sendSignal(Signal='TeenDrvRsp', Value=2, Type='Signal', Mode='HS')
        d_obj.click(resourceId=element.enter)
    with allure.step('10. Click OK '):
        d_obj.click(xpath=element.ok)
        d_obj.assert_exist(xpath=element.add_or_remove_teen_driver_keys)
    with allure.step('11. Send TeenDrvReq Signal ==> 5=Check_for_Teen_Key'):
        GMS.sendSignal(Signal='TeenDrvReq', Value=5, Type='Signal', Mode='HS')
    with allure.step('12. Send TeenDrvRsp Signal ==> 8=Key_Detected_As_NOT_Teen_Key'):
        GMS.sendSignal(Signal='TeenDrvRsp', Value=8, Type='Signal', Mode='HS')
    with allure.step('13. Click Add/Remove Teen Driver Keys'):
        d_obj.click(xpath=element.add_or_remove_teen_driver_keys)
        d_obj.assert_exist(text="Add Teen Driver Key?")
        d_obj.assert_exist(text="Teen Driver restrictions will apply when this key is used.")
        d_obj.assert_exist(text="Add")
        d_obj.assert_exist(text="Cancel")
    with allure.step('14. Send TeenDrvReq Signal ==> 3 = Set Teen key'):
        GMS.sendSignal(Signal='TeenDrvReq', Value=3, Type='Signal', Mode='HS')
    with allure.step('15. Send TeenDrvRsp Signal ==> 4 = Teen Key Set Complete'):
        GMS.sendSignal(Signal='TeenDrvRsp', Value=4, Type='Signal', Mode='HS')
    with allure.step('16. Click Add Button'):
        d_obj.click(text="Add")
        time.sleep(1)
        text = d_obj(resourceId=element.txt_dialog_message).text.replace("\n", "")
        assert text == 'Whenever this key is used, Teen Driver restrictions will apply.You can now configure Teen Driver Settings.', "assert text fail"
    with allure.step('17. Click OK button'):
        d_obj.click(xpath=element.ok)
        d_obj.assert_exist(xpath=element.add_or_remove_teen_driver_keys)


@allure.title("To verify Remove button in Remove Teen Driver Key process")
def test_391802(d_obj: AndroidDevice):
    """
    step:
    1. Open Settings Application    2. Send Teen Driver available signal TRUE - TeenDrvFtrAvl(1)
    3. Select Vehicle      4. Select Teen Driver
    5. Select Continue    6. Enter a 4 digit PIN
    7. Click Enter
    8. Confirm your 4 digit PIN
    9. Send TeenDrvRsp Signal ==> 2=Teen_PIN_Updated
    10. Click OK
    11. Send TeenDrvReq Signal ==> 5=Check_for_Teen_Key
    12. Send TeenDrvRsp Signal ==> 7=Key_Detected_As_Teen_Key
    13. Click Add/Remove Teen Driver Keys
    14. Send TeenDrvReq Signal ==> 4 = Clear_Teen_Key
    15. Send TeenDrvRsp Signal ==> 5 = Teen Key Clear complete
    16. Click Remove Button
    17. Click OK button
    expect:
    10.Verify Add/Remove Teen Driver Keys exits in Teen Driver menu
     13.Remove Teen Driver Key page is displayed
        i. Verify Remove Teen Driver Key? text is displayed
        ii. Verify Teen Driver restrictions will apply when this key is used. Text is displayed
        iii. Verify Remove button is displayed  iv. Verify Cancel button is displayed
    16.Verify Key Removed page is displayed
        i. Verify Key Removed text is displayed
        ii. Verify This key will no longer have Teen Driver Restrictions. Text is displayed
        iii. Verify OK button is displayed
    17.Verify Add/Remove Teen Driver Keys in Teen Driver Menu is displayed
    """
    d_obj.click(text="Settings")
    GMS.sendSignal(Signal='TeenDrvFtrAvl', Value=1, Type='Signal', Mode='HS')
    d_obj.click(text="Vehicle")
    d_obj.click(text="Teen Driver")
    d_obj.click(text="Continue")
    d_obj.click(text="1").click(text="2").click(text="3").click(text="4")
    d_obj.click(resourceId=element.enter)
    d_obj.click(text="1").click(text="2").click(text="3").click(text="4")
    GMS.sendSignal(Signal='TeenDrvRsp', Value=2, Type='Signal', Mode='HS')
    d_obj.click(resourceId=element.enter)
    d_obj.click(xpath=element.ok)
    d_obj.assert_exist(xpath=element.add_or_remove_teen_driver_keys)
    GMS.sendSignal(Signal='TeenDrvReq', Value=5, Type='Signal', Mode='HS')
    GMS.sendSignal(Signal='TeenDrvRsp', Value=7, Type='Signal', Mode='HS')

    d_obj.click(xpath=element.add_or_remove_teen_driver_keys)
    d_obj.assert_exist(text="Remove Teen Driver Key?")
    d_obj.assert_exist(text="This key will no longer have Teen Driver restrictions.")
    d_obj.assert_exist(text="Remove")
    d_obj.assert_exist(text="Cancel")
    GMS.sendSignal(Signal='TeenDrvReq', Value=4, Type='Signal', Mode='HS')
    GMS.sendSignal(Signal='TeenDrvRsp', Value=5, Type='Signal', Mode='HS')
    d_obj.click(text="Remove")
    d_obj.assert_exist(text="Key Removed")
    d_obj.assert_exist(text="This key no longer has Teen Driver restrictions.")
    d_obj.click(xpath=element.ok)
    d_obj.assert_exist(xpath=element.add_or_remove_teen_driver_keys)


@allure.title("To verify Clear All Keys and PIN Success process")
def test_394754(d_obj: AndroidDevice):
    with allure.step('1. Open Settings Application'):
        d_obj.click(text="Settings")
    with allure.step('2. Send Teen Driver available signal TRUE - TeenDrvFtrAvl(1)'):
        GMS.sendSignal(Signal='TeenDrvFtrAvl', Value=1, Type='Signal', Mode='HS')
    with allure.step('3. Select Vehicle   '):
        d_obj.click(text="Vehicle")
    with allure.step('4. Select Teen Driver'):
        d_obj.click(text="Teen Driver")
    with allure.step('5. Click continue'):
        d_obj.click(text="Continue")
    with allure.step('6. Enter a 4 digit PIN'):
        d_obj.click(text="1").click(text="2").click(text="3").click(text="4")
    with allure.step('7. Click Enter  '):
        d_obj.click(resourceId=element.enter)
    with allure.step('8. Confirm your 4 digit PIN'):
        d_obj.click(text="1").click(text="2").click(text="3").click(text="4")
    with allure.step('9. Send TeenDrvRsp Signal ==> 2=Teen_PIN_Updated'):
        GMS.sendSignal(Signal='TeenDrvRsp', Value=2, Type='Signal', Mode='HS')
        d_obj.click(resourceId=element.enter)
    with allure.step('10. Click OK '):
        d_obj.click(xpath=element.ok)
        d_obj.assert_exist(xpath=element.add_or_remove_teen_driver_keys)
    with allure.step('11. Click Clear PIN and All Teen Driver Keys'):
        d_obj.swipe.down()
        d_obj.click(xpath=element.clear_pin_and_teen_driver_keys)
        d_obj.assert_exist(text="Clear PIN and all Teen Driver keys?")
        d_obj.assert_exist(text="This will clear your PIN and all Teen Driver keys.")
        d_obj.assert_exist(text="Clear")
        d_obj.assert_exist(text="Cancel")
    with allure.step('12. Click Cancel button'):
        d_obj.click(text="Cancel")
        d_obj.assert_exist(xpath=element.clear_pin_and_teen_driver_keys)
    with allure.step('13. Click Clear PIN and All Teen Driver Keys'):
        d_obj.click(xpath=element.clear_pin_and_teen_driver_keys)
    with allure.step('14. Send TeenDrvReq Signal ==> 6=Clear_Teen_Keys_and_PIN'):
        GMS.sendSignal(Signal='TeenDrvReq', Value=6, Type='Signal', Mode='HS')
    with allure.step('15. Send TeenDrvRsp Signal ==> 5=Teen_Key_Clear_Complete'):
        GMS.sendSignal(Signal='TeenDrvRsp', Value=5, Type='Signal', Mode='HS')
    with allure.step('16. Click Clear'):
        d_obj.click(text="Clear")
        d_obj.assert_exist(text="Success")
        d_obj.assert_exist(text="Your PIN and all Teen Driver keys were successfully cleared.")
        d_obj.assert_exist(xpath=element.ok)
    with allure.step('17. Click OK button'):
        d_obj.click(xpath=element.ok)
        d_obj.assert_exist(text="Teen Driver")


@allure.title("To verify elements in Teen Driver - Report card")
def test_396972(d_obj: AndroidDevice):
    with allure.step('1. Open Settings Application'):
        d_obj.click(text="Settings")
    with allure.step('2. Select Vehicle'):
        d_obj.click(text="Vehicle")
    with allure.step('3. Send Teen Driver available signal'):
        GMS.sendSignal(Signal='TeenDrvFtrAvl', Value=1, Type='Signal', Mode='HS')
    with allure.step('4. Send TEEN PIN STORED signal'):
        GMS.sendSignal(Signal='TnDrvPINStrd', Value=1, Type='Signal', Mode='HS')
    with allure.step('5. Select Teen Driver '):
        d_obj.click(text="Teen Driver")
    with allure.step('6. Enter your 4 digit Teen Driver PIN'):
        d_obj.click(text="1").click(text="2").click(text="3").click(text="4")
    with allure.step('7. Send TEEN PIN VERIFIED signal'):
        GMS.sendSignal(Signal='TeenDrvRsp', Value=1, Type='Signal', Mode='HS')
    with allure.step('8. Click Unlock'):
        d_obj.click(resourceId=element.enter)
        d_obj.assert_exist(xpath=element.view_report_card)
    with allure.step('9. Click View Report Card'):
        d_obj.click(xpath=element.view_report_card)
        d_obj.assert_exist(resourceId=element.report_card_reset_btn)
    with allure.step('10. Click back button in Report Card'):
        d_obj.click(resourceId=element.back)
        d_obj.assert_exist(xpath=element.view_report_card)
    with allure.step('11. Click View Report Card'):
        d_obj.click(xpath=element.view_report_card)
    with allure.step(
            '12. Send TRUE for below signal Teen Driver Report Card Available Display Data : Distance Driven - TDRCADD_DistDrvn'):
        GMS.sendSignal(Signal='TDRCADD_DistDrvn', Value=1, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='TnDrvDistDrvnRpt', Value=0, Type='Signal', Mode='HS')
        time.sleep(1)
        d_obj.assert_exist(text="Distance Driven: 0 km")
    with allure.step(
            '13. Send TRUE for below signal Teen Driver Report Card Available Display Data : Maximum Speed / TDRCADD_MaxSpd'):
        GMS.sendSignal(Signal='TDRCADD_MaxSpd', Value=1, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='TeenDrvMaxSpdRpt', Value=0, Type='Signal', Mode='HS')
        time.sleep(1)
        d_obj.assert_exist(text="Maximum Speed: 0.0 km/h")
    with allure.step(
            '14. Send TRUE for below signal Teen Driver Report Card Available Display Data : Overspeed Events / TDRCADD_OvSpdEvnt'):
        GMS.sendSignal(Signal='TDRCADD_OvSpdEvnt', Value=1, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='TnDrvOvSpdEvntsRpt', Value=0, Type='Signal', Mode='HS')
        time.sleep(1)
        d_obj.assert_exist(text="Overspeed Warnings: 0")
    with allure.step(
            '15. Send TRUE for below signal Teen Driver Report Card Available Display Data : Wide Open Throttle Events / TDRCADD_WOTEvnts'):
        GMS.sendSignal(Signal='TDRCADD_WOTEvnts', Value=1, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='TeenDrvWOTEvntsRpt', Value=0, Type='Signal', Mode='HS')
        time.sleep(1)
        d_obj.assert_exist(text="Wide Open Throttle: 0")
    with allure.step(
            '16. Send TRUE for below signal Teen Driver Report Card Available Display Data : Forward Collision Headway Alerts / TDRCADD_FCHdwyAlrt'):
        GMS.sendSignal(Signal='TDRCADD_FCHdwyAlrt', Value=1, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='TDFwdClnHdwyAlrtsRpt', Value=0, Type='Signal', Mode='HS')
        time.sleep(1)
        d_obj.assert_exist(text="Tailgating Alerts: 0")
    with allure.step(
            '17. Send TRUE for below signal Teen Driver Report Card Available Display Data : Forward Collision Mitigation Braking Events / TDRCADD_FCMBrEvts'):
        GMS.sendSignal(Signal='TDRCADD_FCMBrEvts', Value=1, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='TDFwdClnMtgnBrEvRpt', Value=0, Type='Signal', Mode='HS')
        time.sleep(1)
        d_obj.assert_exist(text="Automatic Emergency Braking: 0")
    with allure.step(
            '18. Send TRUE for below signal Teen Driver Report Card Available Display Data : Reverse Collision Mitigation Braking Events / TDRCADD_RCMBrEvts'):
        GMS.sendSignal(Signal='TDRCADD_RCMBrEvts', Value=1, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='TDRevClnMtgnBrEvRpt', Value=0, Type='Signal', Mode='HS')
        time.sleep(1)
        d_obj.assert_exist(text="Reverse Automatic Braking: 0")
    with allure.step(
            '19. Send TRUE for below signal Teen Driver Report Card Available Display Data : Forward Collision Imminent Alerts / TDRCADD_FCImntAlrts'):
        GMS.sendSignal(Signal='TDRCADD_FCImntAlrts', Value=1, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='TDFwdClnImntAlrtsRpt', Value=0, Type='Signal', Mode='HS')
        time.sleep(1)
        d_obj.assert_exist(text="Forward Collision Alerts: 0")
    with allure.step(
            '20. Send TRUE for below signal Teen Driver Report Card Available Display Data : Lane Departure Warning Events / TDRCADD_LDWEvnts'):
        GMS.sendSignal(Signal='TDRCADD_LDWEvnts', Value=1, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='TeenDrvLDWEvntsRpt', Value=0, Type='Signal', Mode='HS')
        time.sleep(1)
        d_obj.assert_exist(text="Lane Departure Warnings: 0")
    with allure.step(
            '21. Send TRUE for below signal Teen Driver Report Card Available Display Data : Traction Control Events / TDRCADD_TrCtrlEvnts'):
        GMS.sendSignal(Signal='TDRCADD_TrCtrlEvnts', Value=1, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='TnDrvTrCtrlEvntsRpt', Value=0, Type='Signal', Mode='HS')
        time.sleep(1)
        d_obj.assert_exist(text="Traction Control: 0")
    with allure.step(
            '22. Send TRUE for below signal Teen Driver Report Card Available Display Data : Stability Control Events / TDRCADD_StCtrlEvnts'):
        GMS.sendSignal(Signal='TDRCADD_StCtrlEvnts', Value=1, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='TnDrvStblCtrlEvntsRpt', Value=0, Type='Signal', Mode='HS')
        time.sleep(1)
        d_obj.swipe.down()
        d_obj.assert_exist(text="Stability Control: 0")
    with allure.step(
            '23. Send TRUE for below signal  Teen Driver Report Card Available Display Data : Antilock Braking System Active Events / TDRCADD_ABSAtvEvt'):
        GMS.sendSignal(Signal='TDRCADD_ABSAtvEvt', Value=1, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='TnDrvABSAtvEvntsRpt', Value=0, Type='Signal', Mode='HS')
        time.sleep(1)
        d_obj.assert_exist(text="Antilock Brake System Active: 0")
    with allure.step('24. Click back button'):
        d_obj.click(resourceId=element.back)
        d_obj.assert_exist(xpath=element.view_report_card)
    with allure.step('25. Send FALSE for below signals'):
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
    with allure.step('26. Click View Report Card'):
        d_obj.click(xpath=element.view_report_card)
        time.sleep(1)
        d_obj.assert_exist(resourceId=element.report_card_reset_btn)
        d_obj.assert_not_exist(text="Distance Driven: 0 km")
        d_obj.assert_not_exist(text="Maximum Speed: 0.0 km/h")
        d_obj.assert_not_exist(text="Overspeed Warnings: 0")
        d_obj.assert_not_exist(text="Wide Open Throttle: 0")
        d_obj.assert_not_exist(text="Forward Collision Alerts: 0")
        d_obj.assert_not_exist(text="Automatic Emergency Braking: 0")
        d_obj.assert_not_exist(text="Reverse Automatic Braking: 0")
        d_obj.assert_not_exist(text="Lane Departure Warnings: 0")
        d_obj.assert_not_exist(text="Traction Control: 0")
        d_obj.assert_not_exist(text="Stability Control: 0")
        d_obj.assert_not_exist(text="Antilock Brake System Active: 0")
        d_obj.assert_not_exist(text="Tailgating Alerts: 0")


@allure.title("To verify clear report card process")
@pytest.mark.usefixtures("report_card_close")
def test_397412(d_obj: AndroidDevice):
    with allure.step('1. Open Settings Application'):
        d_obj.click(text="Settings")
    with allure.step('2. Select Vehicle'):
        d_obj.click(text="Vehicle")
    with allure.step('3. Send Teen Driver available signal'):
        GMS.sendSignal(Signal='TeenDrvFtrAvl', Value=1, Type='Signal', Mode='HS')
    with allure.step('4. Select Teen Driver  '):
        d_obj.click(text="Teen Driver")
        d_obj.click(text="Continue")
    with allure.step('5. Enter your 4 digit Teen Driver PIN'):
        d_obj.click(text="1").click(text="2").click(text="3").click(text="4")
        d_obj.click(resourceId=element.enter)
    with allure.step('6. Confirm your 4 digit PIN   '):
        d_obj.click(text="1").click(text="2").click(text="3").click(text="4")
    with allure.step('7. Send TEEN PIN UPDATED signal'):
        GMS.sendSignal(Signal='TeenDrvRsp', Value=2, Type='Signal', Mode='HS')
    with allure.step('8. Click Set  '):
        d_obj.click(resourceId=element.enter)
        d_obj.click(xpath=element.ok)
        d_obj.assert_exist(xpath=element.view_report_card)
    with allure.step('9. Click View Report Card'):
        d_obj.click(xpath=element.view_report_card)
        d_obj.assert_exist(resourceId=element.report_card_reset_btn)
    with allure.step(
            '10. Send signal for OVERSPEED WARNINGS (VALUE = 1000) Teen Driver Report Card Available Display Data : Overspeed Events / TDRCADD_OvSpdEvnt Teen Driver OverSpeed Events Report / TnDrvOvSpdEvntsRpt'):
        GMS.sendSignal(Signal='TDRCADD_OvSpdEvnt', Value=1, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='TnDrvOvSpdEvntsRpt', Value=1000, Type='Signal', Mode='HS')
        time.sleep(1)
        d_obj.assert_exist(text="Overspeed Warnings: 1000")
    with allure.step(
            '11. Send signal for WIDE OPEN THROTTLE EVENTS (VALUE = 1000) Teen Driver Report Card Available Display Data : Wide Open Throttle Events / TDRCADD_WOTEvnts Teen Driver Wide Open Throttle Events Report / TeenDrvWOTEvntsRpt'):
        GMS.sendSignal(Signal='TDRCADD_WOTEvnts', Value=1, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='TeenDrvWOTEvntsRpt', Value=1000, Type='Signal', Mode='HS')
        time.sleep(1)
        d_obj.assert_exist(text="Wide Open Throttle: 1000")
    with allure.step(
            '12. Send signal for Forward Collision Alerts(VALUE = 1000) Teen Driver Forward Collision Imminent Alerts Report / TDFwdClnImntAlrtsRpt Teen Driver Report Card Available Display Data : Forward Collision Imminent Alerts / TDRCADD_FCImntAlrts'):
        GMS.sendSignal(Signal='TDRCADD_FCImntAlrts', Value=1, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='TDFwdClnImntAlrtsRpt', Value=1000, Type='Signal', Mode='HS')
        time.sleep(1)
        d_obj.assert_exist(text="Forward Collision Alerts: 1000")
    with allure.step(
            '13. Send signal for Forward Collision Avoidance Braking(VALUE = 1000) Teen Driver Report Card Available Display Data : Forward Collision Mitigation Braking Events / TDRCADD_FCMBrEvts Teen Driver Forward Collision Mitigation Braking Events Report / TDFwdClnMtgnBrEvRpt'):
        GMS.sendSignal(Signal='TDRCADD_FCMBrEvts', Value=1, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='TDFwdClnMtgnBrEvRpt', Value=1000, Type='Signal', Mode='HS')
        time.sleep(1)
        d_obj.assert_exist(text="Automatic Emergency Braking: 1000")
    with allure.step(
            '14. Send signal for Rear Collision Avoidance Braking(VALUE = 1000) Teen Driver Report Card Available Display Data : Reverse Collision Mitigation Braking Events / TDRCADD_RCMBrEvts Teen Driver Reverse Collision Mitigation Braking Events Report / TDRevClnMtgnBrEvRpt'):
        GMS.sendSignal(Signal='TDRCADD_RCMBrEvts', Value=1, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='TDRevClnMtgnBrEvRpt', Value=1000, Type='Signal', Mode='HS')
        time.sleep(1)
        d_obj.assert_exist(text="Reverse Automatic Braking: 1000")
    with allure.step(
            '15. Send signal for Lane Departure Warnings(VALUE=1000) Teen Driver Report Card Available Display Data : Lane Departure Warning Events / TDRCADD_LDWEvnts Teen Driver Lane Departure Warning Events Report / TeenDrvLDWEvntsRpt'):
        GMS.sendSignal(Signal='TDRCADD_LDWEvnts', Value=1, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='TeenDrvLDWEvntsRpt', Value=1000, Type='Signal', Mode='HS')
        time.sleep(1)
        d_obj.assert_exist(text="Lane Departure Warnings: 1000")
    with allure.step(
            '16. Send signal for Tailgating Alerts(VALUE=1000) Teen Driver Report Card Available Display Data : Forward Collision Headway Alerts / TDRCADD_FCHdwyAlrt Teen Driver Forward Collision Headway Alerts Report / TDFwdClnHdwyAlrtsRpt'):
        GMS.sendSignal(Signal='TDRCADD_FCHdwyAlrt', Value=1, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='TDFwdClnHdwyAlrtsRpt', Value=1000, Type='Signal', Mode='HS')
        time.sleep(1)
        d_obj.assert_exist(text="Tailgating Alerts: 1000")
    with allure.step(
            '17. Send signal for Stability Control(VALUE=1000) Teen Driver Report Card Available Display Data : Stability Control Events / TDRCADD_StCtrlEvnts   Teen Driver Stability Control Events Report / TnDrvStblCtrlEvntsRpt'):
        GMS.sendSignal(Signal='TDRCADD_StCtrlEvnts', Value=1, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='TnDrvStblCtrlEvntsRpt', Value=1000, Type='Signal', Mode='HS')
        time.sleep(1)
        d_obj.assert_exist(text="Stability Control: 1000")
    with allure.step(
            '18. Send signal for Antilock Brake System Active(VALUE= 1000) Teen Driver Report Card Available Display Data : Antilock Braking System Active Events / TDRCADD_ABSAtvEvt   Teen Driver Antilock Brake System Active Events Report / TnDrvABSAtvEvntsRpt'):
        GMS.sendSignal(Signal='TDRCADD_ABSAtvEvt', Value=1, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='TnDrvABSAtvEvntsRpt', Value=1000, Type='Signal', Mode='HS')
        time.sleep(1)
        d_obj.assert_exist(text="Antilock Brake System Active: 1000")
    with allure.step(
            '19. Send Signal for Traction Control(VALUE= 1000) Teen Driver Report Card Available Display Data : Traction Control Events / TDRCADD_TrCtrlEvnts Teen Driver Traction Control Events Report / TnDrvTrCtrlEvntsRpt'):
        GMS.sendSignal(Signal='TDRCADD_TrCtrlEvnts', Value=1, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='TnDrvTrCtrlEvntsRpt', Value=1000, Type='Signal', Mode='HS')
        time.sleep(1)
        d_obj.assert_exist(text="Traction Control: 1000")
    with allure.step(
            '20. Send Signal for Distance Driven(Value - 65535) Teen Driver Report Card Available Display Data : Distance Driven - TDRCADD_DistDrvn Teen Driver Distance Driven Report - TnDrvDistDrvnRpt'):
        GMS.sendSignal(Signal='TDRCADD_DistDrvn', Value=1, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='TnDrvDistDrvnRpt', Value=65535, Type='Signal', Mode='HS')
        time.sleep(1)
        d_obj.assert_exist(text="Distance Driven: 65,535 km")
    with allure.step(
            '21. Send Signal for Maximum Speed(Value 255.9) Teen Driver Report Card Available Display Data : Maximum Speed - TDRCADD_MaxSpd Teen Driver Maximum Speed Report - TeenDrvMaxSpdRpt'):
        GMS.sendSignal(Signal='TDRCADD_MaxSpd', Value=1, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='TeenDrvMaxSpdRpt', Value=255.9, Type='Signal', Mode='HS')
        time.sleep(1)
        d_obj.assert_exist(text="Maximum Speed: 255.9 km/h")
    with allure.step('22. Click Reset  '):
        d_obj.click(resourceId=element.report_card_reset_btn)
        d_obj.assert_exist(text="Clear Report Card?")
        d_obj.assert_exist(text="This will clear all Report Card values.")
        d_obj.assert_exist(text="Clear")
        d_obj.assert_exist(text="Cancel")
    with allure.step('23. Click Cancel'):
        d_obj.click(text="Cancel")
        d_obj.assert_exist(text="Report Card")
    with allure.step('24. Click Reset'):
        d_obj.click(resourceId=element.report_card_reset_btn)
        d_obj.assert_exist(text="Clear Report Card?")
    with allure.step('25.Send signal for all parameter to set value to 0'):
        GMS.sendSignal(Signal='TnDrvOvSpdEvntsRpt', Value=0, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='TeenDrvWOTEvntsRpt', Value=0, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='TDFwdClnImntAlrtsRpt', Value=0, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='TDFwdClnMtgnBrEvRpt', Value=0, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='TDRevClnMtgnBrEvRpt', Value=0, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='TeenDrvLDWEvntsRpt', Value=0, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='TDFwdClnHdwyAlrtsRpt', Value=0, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='TnDrvStblCtrlEvntsRpt', Value=0, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='TnDrvABSAtvEvntsRpt', Value=0, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='TnDrvTrCtrlEvntsRpt', Value=0, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='TnDrvDistDrvnRpt', Value=0, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='TeenDrvMaxSpdRpt', Value=0, Type='Signal', Mode='HS')
    with allure.step('26. Click Clear'):
        d_obj.click(text="Clear")
        d_obj.assert_exist(text="Distance Driven: 0 km")
        d_obj.assert_exist(text="Maximum Speed: 0.0 km/h")
        d_obj.assert_exist(text="Overspeed Warnings: 0")
        d_obj.assert_exist(text="Wide Open Throttle: 0")
        d_obj.assert_exist(text="Forward Collision Alerts: 0")
        d_obj.assert_exist(text="Automatic Emergency Braking: 0")
        d_obj.assert_exist(text="Reverse Automatic Braking: 0")
        d_obj.assert_exist(text="Lane Departure Warnings: 0")
        d_obj.assert_exist(text="Traction Control: 0")
        d_obj.swipe.down()
        d_obj.assert_exist(text="Stability Control: 0")
        d_obj.assert_exist(text="Antilock Brake System Active: 0")
        d_obj.assert_exist(text="Tailgating Alerts: 0")
        d_obj.swipe.up()
    with allure.step('27. Open Settings Application'):
        d_obj.press('home')
        d_obj.click(text="Settings")
    with allure.step('28. Select Vehicle '):
        d_obj.click(text="Vehicle")
    with allure.step('29. Send Teen Driver available signal'):
        GMS.sendSignal(Signal='TeenDrvFtrAvl', Value=1, Type='Signal', Mode='HS')
    with allure.step('30. Select Teen Driver '):
        d_obj.click(text="Teen Driver")
        d_obj.click(text="Continue")
    with allure.step('31. Enter your 4 digit Teen Driver PIN'):
        d_obj.click(text="1").click(text="2").click(text="3").click(text="4")
        d_obj.click(resourceId=element.enter)
    with allure.step('32. Confirm your 4 digit PIN'):
        d_obj.click(text="1").click(text="2").click(text="3").click(text="4")
    with allure.step('33. Send TEEN PIN UPDATED signal'):
        GMS.sendSignal(Signal='TeenDrvRsp', Value=2, Type='Signal', Mode='HS')
    with allure.step('34. Click Set'):
        d_obj.click(resourceId=element.enter)
        d_obj.click(xpath=element.ok)
    with allure.step('35. Click View Report Card'):
        d_obj.click(xpath=element.view_report_card)
        d_obj.assert_exist(text="Distance Driven: 0 km")
        d_obj.assert_exist(text="Maximum Speed: 0.0 km/h")
        d_obj.assert_exist(text="Overspeed Warnings: 0")
        d_obj.assert_exist(text="Wide Open Throttle: 0")
        d_obj.assert_exist(text="Forward Collision Alerts: 0")
        d_obj.assert_exist(text="Automatic Emergency Braking: 0")
        d_obj.assert_exist(text="Reverse Automatic Braking: 0")
        d_obj.assert_exist(text="Lane Departure Warnings: 0")
        d_obj.assert_exist(text="Traction Control: 0")
        d_obj.swipe.down()
        d_obj.assert_exist(text="Stability Control: 0")
        d_obj.assert_exist(text="Antilock Brake System Active: 0")
        d_obj.assert_exist(text="Tailgating Alerts: 0")
        d_obj.swipe.up()


@allure.title("To verify Key Not Detected Process from Add / Remove Teen Keys popup")
def test_397659(d_obj: AndroidDevice):
    with allure.step('1. Open Settings Application'):
        d_obj.click(text="Settings")
    with allure.step('2. Send Teen Driver available signal TRUE - TeenDrvFtrAvl(1)'):
        GMS.sendSignal(Signal='TeenDrvFtrAvl', Value=1, Type='Signal', Mode='HS')
    with allure.step('3. Select Vehicle'):
        d_obj.click(text="Vehicle")
    with allure.step('4. Select Teen Driver'):
        d_obj.click(text="Teen Driver")
    with allure.step('5. Click continue'):
        d_obj.click(text="Continue")
    with allure.step('6. Enter a 4 digit PIN'):
        d_obj.click(text="1").click(text="2").click(text="3").click(text="4")
    with allure.step('7. Click Enter  '):
        d_obj.click(resourceId=element.enter)
    with allure.step('8. Confirm your 4 digit PIN'):
        d_obj.click(text="1").click(text="2").click(text="3").click(text="4")
    with allure.step('9. Send TeenDrvRsp Signal ==> 2=Teen_PIN_Updated'):
        GMS.sendSignal(Signal='TeenDrvRsp', Value=2, Type='Signal', Mode='HS')
        d_obj.click(resourceId=element.enter)
    with allure.step('10. Click OK '):
        d_obj.click(xpath=element.ok)
        d_obj.assert_exist(xpath=element.add_or_remove_teen_driver_keys)
    with allure.step('11. Send TeenDrvReq Signal ==> 5=Check_for_Teen_Key'):
        GMS.sendSignal(Signal='TeenDrvReq', Value=5, Type='Signal', Mode='HS')
    with allure.step('12. Send TeenDrvRsp Signal ==> 6=Key_Not_Present'):
        GMS.sendSignal(Signal='TeenDrvRsp', Value=6, Type='Signal', Mode='HS')
    with allure.step('13. Click Add/Remove Teen Keys'):
        d_obj.click(xpath=element.add_or_remove_teen_driver_keys)
        d_obj.assert_exist(text="Add / Remove Teen Driver Keys")
        text = d_obj(resourceId=element.txt_dialog_message).text.replace("\n", "")
        assert text == 'Place the key you want to add or remove in the transmitter pocket.See your Owner’s Manual for details.', "assert text fail"
        d_obj.assert_exist(text="Continue")
        d_obj.assert_exist(text="Cancel")
    with allure.step('14. Send TeenDrvReq Signal ==> 5=Check_for_Teen_Key'):
        GMS.sendSignal(Signal='TeenDrvReq', Value=5, Type='Signal', Mode='HS')
    with allure.step('15. Send TeenDrvRsp Signal ==> 6=Key_Not_Present'):
        GMS.sendSignal(Signal='TeenDrvRsp', Value=6, Type='Signal', Mode='HS')
    with allure.step('16. Click Continue'):
        d_obj.click(text="Continue")
        d_obj.assert_exist(text="Key Not Detected")
        d_obj.assert_exist(text="Place a key in the transmitter pocket and tap Retry.")
        d_obj.assert_exist(text="Retry")
        d_obj.assert_exist(text="Cancel")
    with allure.step('17. Send TeenDrvReq Signal ==> 5=Check_for_Teen_Key'):
        GMS.sendSignal(Signal='TeenDrvReq', Value=5, Type='Signal', Mode='HS')
    with allure.step('18. Send TeenDrvRsp Signal ==> 6=Key_Not_Present'):
        GMS.sendSignal(Signal='TeenDrvRsp', Value=6, Type='Signal', Mode='HS')
    with allure.step('19. Click Retry'):
        d_obj.click(text="Retry")
        d_obj.assert_exist(text="Key Not Detected")
        d_obj.assert_exist(text="Place a key in the transmitter pocket and tap Retry.")
        d_obj.assert_exist(text="Retry")
        d_obj.assert_exist(text="Cancel")
    with allure.step('20. Click Cancel'):
        d_obj.click(text="Cancel")


@allure.title("To verify Key Not Detected in Add Teen Driver Key process")
def test_397660(d_obj: AndroidDevice):
    with allure.step('1. Open Settings Application'):
        d_obj.click(text="Settings")
    with allure.step('2. Send Teen Driver available signal TRUE - TeenDrvFtrAvl(1)'):
        GMS.sendSignal(Signal='TeenDrvFtrAvl', Value=1, Type='Signal', Mode='HS')
    with allure.step('3. Select Vehicle'):
        d_obj.click(text="Vehicle")
    with allure.step('4. Select Teen Driver'):
        d_obj.click(text="Teen Driver")
    with allure.step('5. Click continue'):
        d_obj.click(text="Continue")
    with allure.step('6. Enter a 4 digit PIN'):
        d_obj.click(text="1").click(text="2").click(text="3").click(text="4")
    with allure.step('7. Click Enter  '):
        d_obj.click(resourceId=element.enter)
    with allure.step('8. Confirm your 4 digit PIN'):
        d_obj.click(text="1").click(text="2").click(text="3").click(text="4")
    with allure.step('9. Send TeenDrvRsp Signal ==> 2=Teen_PIN_Updated'):
        GMS.sendSignal(Signal='TeenDrvRsp', Value=2, Type='Signal', Mode='HS')
        d_obj.click(resourceId=element.enter)
    with allure.step('10. Click OK '):
        d_obj.click(xpath=element.ok)
        d_obj.assert_exist(xpath=element.add_or_remove_teen_driver_keys)
    with allure.step('11. Send TeenDrvReq Signal ==> 5=Check_for_Teen_Key'):
        GMS.sendSignal(Signal='TeenDrvReq', Value=5, Type='Signal', Mode='HS')
    with allure.step('12. Send TeenDrvRsp Signal ==> 8=Key_Detected_As_NOT_Teen_Key'):
        GMS.sendSignal(Signal='TeenDrvRsp', Value=8, Type='Signal', Mode='HS')
    with allure.step('13. Click Add/Remove Teen Keys'):
        d_obj.click(xpath=element.add_or_remove_teen_driver_keys)
        d_obj.assert_exist(text="Add Teen Driver Key?")
        d_obj.assert_exist(text="Teen Driver restrictions will apply when this key is used.")
        d_obj.assert_exist(text="Add")
        d_obj.assert_exist(text="Cancel")
    with allure.step('14. Send TeenDrvReq Signal ==> 3=Set_Teen_Key'):
        GMS.sendSignal(Signal='TeenDrvReq', Value=3, Type='Signal', Mode='HS')
    with allure.step('15. Send TeenDrvRsp Signal ==> 6=Key_Not_Present'):
        GMS.sendSignal(Signal='TeenDrvRsp', Value=6, Type='Signal', Mode='HS')
    with allure.step('16. Click Add Button'):
        d_obj.click(text="Add")
        time.sleep(10)
        d_obj.assert_exist(text="Key Not Detected")
        d_obj.assert_exist(text="Place a key in the transmitter pocket and tap Retry.")
        d_obj.assert_exist(text="Retry")
        d_obj.assert_exist(text="Cancel")
    with allure.step('17. Click Cancel Button'):
        d_obj.click(text="Cancel")
        d_obj.assert_exist(xpath=element.add_or_remove_teen_driver_keys)


#
# @allure.title("To verify Driver Workload and Ignition Restrictions in IGNITION STATE")
# def test_399687(d_obj: AndroidDevice):
#     with allure.step('1. Open Settings Application'):
#         d_obj.click(text="Settings")
#     with allure.step('2. Send Teen Driver available signal TRUE - TeenDrvFtrAvl(1)'):
#         GMS.sendSignal(Signal='TeenDrvFtrAvl', Value=1, Type='Signal', Mode='HS')
#     with allure.step('3. Select Vehicle'):
#         d_obj.click(text="Vehicle")
#     with allure.step('4. Select Teen Driver'):
#         d_obj.click(text="Teen Driver")
#     with allure.step('5. Click continue'):
#         d_obj.click(text="Continue")
#     with allure.step('6. Enter a 4 digit PIN'):
#         d_obj.click(text="1").click(text="2").click(text="3").click(text="4")
#     with allure.step('7. Click Enter  '):
#         d_obj.click(resourceId=element.enter)
#     with allure.step('8. Confirm your 4 digit PIN'):
#         d_obj.click(text="1").click(text="2").click(text="3").click(text="4")
#
#     with allure.step('9. Send TeenDrvRsp Signal ==> 2=Teen_PIN_Updated'):
#         GMS.sendSignal(Signal='TeenDrvRsp', Value=2, Type='Signal', Mode='HS')
#         d_obj.click(resourceId=element.enter)
#     with allure.step('10. Click OK '):
#         d_obj.click(xpath=element.ok)
#         d_obj.assert_exist(xpath=element.add_or_remove_teen_driver_keys)
#     with allure.step('11. Send TeenDrvReq Signal ==> 5=Check_for_Teen_Key'):
#         GMS.sendSignal(Signal='TeenDrvReq', Value=5, Type='Signal', Mode='HS')
#     with allure.step('12. Send TeenDrvRsp Signal ==> 8=Key_Detected_As_NOT_Teen_Key'):
#         GMS.sendSignal(Signal='TeenDrvRsp', Value=8, Type='Signal', Mode='HS')
#     with allure.step('13. Click Add/Remove Teen Keys'):
#         d_obj.click(xpath=element.add_or_remove_teen_driver_keys)
#         d_obj.assert_exist(text="Add Teen Driver Key?")
#         d_obj.assert_exist(text="Teen Driver restrictions will apply when this key is used.")
#         d_obj.assert_exist(text="Add")
#         d_obj.assert_exist(text="Cancel")
#     with allure.step('14. Send TeenDrvReq Signal ==> 3=Set_Teen_Key'):
#         GMS.sendSignal(Signal='TeenDrvReq', Value=3, Type='Signal', Mode='HS')
#     with allure.step('15. Send TeenDrvRsp Signal ==> 6=Key_Not_Present'):
#         GMS.sendSignal(Signal='TeenDrvRsp', Value=6, Type='Signal', Mode='HS')
#     with allure.step('16. Click Add Button'):
#         d_obj.click(text="Add")
#         time.sleep(2)
#         d_obj.assert_exist(text="Key Not Detected")
#         d_obj.assert_exist(text="Place a key in the transmitter pocket and tap Retry.")
#         d_obj.assert_exist(text="Retry")
#         d_obj.assert_exist(text="Cancel")
#     with allure.step('17. Click Cancel Button'):
#         d_obj.click(text="Cancel")
#         d_obj.assert_exist(xpath=element.add_or_remove_teen_driver_keys)

@allure.title(
    "To verify Driver Workload and Ignition Restrictions in UxR is NO_SETUP - Teen Driver Settings from Teen Driver app")
def test_399718(d_obj: AndroidDevice):
    with allure.step('1. Open Settings Application'):
        d_obj.click(text="Settings")
    with allure.step('2. Send Teen Driver available signal TRUE - TeenDrvFtrAvl(1)'):
        GMS.sendSignal(Signal='TeenDrvFtrAvl', Value=1, Type='Signal', Mode='HS')
    with allure.step('3. Select Vehicle'):
        d_obj.click(text="Vehicle")
    with allure.step('4. Select Teen Driver'):
        d_obj.click(text="Teen Driver")
        d_obj.click(text="Continue")
    with allure.step('5. Enter a 4 digit PIN '):
        d_obj.click(text="1").click(text="2").click(text="3").click(text="4")
    with allure.step('6. Click Enter'):
        d_obj.click(resourceId=element.enter)
    with allure.step('7. Confirm your 4 digit PIN'):
        d_obj.click(text="1").click(text="2").click(text="3").click(text="4")
    with allure.step('8. Send TeenDrvRsp Signal ==> 2=Teen_PIN_Updated'):
        GMS.sendSignal(Signal='TeenDrvRsp', Value=2, Type='Signal', Mode='HS')
        d_obj.click(resourceId=element.enter)
    with allure.step('9. Click OK'):
        d_obj.assert_exist(text="Teen Driver PIN Set")
        d_obj.click(xpath=element.ok)
    with allure.step(
            '10. Send below signals AutoTransGrDispdVal set to 10 = D6 AutoTransGrDispdVal_Inv set to False VSADP_VehSpdAvgDrvnAuth set to 10.0 VSADP_VehSpdAvgDrvnAuth_Inv set to False'):
        GMS.sendSignal(Signal='TEGP_TrnsShftLvrPstnAuth', Value=7, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='TEGP_TrnsShftLvrPstnAuth_Inv', Value=0, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='VSADP_VehSpdAvgDrvnAuth', Value=10.0, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='VSADP_VehSpdAvgDrvnAuth_Inv', Value=0, Type='Signal', Mode='HS')
        time.sleep(10)
        d_obj.assert_exist(text="Vehicle")
        e = d_obj(resourceId='com.gm.hmi.settings:id/car_ui_list_item_text_container')[1]
        e.click()
        time.sleep(1)
        el = d_obj(resourceId='com.gm.hmi.settings:id/rv_vehicle_sub_menu').child(className="android.view.ViewGroup",
                                                                                  index=3)
        el.screenshot(settings.report_path / 'menu_unavailable_while_driving.png')
        time.sleep(1)
        text_list = d_obj.ocr.image_to_text(settings.report_path / 'menu_unavailable_while_driving.png')
        assert text_list[0] == "Menu unavailable while driving", "menu assert failed"
    with allure.step('11. Wait 30 seconds'):
        time.sleep(30)
    with allure.step('12. Click Teen Driver menu'):
        e = d_obj(resourceId='com.gm.hmi.settings:id/car_ui_list_item_text_container')[1]
        e.click()
        time.sleep(1)
        el = d_obj(resourceId='com.gm.hmi.settings:id/rv_vehicle_sub_menu').child(className="android.view.ViewGroup",
                                                                                  index=3)
        el.screenshot(settings.report_path / 'menu_unavailable_while_driving.png')
        time.sleep(1)
        text_list = d_obj.ocr.image_to_text(settings.report_path / 'menu_unavailable_while_driving.png')
        assert text_list[0] == "Menu unavailable while driving", "menu assert failed"
    with allure.step('13. wait 30 seconds'):
        time.sleep(30)
    with allure.step(
            '14. Send below signal to Reset VSADP_VehSpdAvgDrvnAuth set to 0.0 VSADP_VehSpdAvgDrvnAuth_Inv set to False AutoTransGrDispdVal set to 1 = P AutoTransGrDispdVal_Inv set to False'):
        GMS.sendSignal(Signal='TEGP_TrnsShftLvrPstnAuth', Value=1, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='TEGP_TrnsShftLvrPstnAuth_Inv', Value=0, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='VSADP_VehSpdAvgDrvnAuth', Value=0.0, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='VSADP_VehSpdAvgDrvnAuth_Inv', Value=0, Type='Signal', Mode='HS')
    with allure.step('15. Select Teen Driver'):
        d_obj.click(text="Teen Driver")
        d_obj.assert_exist(text="Teen Driver")


@allure.title(
    "To verify Driver Workload and Ignition Restrictions in No_VIDEO - from Key Not Detected process")
def test_399762(d_obj: AndroidDevice):
    with allure.step('1. Open Settings Application'):
        d_obj.click(text="Settings")
    with allure.step('2. Send Teen Driver available signal TRUE - TeenDrvFtrAvl(1)'):
        GMS.sendSignal(Signal='TeenDrvFtrAvl', Value=1, Type='Signal', Mode='HS')
    with allure.step('3. Select Vehicle'):
        d_obj.click(text="Vehicle")
    with allure.step('4. Select Teen Driver'):
        d_obj.click(text="Teen Driver")
    with allure.step('5. Select Continue'):
        d_obj.click(text="Continue")
    with allure.step('6. Enter a 4 digit PIN '):
        d_obj.click(text="1").click(text="2").click(text="3").click(text="4")
    with allure.step('7. Click Enter'):
        d_obj.click(resourceId=element.enter)
    with allure.step('8. Confirm your 4 digit PIN'):
        d_obj.click(text="1").click(text="2").click(text="3").click(text="4")
    with allure.step('9. Send TeenDrvRsp Signal ==> 2=Teen_PIN_Updated'):
        GMS.sendSignal(Signal='TeenDrvRsp', Value=2, Type='Signal', Mode='HS')
        d_obj.click(resourceId=element.enter)
    with allure.step('10. Click OK'):
        d_obj.click(xpath=element.ok)
        d_obj.assert_exist(xpath=element.add_or_remove_teen_driver_keys)
    with allure.step('11. Send TeenDrvReq Signal ==> 5=Check_for_Teen_Key'):
        GMS.sendSignal(Signal='TeenDrvReq', Value=5, Type='Signal', Mode='HS')
    with allure.step('12. Send TeenDrvRsp Signal ==> 7=Key_Detected_As_Teen_Key'):
        GMS.sendSignal(Signal='TeenDrvRsp', Value=7, Type='Signal', Mode='HS')
    with allure.step('13. Click Add/Remove Teen Keys'):
        d_obj.click(xpath=element.add_or_remove_teen_driver_keys)
        d_obj.assert_exist(text="Remove Teen Driver Key?")
    with allure.step('14. Send TeenDrvReq Signal ==> 4=Clear_Teen_Key'):
        GMS.sendSignal(Signal='TeenDrvReq', Value=4, Type='Signal', Mode='HS')
    with allure.step('15. Send TeenDrvRsp Signal ==> 6=Key_Not_Present'):
        GMS.sendSignal(Signal='TeenDrvRsp', Value=6, Type='Signal', Mode='HS')
    with allure.step('16. Click Remove Button'):
        d_obj.click(text="Remove")
        time.sleep(10)
        d_obj.assert_exist(text="Key Not Detected")
    with allure.step(
            '17. Send below signals AutoTransGrDispdVal set to 3 = N AutoTransGrDispdVal_Inv set to False VSADP_VehSpdAvgDrvnAuth set to 0.0 VSADP_VehSpdAvgDrvnAuth_Inv set to False'):
        GMS.sendSignal(Signal='TEGP_TrnsShftLvrPstnAuth', Value=3, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='TEGP_TrnsShftLvrPstnAuth_Inv', Value=0, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='VSADP_VehSpdAvgDrvnAuth', Value=10.0, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='VSADP_VehSpdAvgDrvnAuth_Inv', Value=0, Type='Signal', Mode='HS')
        time.sleep(10)
        d_obj.assert_exist(text="Vehicle")
        e = d_obj(resourceId='com.gm.hmi.settings:id/car_ui_list_item_text_container')[1]
        e.click()
        time.sleep(1)
        el = d_obj(resourceId='com.gm.hmi.settings:id/rv_vehicle_sub_menu').child(className="android.view.ViewGroup",
                                                                                  index=3)
        el.screenshot(settings.report_path / 'menu_unavailable_while_driving.png')
        time.sleep(1)
        text_list = d_obj.ocr.image_to_text(settings.report_path / 'menu_unavailable_while_driving.png')
        assert text_list[0] == "Menu unavailable while driving", "menu assert failed"

    with allure.step('18. Wait 30 seconds'):
        time.sleep(30)
    with allure.step(
            '19. Send below signal to Reset VSADP_VehSpdAvgDrvnAuth set to 0.0 VSADP_VehSpdAvgDrvnAuth_Inv set to False AutoTransGrDispdVal set to 1 = P AutoTransGrDispdVal_Inv set to False'):
        GMS.sendSignal(Signal='TEGP_TrnsShftLvrPstnAuth', Value=1, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='TEGP_TrnsShftLvrPstnAuth_Inv', Value=0, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='VSADP_VehSpdAvgDrvnAuth', Value=0.0, Type='Signal', Mode='HS')
        GMS.sendSignal(Signal='VSADP_VehSpdAvgDrvnAuth_Inv', Value=0, Type='Signal', Mode='HS')
        d_obj.click(text="Teen Driver")
        d_obj.click(text="Continue")
        d_obj.click(text="1").click(text="2").click(text="3").click(text="4")
        d_obj.click(resourceId=element.enter)
        d_obj.click(text="1").click(text="2").click(text="3").click(text="4")
        GMS.sendSignal(Signal='TeenDrvRsp', Value=2, Type='Signal', Mode='HS')
        d_obj.click(resourceId=element.enter)
        d_obj.click(xpath=element.ok)
        d_obj.assert_exist(xpath=element.add_or_remove_teen_driver_keys)


@allure.title(
    "To verify Speed Warning Switch On and Off in Teen Driver Settings Screen")
def test_413361(d_obj: AndroidDevice):
    with allure.step('1. Navigate to Teen Driver Menu'):

        d_obj.click(text="Settings").click(text="Vehicle").click(text="Teen Driver")
        d_obj.click(text="Continue")
        d_obj.click(text="1").click(text="2").click(text="3").click(text="4")
        d_obj.click(resourceId=element.enter)
        d_obj.click(text="1").click(text="2").click(text="3").click(text="4")
        GMS.sendSignal(Signal='TeenDrvRsp', Value=2, Type='Signal', Mode='HS')
        d_obj.click(resourceId=element.enter)
        d_obj.click(xpath=element.ok)
    with allure.step(
            '2. Send    TeenDriverOverspeedWarningCustomizationSettingAvailable / TnDrvOvSpdWrnCstStAvl signal - True'):
        GMS.sendSignal(Signal='TnDrvOvSpdWrnCstStAvl', Value=1, Type='Signal', Mode='HS')
    with allure.step(
            '3. Send TeenDriverOverspeedWarningCustomizationCurrentSettingValue / TDOSWCCSV_CrSetVal Signal - OFF'):
        GMS.sendSignal(Signal='TDOSWCCSV_CrSetVal', Value=1, Type='Signal', Mode='HS')
    with allure.step('5.Click Teen driver settings option'):
        d_obj.click(text="Teen Driver Settings")
        assert d_obj(text="Speed Warning").offset(x=0.58).checked == False, "assert switch off failed"
    with allure.step('6. Switch ON Speed Warning in Teen Driver Settings Screen'):
        d_obj(text="Speed Warning").offset(x=0.58).click()
    with allure.step(
            '7.Send TeenDriverOverspeedWarningCustomizationCurrentSettingValue / TDOSWCCSV_CrSetVal Signal - ON'):
        GMS.sendSignal(Signal='TDOSWCCSV_CrSetVal', Value=2, Type='Signal', Mode='HS')
        assert d_obj(text="Speed Warning").offset(x=0.58).checked == True, "assert switch on failed"
    with allure.step('8. Click Speed Warning'):
        d_obj(text="Speed Warning").click()
        assert d_obj(text="Speed Warning").offset(x=0.4).checked == True, "assert switch on failed"
    with allure.step('9. Click back'):
        d_obj.click(resourceId=element.back)
    with allure.step(
            '10. Send TeenDriverOverspeedWarningCustomizationCurrentSettingValue / TDOSWCCSV_CrSetVal Signal - OFF'):
        GMS.sendSignal(Signal='TDOSWCCSV_CrSetVal', Value=1, Type='Signal', Mode='HS')
    with allure.step('11. Switch OFF Speed Warning in Teen Driver Settings Screen'):
        # 点击返回键后自带关闭开关
        if d_obj(text="Speed Warning").offset(x=0.4).checked:
            d_obj(text="Speed Warning").offset(x=0.58).click()
        assert d_obj(text="Speed Warning").offset(x=0.58).checked == False, "assert switch off failed"
    with allure.step('12.Click Speed Warning'):
        d_obj(text="Speed Warning").click()
        assert d_obj(text="Speed Warning").offset(x=0.4).checked == False, "assert switch off failed"


@allure.title(
    "To verify Increment and Decrement  button in Speed Warning Tertiary Screen when Speed Warning is Switched ON (MPH)")
def test_413364(d_obj: AndroidDevice):
    with allure.step('1. Navigate to Teen Driver Menu'):
        d_obj.click(text="Settings").click(text="Vehicle").click(text="Teen Driver")
        d_obj.click(text="Continue")
        d_obj.click(text="1").click(text="2").click(text="3").click(text="4")
        d_obj.click(resourceId=element.enter)
        d_obj.click(text="1").click(text="2").click(text="3").click(text="4")
        GMS.sendSignal(Signal='TeenDrvRsp', Value=2, Type='Signal', Mode='HS')
        d_obj.click(resourceId=element.enter)
        d_obj.click(xpath=element.ok)
    with allure.step(
            '2. Send TeenDriverOverspeedWarningCustomizationSettingAvailable / TnDrvOvSpdWrnCstStAvl   signal - True'):
        GMS.sendSignal(Signal='TnDrvOvSpdWrnCstStAvl', Value=1, Type='Signal', Mode='HS')
    with allure.step(
            '3. Send      TeenDriverOverspeedWarningCustomizationCurrentSettingValue / TDOSWCCSV_CrSetVal Signal - ON'):
        GMS.sendSignal(Signal='TDOSWCCSV_CrSetVal', Value=2, Type='Signal', Mode='HS')
    with allure.step(
            '4. SendDisplay Measurement System Extended / DispMeasSysExtnd - 1 (for miles per hour)'):
        GMS.sendSignal(Signal='DispMeasSysExtnd', Value=1, Type='Signal', Mode='HS')
    with allure.step('5.Click Teen driver settings optionDispMeasSysExtnd'):
        d_obj.click(text="Teen Driver Settings")


@allure.title(
    "To verify Switching on and Switching off Audio Volume Limit option  in Teen Driver Menu")
def test_423214(d_obj: AndroidDevice):
    with allure.step('1. Open Settings Application '):
        d_obj.click(text="Settings")
    with allure.step('2. Select Vehicle'):
        d_obj.click(text="Vehicle")
    with allure.step('3. Send Teen Driver available signal'):
        GMS.sendSignal(Signal='TeenDrvFtrAvl', Value=1, Type='Signal', Mode='HS')
    with allure.step('4. Select Teen Driver'):
        d_obj.click(text="Teen Driver")
        d_obj.click(text="Continue")
    with allure.step('5. Enter your 4 digit Teen Driver PIN'):
        d_obj.click(text="1").click(text="2").click(text="3").click(text="4")
        d_obj.click(resourceId=element.enter)
    with allure.step('6. Confirm your 4 digit Teen Driver PIN'):
        d_obj.click(text="1").click(text="2").click(text="3").click(text="4")
    with allure.step('7. Send TEEN PIN UPDATED signal'):
        GMS.sendSignal(Signal='TeenDrvRsp', Value=2, Type='Signal', Mode='HS')
    with allure.step('8. Click Unlock'):
        d_obj.click(resourceId=element.enter)
        d_obj.click(xpath=element.ok)
    with allure.step('9. Click Audio Volume Limit option'):
        d_obj.click(text="Teen Driver Settings")
        assert d_obj(text="Audio Volume Limit").offset(x=0.58).checked == True, "assert switch on failed"
        d_obj.click(text="Audio Volume Limit")
        assert d_obj(text="Audio Volume Limit").offset(x=0.4).checked == True, "assert switch on failed"
    with allure.step('10. Click Back'):
        d_obj.click(resourceId=element.back)
    with allure.step('11. Switch OFF the Audio Volume Limit option in Teen Driver Menu'):
        d_obj(text="Audio Volume Limit").offset(x=0.58).click()
        assert d_obj(text="Audio Volume Limit").offset(x=0.58).checked == False, "assert switch off failed"
    with allure.step('12. Click Audio Volume Limit option'):
        d_obj.click(text="Audio Volume Limit")
        assert d_obj(text="Audio Volume Limit").offset(x=0.4).checked == False, "assert switch off failed"
        assert d_obj(resourceId=element.btn_volume_increase).enabled == False, "assert btn increase off failed"
        assert d_obj(resourceId=element.btn_volume_decrease).enabled == False, "assert btn decrease off failed"
    with allure.step('13. Click Back'):
        d_obj.click(resourceId=element.back)
    with allure.step('14. Switch ON the Audio Volume Limit option in Teen Driver Menu'):
        d_obj(text="Audio Volume Limit").offset(x=0.58).click()
        assert d_obj(text="Audio Volume Limit").offset(x=0.58).checked == True, "assert switch on failed"
    with allure.step('15. Click Audio Volume Limit option'):
        d_obj.click(text="Audio Volume Limit")
        assert d_obj(text="Audio Volume Limit").offset(x=0.4).checked == True, "assert switch on failed"
        assert d_obj(resourceId=element.btn_volume_increase).enabled == True, "assert btn increase on failed"
        assert d_obj(resourceId=element.btn_volume_decrease).enabled == True, "assert btn decrease on failed"
    with allure.step('16. Switch OFF the Audio Volume Limit option in Tertiary Screen'):
        d_obj(text="Audio Volume Limit").offset(x=0.4).click()
        assert d_obj(text="Audio Volume Limit").offset(x=0.4).checked == False, "assert switch off failed"
        assert d_obj(resourceId=element.btn_volume_increase).enabled == False, "assert btn increase off failed"
        assert d_obj(resourceId=element.btn_volume_decrease).enabled == False, "assert btn decrease off failed"
    with allure.step('17. Click Back'):
        d_obj.click(resourceId=element.back)
    with allure.step('18. Click Audio Volume Limit option'):
        d_obj.click(text="Audio Volume Limit")
        assert d_obj(text="Audio Volume Limit").offset(x=0.4).checked == False, "assert switch off failed"
        assert d_obj(resourceId=element.btn_volume_increase).enabled == False, "assert btn increase off failed"
        assert d_obj(resourceId=element.btn_volume_decrease).enabled == False, "assert btn decrease off failed"
    with allure.step('19. Switch ON the Audio Volume Limit option in Tertiary Screen'):
        d_obj(text="Audio Volume Limit").offset(x=0.4).click()
        assert d_obj(text="Audio Volume Limit").offset(x=0.4).checked == True, "assert switch on failed"
        assert d_obj(resourceId=element.btn_volume_increase).enabled == True, "assert btn increase on failed"
        assert d_obj(resourceId=element.btn_volume_decrease).enabled == True, "assert btn decrease on failed"
    with allure.step('20. Click Back'):
        d_obj.click(resourceId=element.back)
        assert d_obj(text="Audio Volume Limit").offset(x=0.58).checked == True, "assert switch on failed"


@allure.title(
    "To verify the increase and decrease volume button in Audio Limit Tertiary Screen")
def test_423215(d_obj: AndroidDevice):
    with allure.step('1. Open Settings Application '):
        d_obj.click(text="Settings")
    with allure.step('2. Select Vehicle'):
        d_obj.click(text="Vehicle")
    with allure.step('3. Send Teen Driver available signal'):
        GMS.sendSignal(Signal='TeenDrvFtrAvl', Value=1, Type='Signal', Mode='HS')
    with allure.step('4. Select Teen Driver'):
        d_obj.click(text="Teen Driver")
        d_obj.click(text="Continue")
    with allure.step('5. Enter your 4 digit Teen Driver PIN'):
        d_obj.click(text="1").click(text="2").click(text="3").click(text="4")
        d_obj.click(resourceId=element.enter)
    with allure.step('6. Confirm your 4 digit Teen Driver PIN'):
        d_obj.click(text="1").click(text="2").click(text="3").click(text="4")
    with allure.step('7. Send TEEN PIN UPDATED signal'):
        GMS.sendSignal(Signal='TeenDrvRsp', Value=2, Type='Signal', Mode='HS')
    with allure.step('8. Click Unlock'):
        d_obj.click(resourceId=element.enter)
        d_obj.click(xpath=element.ok)

    with allure.step('9. Click Audio Volume Limit option'):
        d_obj.click(text="Teen Driver Settings")
        assert d_obj(text="Audio Volume Limit").offset(x=0.58).checked == True, "assert switch on failed"
        d_obj.click(text="Audio Volume Limit")
        assert d_obj(resourceId=element.btn_volume_increase).enabled == True, "assert btn increase on failed"
        assert d_obj(resourceId=element.btn_volume_decrease).enabled == True, "assert btn decrease on failed"

    with allure.step('10. Click the Volume Increase button once'):
        d_obj(resourceId=element.btn_volume_increase).click()
        assert d_obj(resourceId=element.btn_volume_increase).enabled == True, "assert btn increase on failed"
        assert d_obj(resourceId=element.btn_volume_decrease).enabled == True, "assert btn decrease on failed"
    with allure.step('11. Click Volume Decrease button once'):
        d_obj(resourceId=element.btn_volume_decrease).click()
        assert d_obj(resourceId=element.btn_volume_increase).enabled == True, "assert btn increase on failed"
        assert d_obj(resourceId=element.btn_volume_decrease).enabled == True, "assert btn decrease on failed"
    with allure.step('12. Click the Volume Increase button till max volume is reached'):
        while d_obj(resourceId=element.btn_volume_increase).enabled:
            d_obj(resourceId=element.btn_volume_increase).click()
        assert d_obj(resourceId=element.btn_volume_increase).enabled == False, "assert btn increase off failed"
        assert d_obj(resourceId=element.btn_volume_decrease).enabled == True, "assert btn decrease on failed"
    with allure.step('13. Click Volume Decrease button once'):
        d_obj(resourceId=element.btn_volume_decrease).click()
        assert d_obj(resourceId=element.btn_volume_increase).enabled == True, "assert btn increase on failed"
        assert d_obj(resourceId=element.btn_volume_decrease).enabled == True, "assert btn decrease on failed"
        # 执行10次减小防止影响其他用例
        d_obj(resourceId=element.btn_volume_decrease).click(times=10)


# @allure.title(
#     "To verify Teen Driver volume snack bar with default Audio Volume Limit setting in Teen Driver")
# @pytest.mark.usefixtures("driver_seat_belts_are_bucked_up")
# def test_424369(d_obj: AndroidDevice):
#     with allure.step('1. Send Teen Driver Active Authenticated / TDAP_TeenDrvrActvAuth Signal'):
#         GMS.sendSignal(Signal='TDAP_TeenDrvrActvAuth', Value=1, Type='Signal', Mode='HS')
#     with allure.step('2. Increase the volume by 1 level'):
#         d_obj.adb_fp.adb.shell("input keyevent 25")
#     with allure.step('3. Decrease the volume by 1 level'):
#         d_obj.adb_fp.adb.shell("input keyevent 24")
#     with allure.step('4. Decrease the volume till volume level reach 0'):
#         d_obj.click(text="Teen Driver")
#         d_obj.click(text="Continue")

@allure.title(
    'To verify status of radio button in "Speed Limiter" tertiary screen is matched with the "Speed Limiter" switch under Teen Driver Settings')
def test_427292(d_obj: AndroidDevice):
    """
    step:
    1. Navigate to Teen driver
    2. Send TeenDriverSpeedLimitCustomizationSettingAvailable / TnDrvSpdLmtCstStAvl signal - True
    3. Send TeenDriverSpeedLimitCustomizationCurrentSettingValue / TDSLCCSV_CrSetVal - OFF
    4. Click Teen driver settings option
    5. Click the Speed Limiter option
    6. Turn ON the Speed Limiter tertiary option
    7. Send TeenDriverSpeedLimitCustomizationCurrentSettingValue / TDSLCCSV_CrSetVal - ON
    8. Navigate back to Teen Driver Settings
    9. Click the Speed Limiter option
    expect:
    5. Speed Limiter tertiary option is TURNED OFF
    8. Speed Limiter Switch is TURNED ON
    9. Speed Limiter tertiary option is TURNED ON
    """
    d_obj.click(text="Settings").click(text="Vehicle").click(text="Teen Driver")
    d_obj.click(text="Continue")
    d_obj.click(text="1").click(text="2").click(text="3").click(text="4")
    d_obj.click(resourceId=element.enter)
    d_obj.click(text="1").click(text="2").click(text="3").click(text="4")
    GMS.sendSignal(Signal='TeenDrvRsp', Value=2, Type='Signal', Mode='HS')
    d_obj.click(resourceId=element.enter)
    d_obj.click(xpath=element.ok)
    GMS.sendSignal(Signal='TnDrvSpdLmtCstStAvl', Value=1, Type='Signal', Mode='HS')
    GMS.sendSignal(Signal='TDSLCCSV_CrSetVal', Value=1, Type='Signal', Mode='HS')
    d_obj.click(text="Teen Driver Settings")
    d_obj.click(text="Speed Limiter").click()
    assert d_obj(text="Off").offset(x=0.12).checked == True, "assert switch off failed"
    assert d_obj(text="On").offset(x=0.12).checked == False, "assert switch on failed"
    GMS.sendSignal(Signal='TDSLCCSV_CrSetVal', Value=2, Type='Signal', Mode='HS')
    d_obj.click(resourceId=element.back)
    assert d_obj(text="Speed Limiter").offset(x=0.58).checked == True, "assert switch on failed"
    d_obj.click(text="Speed Limiter").click()
    assert d_obj(text="Off").offset(x=0.12).checked == False, "assert switch off failed"
    assert d_obj(text="On").offset(x=0.12).checked == True, "assert switch on failed"
