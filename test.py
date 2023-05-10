#!/usr/bin/python

# Copyright (C) 2021 General Motors
#

"""Tool to test boot-up timing."""

import argparse
import collections
import datetime
import math
import operator
import os
import re
import select
import subprocess
import sys
import time
import serial

import xlsxwriter, openpyxl
from pathlib import Path
from openpyxl import load_workbook

from datetime import datetime, date

DBG = False

PERFORMANCE_TEST_START_TIME = None
BUILD_FINGERPRINT = "build_fingerprint"

app_list = ["com.android.car.dialer/.ui.TelecomActivity",
            "com.google.android.apps.maps/com.google.android.maps.MapsActivity",
            "com.android.car.media/.MediaActivity",
            "com.gm.hmi.hvac/com.gm.hmi.hvac.ui.activities.LauncherActivity",
            "com.gm.hmi.trailer/com.gm.hmi.trailer.ui.activities.TrailerHomeActivityFull",
            "com.gm.gmmedia/com.gm.gmmedia.launcher.AppGridActivity",
            "com.gm.hmi.connection/com.gm.hmi.connection.ui.activities.WifiHotspotActivity",
            "com.gm.gmmedia/.dispatcher.MediaDispatcherActivity",
            "com.gm.hmi.radio/com.gm.hmi.radio.ui.activities.RadioNowPlayingViewPagerActivity",
            "com.android.car.dialer/.ui.TelecomActivity",
            "com.gm.homescreen/.app.HomeScreenActivity",
            "com.android.car.settings/.Settings_Launcher_Homepage",
            "com.gm.hmi.connection/.ui.activities.WifiHotspotActivity",
            "com.gm.hmi.settings/.ui.activities.VehicleSettingsActivity",
            "com.gm.hmi.onstarui/.ui.activities.ServicesNoActivity",
            "com.gm.hmi.onstar/.ui.activities.OnStarTBTActivity",
            "com.gm.teenmode/.presentation.pincheck.PinCheckActivity",
            "com.gm.passengermodeapp/.ActivityBlockingActivity",
            "com.gm.hmi.energy/.ui.activity.MainLauncherActivity",
            "com.gm.hmi.trailer/.ui.activities.TrailerHomeActivityFull",
            "com.gm.hmi.hvac/.ui.activities.LauncherActivity",
            "com.gm.hmi.seatstatus/.ui.activities.SeatStatusPaneActivity",
            "com.gm.offroad/.presentation.main.MainActivity",
            "com.android.car.settings/.Settings_Launcher_Homepage",
            "com.gm.drivemode/.presentation.main.MainActivity",
            ]


def init_arguments():
    parser = argparse.ArgumentParser(description='Measures boot time based on logs in a folder.')
    parser.add_argument('-s', '--serial_port', dest='serial_port_name',
                        default=None, required=False,
                        help='Name of the serial port device to connect to CSM SOC. ')

    parser.add_argument('-l', '--loop', dest='test_cycles',
                        default=1,
                        help='How many test cycle to run.')

    parser.add_argument('-p', '--log_path', dest='log_path',
                        default=".",
                        help='file path to store the generated test report.')

    parser.add_argument('-r', '--remark', dest='remark',
                        default="",
                        help='special comments for this test or build used.')

    return parser.parse_args()


class Logger(object):
    def __init__(self, log_path):
        self.terminal = sys.stdout
        self.log = open(log_path, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        # this flush method is needed for python 3 compatibility.
        # this handles the flush command by doing nothing.
        # you might want to specify some extra behavior here.
        self.terminal.flush()
        pass


class Parser:
    """文本解析"""

    def __init__(self):

        self.line_patterns = None

    def set_patterns(self, pattern_def):
        self.line_patterns = None
        self.line_patterns = {key: re.compile(pattern)
                              for key, pattern in pattern_def.items()}

    def parse_line(self, line):
        for event_key, line_pattern in self.line_patterns.items():
            m = line_pattern.search(line)
            if m:
                return event_key, m
        return None, None


class TestCase:

    def __init__(self, serial_port, args):
        print("Initialize test case ... Done")

        self.parser = Parser()
        self.serial_port = serial_port

        # how many test cycles for boot time measurement
        self.total_test_cycles = int(args.test_cycles)

        # remark of the test
        self.test_remark = args.remark

        # collection of boot time measurement records
        self.test_records = collections.OrderedDict()

        # indicate if a retry of the same test case is required.
        self.retry_required = False

        self.test_start_time = datetime.now()
        self.test_stop_time = None

        print("\nTest started at: " + str(self.test_start_time))
        print("Total test cycle planned: " + str(self.total_test_cycles))

        if self.test_remark != "":
            print("Test Remark: " + self.test_remark)
        print("")

        self.csm_version = None

        global PERFORMANCE_TEST_START_TIME
        PERFORMANCE_TEST_START_TIME = self.test_start_time

    def send_cmd_wait_line(self, cmd, output, operation_text, wait_sec, step_sec):
        if not self.serial_port.is_open:
            print("ERROR: The serial port is already closed.")
            return False

        self.serial_port.timeout = 0.2
        self.serial_port.write_timeout = 5

        sin = ""

        if not (operation_text == None or operation_text == ""):
            sys.stdout.write(operation_text)
            sys.stdout.flush()

        if not (cmd == None or cmd == ""):
            cmd += "\n"
            self.serial_port.write(cmd.encode('ascii'))
            self.serial_port.flush()

        expected_output = False
        loop_count = 0

        while not expected_output:
            if not (output == None or output == ""):
                sin = self.serial_port.readline().strip().decode('ascii')

            if sin == "":
                if not (operation_text == None or operation_text == ""):
                    sys.stdout.write(".")
                    sys.stdout.flush()

                loop_count += step_sec
                if loop_count > wait_sec:
                    if output == None or output == "":
                        expected_output = True
                    break
                else:
                    time.sleep(step_sec)
            elif sin == output:
                expected_output = True
            else:
                pass

        if expected_output:
            if not (operation_text == None or operation_text == ""):
                sys.stdout.write("...Done\n")
                sys.stdout.flush()

        else:
            if not (operation_text == None or operation_text == ""):
                sys.stdout.write("...FAILED\n")
                sys.stdout.flush()

        return expected_output

    def reboot_csm(self):
        # send reboot command
        cmd_result = self.send_cmd_wait_line("reboot -p", "Done", "Reboot CSM ", 5, 1)
        if not cmd_result:
            print("ERROR: Failed to reboot CSM.")
            return False

            # wait for shutdown start
        cmd_result = self.send_cmd_wait_line("", "GHS: Initiating VIP reset", "Wait for CSM shutdown ", 30, 1)
        # cmd_result = self.send_cmd_wait_line("", "console:/ $", "Wait for CSM shutdown ", 30, 1)

        if not cmd_result:
            print("ERROR: Failed to reboot CSM.")
            return False

        return True

    def set_adb(self):
        # set adb
        cmd_result = self.send_cmd_wait_line("setprop sys.usb.config adb", "console:/ #", "Enable ADB ", 2, 0.5)
        if not cmd_result:
            print("WARNING: Failed to enable ADB-1.")
            return True

        cmd_result = self.send_cmd_wait_line("echo \"device\" > /sys/class/usb_role/intel_xhci_usb_sw-role-switch/role",
                                             "console:/ #", "", 2, 0.5)
        if not cmd_result:
            print("WARNING: Failed to enable ADB-2.")
            return True

        self.serial_port.reset_input_buffer()

        return True

    def clear_log(self):
        # clear gmlogger logs
        cmd_result = self.send_cmd_wait_line("gmlc -c", "console:/ #", "Clear GMLogger logs ", 20, 1)
        if not cmd_result:
            print("ERROR: Failed to clear GMLogger logs.")
            return False

        cmd_result = self.send_cmd_wait_line("sync", "console:/ #", "", 10, 1)
        if not cmd_result:
            print("ERROR: Failed to clear GMLogger logs.")
            return False

        time.sleep(5)

        return True

    def set_root_dir(self):
        # set to root dir
        cmd_result = self.send_cmd_wait_line("cd /", "", "Set to root dir ", 1, 0.5)
        if not cmd_result:
            print("ERROR: Failed to set to root dir.")
            return False

        self.serial_port.reset_input_buffer()

        return True

    def get_build_fingerprint(self):
        # get build fingerprint
        self.serial_port.reset_input_buffer()

        print("Read CSM Software Version...")
        self.serial_port.write("getprop | grep ro.build.fingerprint\n".encode('ascii'))
        self.serial_port.flush()

        time.sleep(0.2)

        global BUILD_FINGERPRINT
        op_completed = False
        op_reponse_wait_count = 5

        while (not op_completed) and (op_reponse_wait_count > 0):
            sin = self.serial_port.readline().strip().decode('ascii')

            if sin == "getprop | grep ro.build.fingerprint":
                continue

            elif sin[:22] == "[ro.build.fingerprint]":
                op_completed = True
                self.csm_version = sin[25:len(sin) - 1]

            else:
                op_reponse_wait_count -= 1
                time.sleep(0.5)

        if not op_completed:
            print("WARNING: Failed to read CSM build fingerprint.")
            self.csm_version = ""

        else:
            print("Read CSM Software Version: " + self.csm_version)
            BUILD_FINGERPRINT = self.csm_version

        return True

    def set_root(self):
        # set to root
        cmd_result = self.send_cmd_wait_line("su", "console:/ #", "Set as root ", 5, 1)
        if not cmd_result:
            print("ERROR: Failed to set to root.")
            return False

        return True

    def send_ctrlc(self):
        # send ctrl-c
        cmd_result = self.send_cmd_wait_line("\x03", "console:/ #", "", 10, 1)
        if not cmd_result:
            print("ERROR: Failed to send Ctrl-C.")
            return False

        return True

    def get_application_clod_boot_time(self, test_record, activity):
        if not self.serial_port.is_open:
            print("ERROR: The serial port is already closed.")
            return False

        # makes ure we are root
        if not self.set_root():
            return False

        line_patterns_def = {"total_time": "TotalTime:\s(?P<total_time>\d+)",
                             "wait_time": "WaitTime:\s(?P<wait_time>\d+)"}

        self.parser.set_patterns(line_patterns_def)

        op_completed = False
        op_reponse_start = False
        op_reponse_wait_count = 0
        op_start_time = datetime.now()

        sys.stdout.write("Send am command ")
        sys.stdout.flush()

        command = "am start -W -n " + activity + "\n"
        self.serial_port.reset_input_buffer()
        self.serial_port.write(command.encode('ascii'))
        self.serial_port.flush()

        print("get_application_clod_boot_time")
        data_value = []
        while not op_completed:
            sin = self.serial_port.readline().strip().decode('ascii')
            print(sin)
            if sin == "":
                if op_reponse_start:
                    sin = self.serial_port.readline().strip().decode('ascii')

                    if sin == "":
                        # can not find home resume log
                        print("ERROR: Cannot find required info.")
                        self.retry_required = True

                        return False
                else:
                    # still waiting for response
                    sys.stdout.write(".")
                    sys.stdout.flush()

                    op_reponse_wait_count += 1

                    if op_reponse_wait_count > 20:
                        # can not find home resume log
                        print("ERROR: Cannot find get command response.")
                        self.retry_required = True

                        return False

                    time.sleep(1)

            elif sin == "console:/ #":
                # command output is completed
                op_completed = True

            else:
                key, m = self.parser.parse_line(sin)
                if not m:
                    # print("\tDEBUG: Cannot match:\t" + sin)
                    pass
                else:
                    m = m.groupdict()
                    for data_key in m.keys():
                        print(data_key)
                        # print("\tDEBUG: application_clod_boot_total_time data_key:\t" + data_key)
                        if "total_time" == data_key:
                            total_time = int(m[data_key].replace(",", ""))
                            # print("\tDEBUG: total_time data_value:\t" + str(total_time))
                            data_value.append(total_time)
                        if "wait_time" == data_key:
                            wait_time = int(m[data_key].replace(",", ""))
                            # print("\tDEBUG: wait_time data_value:\t" + str(wait_time))
                            data_value.append(wait_time)
                    # print(data_value)
        test_total_time = data_value
        print(test_total_time)
        return True, test_total_time

    def get_data_partition_size(self, test_record):
        if not self.serial_port.is_open:
            print("ERROR: The serial port is already closed.")
            return False

        # makes ure we are root
        if not self.set_root():
            return False

        # 400%cpu  65%user  18%nice  88%sys 227%idle   0%iow   0%irq   2%sirq   0%host
        line_patterns_def = {"data_idle_cpu": "sys\s+(?P<data_idle_cpu>\d+)\%\s*idle"}

        self.parser.set_patterns(line_patterns_def)

        op_completed = False
        op_reponse_start = False
        op_reponse_wait_count = 0
        op_start_time = datetime.now()

        sys.stdout.write("Send df command ")
        sys.stdout.flush()

        self.serial_port.reset_input_buffer()
        self.serial_port.write("df -h\n".encode('ascii'))
        self.serial_port.flush()

        print("get_data_partition_size")
        while not op_completed:
            sin = self.serial_port.readline().strip().decode('ascii')
            print(sin)

            if sin == "":
                if op_reponse_start:
                    sin = self.serial_port.readline().strip().decode('ascii')

                    if sin == "":
                        # can not find home resume log
                        print("ERROR: Cannot find required info.")
                        self.retry_required = True

                        return False
                else:
                    # still waiting for response
                    sys.stdout.write(".")
                    sys.stdout.flush()

                    op_reponse_wait_count += 1

                    if op_reponse_wait_count > 20:
                        # can not find home resume log
                        print("ERROR: Cannot find get command response.")
                        self.retry_required = True

                        return False

                    time.sleep(1)

            elif sin == "console:/ #":
                # command output is completed
                op_completed = True

            else:
                key, m = self.parser.parse_line(sin)
                if not m:
                    # print("\tDEBUG: Cannot match:\t" + sin)
                    pass
                else:
                    m = m.groupdict()

                    for data_key in m.keys():
                        data_value = int(m[data_key].replace(",", ""))
                        test_record[data_key] = data_value
                        print("\tDEBUG: matched:\t\t" + sin)
                        print("\tDEBUG: partition size data added: "
                              + str(data_key) + ":" + str(data_value))
        return True

    def get_idle_mem(self, test_record):
        if not self.serial_port.is_open:
            print("ERROR: The serial port is already closed.")
            return False

        self.serial_port.reset_input_buffer()

        # makes ure we are root
        if not self.set_root():
            return False

        line_patterns_def = {"ev_idle_mem_total": "Total RAM:\s(?P<data_idle_mem_total>[0-9\,]+)K",
                             "ev_idle_mem_free": "Free RAM:\s+(?P<data_idle_mem_free_with_cache>[0-9\,]+)K\s\(\s+[0-9\,]+K\scached pss\s\+\s+[0-9\,]+K\scached kernel\s\+\s+(?P<data_idle_mem_free_actual>[0-9\,]+)K\sfree\)",
                             "ev_idle_mem_used": "Used RAM:\s(?P<data_idle_mem_used>[0-9\,]+)K"}

        self.parser.set_patterns(line_patterns_def)

        op_completed = False
        op_reponse_start = False
        op_reponse_wait_count = 0

        sys.stdout.write("Send meminfo command ")
        sys.stdout.flush()

        # get bootup.log
        self.serial_port.write("cat /proc/uptime; dumpsys meminfo\n".encode('ascii'))
        self.serial_port.flush()

        while not op_completed:

            sin = self.serial_port.readline().strip().decode('ascii')

            if sin == "":
                if op_reponse_start:
                    sin = self.serial_port.readline().strip().decode('ascii')

                    if sin == "":
                        # can not find home resume log
                        print("ERROR: Cannot find required memory info.")
                        self.retry_required = True

                        return False
                else:
                    # still waiting for response
                    sys.stdout.write(".")
                    sys.stdout.flush()

                    op_reponse_wait_count += 1

                    if op_reponse_wait_count > 20:
                        # can not find home resume log
                        print("ERROR: Cannot find get command response.")
                        self.retry_required = True

                        return False

                    time.sleep(1)

            elif sin == "console:/ #":
                # command output is completed
                op_completed = True

            elif sin == "Applications Memory Usage (in Kilobytes):":
                # output started
                op_reponse_start = True

                sys.stdout.write("...\n")
                sys.stdout.flush()

            else:
                key, m = self.parser.parse_line(sin)
                if not m:
                    if op_reponse_start:
                        # print("\tDEBUG: Cannot match:\t" + sin)
                        pass
                else:
                    m = m.groupdict()

                    for data_key in m.keys():
                        data_value = int(m[data_key].replace(",", ""))
                        test_record[data_key] = data_value
                        print("\tDEBUG: matched:\t\t" + sin)
                        print("\tDEBUG: idle mem data added: " + str(data_key) + ":" + str(data_value))
        return True

    def get_idle_cpu(self, test_record):
        if not self.serial_port.is_open:
            print("ERROR: The serial port is already closed.")
            return False

        # makes ure we are root
        if not self.set_root():
            return False

        # 400%cpu  65%user  18%nice  88%sys 227%idle   0%iow   0%irq   2%sirq   0%host
        line_patterns_def = {"data_idle_cpu": "sys\s+(?P<data_idle_cpu>\d+)\%\s*idle"}

        self.parser.set_patterns(line_patterns_def)

        op_completed = False
        op_reponse_start = False
        op_response_wait_count = 0
        op_start_time = datetime.now()

        cpu_data_record = collections.OrderedDict()

        self.serial_port.reset_input_buffer()

        print("Send CPU data command ...Done")

        # get bootup.log
        self.serial_port.write("cat /proc/uptime; top -b -m 10 -n 30 -d 1\n".encode('ascii'))
        self.serial_port.flush()

        while not op_completed:

            sin = self.serial_port.readline().strip().decode('ascii')

            if sin == "":
                op_test_duration = datetime.now() - op_start_time
                if op_test_duration.total_seconds() > 180:
                    print("ERROR: Failed to read CPU usage data.")
                    self.retry_required = True
                    return False

                else:
                    continue

            elif sin == "console:/ #":
                # command output is completed
                op_completed = True

            else:
                key, m = self.parser.parse_line(sin)
                if not m:
                    # print("\tDEBUG: Cannot match:\t" + sin)
                    pass
                else:
                    if op_reponse_start == False:
                        # we skip the first output as it is usually inconsistant
                        op_reponse_start = True
                        time.sleep(2)

                        continue

                    print("\t" + str(datetime.now()) + " DEBUG: matched:\t" + sin)

                    cpu_data_set = sin.split(" ")
                    cpu_data_str = ""

                    for cpu_data_str in cpu_data_set:
                        if cpu_data_str.strip() == "":
                            continue
                        else:
                            tmp_str_set = cpu_data_str.split("%")
                            if len(tmp_str_set) > 2:
                                continue
                            key = tmp_str_set[1]
                            cpu_data = int(tmp_str_set[0])

                            if key == "cpu":
                                continue
                            else:
                                key = "data_cpu_" + key

                            if key in cpu_data_record.keys():
                                cpu_data_record[key] += [cpu_data]
                            else:
                                cpu_data_record[key] = [cpu_data]

                            print("\tDEBUG: CPU data found: " + key + " : " + str(cpu_data))

                    # output from top is set to every 5s
                    # time.sleep(1)

        if len(cpu_data_record) > 0:
            for key in cpu_data_record.keys():
                cpu_date_set = cpu_data_record[key]
                avg_cpu_data = int(sum(cpu_date_set) / len(cpu_date_set))

                print("\tDEBUG: idle CPU data add to record (average of " + str(
                    len(cpu_date_set)) + " data) : " + key + ":" + str(avg_cpu_data))
                test_record[key] = avg_cpu_data

        # dump cpuinfo as well for reference
        self.serial_port.reset_input_buffer()

        self.serial_port.write("dumpsys cpuinfo\n".encode('ascii'))
        self.serial_port.flush()

        op_completed = False
        op_reponse_wait_count = 10

        while (not op_completed) and (op_reponse_wait_count > 0):
            sin = self.serial_port.readline().strip().decode('ascii')

            if sin == "console:/ #":
                op_completed = True
                continue

            elif sin == "":
                op_reponse_wait_count -= 1
                continue

            else:
                print("\tDEBUG: CPUINFO: " + sin)

        return True

    def run_test(self):

        print("Start running test case ... ")
        if not self.set_root_dir():
            return False

        # makes ure we are root
        if not self.set_root():
            return False

        # makes ure we are root
        if not self.get_build_fingerprint():
            return False

        retry_count = 0

        loop_count = 1

        while loop_count <= self.total_test_cycles:
            print("\nRunning test loop: ---------------- " + str(loop_count) + " ----------------")

            test_record = collections.OrderedDict()
            print("看看", test_record)
            self.retry_required = False

            self.serial_port.reset_output_buffer()
            self.serial_port.reset_input_buffer()

            # clean up existing logs
            # if not self.clear_log():
            #    return False

            # reboot CSM
            if not self.reboot_csm():
                return False

            cmd_result = self.send_cmd_wait_line("", "", "Wait for 60s ", 60, 3)

            self.serial_port.reset_input_buffer()

            # makes ure we are root
            if not self.set_root():
                return False

            # makes ure we are root
            if not self.set_adb():
                return False

            # df -h
            if not self.retry_required and not self.get_data_partition_size(test_record):
                if self.retry_required:
                    retry_count += 1
                    if retry_count > 10:
                        print("ERROR: Failed to collect idle memory data.")
                        print("ERROR: Maxim retry count reached!")
                        return False
                    else:
                        print("WARNING: Failed to collect idle memory data, retrying...")
                else:
                    print("ERROR: Failed to collect idle memory data.")
                    return False

            # collect idle memory data
            # dumpsys meminfo
            if not self.retry_required and not self.get_idle_mem(test_record):
                if self.retry_required:
                    retry_count += 1
                    if retry_count > 10:
                        print("ERROR: Failed to collect idle memory data.")
                        print("ERROR: Maxim retry count reached!")
                        return False
                    else:
                        print("WARNING: Failed to collect idle memory data, retrying...")
                else:
                    print("ERROR: Failed to collect idle memory data.")
                    return False

            # collect idle cpu data
            if not self.retry_required and not self.get_idle_cpu(test_record):
                if self.retry_required:
                    retry_count += 1
                    if retry_count > 3:
                        print("ERROR: Failed to collect idle CPU data.")
                        print("ERROR: Maxim retry count reached!")
                        return False
                    else:
                        print("WARNING: Failed to collect idle CPU data, retrying...")
                else:
                    print("ERROR: Failed to get idle CPU data.")
                    return False

            # app cold boot time
            all_app_boot_test_total = []
            if len(app_list):
                for activity in app_list:
                    if not self.retry_required:
                        success, test_total = self.get_application_clod_boot_time(test_record, activity)
                        if not success:
                            if self.retry_required:
                                retry_count += 1
                                if retry_count > 3:
                                    print("ERROR: Failed to collect %s boot time.", activity)
                                    print("ERROR: Maxim retry count reached!")
                                    return False
                                else:
                                    print("WARNING: Failed to collect %s boot time, retrying...", activity)
                            else:
                                print("ERROR: Failed to get idle %s boot time.", activity)
                                return False
                    time.sleep(5)
                    all_app_boot_test_total.append(test_total)
                # print(all_app_boot_test_total)
            # TODO: add other boot test here

            test_record["app_clod_boot_time"] = all_app_boot_test_total
            # print("test_record: " + str(test_record))

            # Save test data
            if not self.retry_required:
                # print(test_record)
                print("---------------end---------------- " + str(loop_count))
                self.test_records["Test-" + str(loop_count)] = test_record
                for key, value in test_record.items():
                    print("\t" + key + ": " + str(value))

            if not self.retry_required:
                loop_count += 1

        print("All test cycle completed.")

        self.test_stop_time = datetime.now()
        print("Test Completed on: " + str(self.test_stop_time))

        return True

    def calculate_stdev(self, data_set):
        if len(data_set) == 0:
            return 0

        average = sum(data_set) / len(data_set)
        s = 0
        for i in data_set:
            s += (i - average) ** 2

        return math.sqrt(s / len(data_set))

    def calculate_boot_time(self, data_set):
        if len(data_set) == 0:
            return 0
        round = self.total_test_cycles
        app_numbers = len(app_list)

        print("calculate_boot_time: " + str(data_set) + ", data len: " + str(len(data_set))
              + ", app_numbers: " + str(app_numbers) + ", round: " + str(round))
        try:
            for i in range(app_numbers):
                total_time = 0
                for j in range(round):
                    total_time += data_set[j][i][0]
                    j += 1
                average = total_time / round
                print(app_list[i] + ": " + str(average))
                i += 1
        except Exception as e:
            print(e)
            print("请检查app_list的packages中是否在测试系统中存在")
            exit(0)

    def print_report(self):
        print("\n")

        if self.test_stop_time is None:
            self.test_stop_time = datetime.now()

        if len(self.test_records) == 0:
            print("ERROR: no boot records to print.")
            return False

        keys = self.test_records["Test-1"].keys()
        average = collections.OrderedDict()
        stdev = collections.OrderedDict()

        for key in keys:
            average[key] = []

        out_line = "test-cycle"
        for key in keys:
            out_line += "|" + key
        print(out_line)

        all_app_clod_boot_time = []

        for test_cycle, test_record in self.test_records.items():
            out_line = test_cycle
            for key in keys:
                # print("key: " + key)
                if key in test_record.keys():
                    out_line += "|" + str(test_record[key])
                    if key[:11] == "application":
                        average[key] += test_record[key]
                    elif "app_clod_boot_time" == key:
                        data = test_record[key]
                        all_app_clod_boot_time.append(data)
                    else:
                        average[key] += [int(test_record[key])]
                    if key[:8] == "data_cpu":
                        out_line += "%"
                else:
                    out_line += "|" + "NA"
            print(out_line)

        out_line = "average"
        for key in keys:
            if len(average[key]) > 0:
                out_line += "|" + str(sum(average[key]) / len(average[key]))
                if key[:8] == "data_cpu":
                    out_line += "%"
                if "app_clod_boot_time" == key:
                    pass
                else:
                    stdev[key] = self.calculate_stdev(average[key])
            else:
                out_line += "|" + "NA"
        print(out_line)

        out_line = "stdev"
        for key in keys:
            if key in stdev.keys():
                out_line += "|" + str('%.1f' % stdev[key])
                if key[:8] == "data_cpu":
                    out_line += "%"

            else:
                out_line += "|" + "NA"

        print(out_line)

        self.calculate_boot_time(all_app_clod_boot_time)

        print("\n\n")

        print("===== Summary =====")
        print("Test Start Time: " + str(self.test_start_time))
        print("Test Stop Time: " + str(self.test_stop_time))
        print("Test Duration: " + str(self.test_stop_time - self.test_start_time))
        print("CSM Version: " + self.csm_version)
        print("Expected Test Cycles: " + str(self.total_test_cycles))
        print("Actual Test Cycles: " + str(len(self.test_records)))
        print("Test Remark: " + self.test_remark)
        print("-------------------")

        for key in keys:
            if len(average[key]) > 0:
                avg = sum(average[key]) / len(average[key])
                if avg > 0:
                    stdev_percent = 100 * stdev[key] / avg
                else:
                    stdev_percent = 0

                out_line = key + " : " + str(avg)
                if key[:8] == "data_cpu":
                    out_line += "%"
                out_line += " (stdev:" + str('%.1f' % stdev[key])
                if key[:8] == "data_cpu":
                    out_line += "%"
                out_line += ", ~" + str('%.2f' % stdev_percent) + "%)"
                print(out_line)

            else:
                print(key + ":" + "NA")

        print("===================")


def main():
    serial_port_name = "COM5"
    args = init_arguments()

    if not args.log_path.endswith('/'):
        args.log_path = args.log_path + '/'
    report_file_path = args.log_path + "dexopt-test.log"
    print("temp logpath: ", report_file_path)

    if os.path.isfile(report_file_path):
        # log file already exist.
        print(report_file_path + " exist, remove it.")
        os.remove(report_file_path)

    # initialize serial port
    ser = None  # 先给 ser 变量赋一个默认值
    try:
        ser = serial.Serial(serial_port_name, 115200, timeout=0.5)
    except serial.SerialException as ex:
        print(ex)
        print(
            "failed to open serial port " + serial_port_name + ". Please make sure no other program is using it!")
        exit(0)

    sys_stdout = sys.stdout
    sys.stdout = Logger(report_file_path)

    print("======================")

    if ser is None or not ser.is_open:  # 在接下来的代码中判断 ser 变量是否为 None
        print("ERROR: Failed to open serial port: " + serial_port_name)
        if ser is not None:
            ser.close()
        exit(0)

    print("清空串口缓冲区")
    ser.reset_input_buffer()
    ser.reset_output_buffer()

    testcast = TestCase(ser, args)

    if not testcast.run_test():
        print("ERROR: Failed to complete test case. ")

    testcast.print_report()

    if ser.is_open:
        ser.close()

    # reset the stdout back
    sys.stdout = sys_stdout

    if BUILD_FINGERPRINT != "build_fingerprint" and PERFORMANCE_TEST_START_TIME != None:
        test_time = str(PERFORMANCE_TEST_START_TIME.date()) + "_" + str(PERFORMANCE_TEST_START_TIME.time())[:8]
        test_time = test_time.replace("-", "_")
        test_time = test_time.replace(":", "_")

        pos = BUILD_FINGERPRINT.find("QIH")

        if pos >= 0:
            filename = "cpu_mem_clodboot_test-" + BUILD_FINGERPRINT[pos:]
            filename = filename.replace(":", "-")
            filename = filename.replace("/", "_")

            filename += "_" + test_time + ".log"
            filename = args.log_path + filename

            if os.path.isfile(report_file_path):
                os.rename(report_file_path, filename)
                print("Test Log: " + filename + "\n\n")
        else:
            print("ERROR: Failed to rename log file. \n\n")
    else:
        # looks like test may not get started, skip
        pass


if __name__ == '__main__':
    main()
