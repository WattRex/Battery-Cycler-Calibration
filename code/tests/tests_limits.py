#!/usr/bin/python3
"""
    This script tests the triger of the different limits of the EPC in each operation mode.
"""
#######################        MANDATORY IMPORTS         #######################
from __future__ import annotations
import os
import sys
import threading
import time

#######################         GENERIC IMPORTS          #######################
from datetime import datetime
from pytz import timezone
from subprocess import run, PIPE

#######################       THIRD PARTY IMPORTS        #######################
import csv
#######################    SYSTEM ABSTRACTION IMPORTS    #######################
sys.path.append(os.getcwd())  #get absolute path

if __name__ == '__main__':
    from system_logger_tool import SysLogLoggerC, sys_log_logger_get_module_logger
    cycler_logger = SysLogLoggerC(file_log_levels= 'log_config.yaml')
from system_shared_tool import SysShdChanC
log = sys_log_logger_get_module_logger(__name__)

#######################          MODULE IMPORTS          #######################
from can_sniffer import DrvCanNodeC
from battery_cycler_drv_epc import DrvEpcDeviceC, DrvEpcLimitE, DrvEpcModeE
#######################          PROJECT IMPORTS         #######################

#######################              ENUMS               #######################

#######################             CLASSES              #######################
class _ConstantsC():
    TO_MILIS = 1000
    TO_DECIS = 100
LINE_CLEAR = '\x1b[2K'

#######################            FUNCTIONS             #######################

def wait(tic, sleep_time, data) -> None:
    while(time.time()-tic <= sleep_time):
        data.epc.read_can_buffer()

class EpcData():
    def __init__(self, epc: DrvEpcDeviceC, file_path:str) -> None:
        self.file_path = file_path
        self.epc       = epc
        self.mode      = None
        self.last_mode = None
        self.limit     = None
        self.ref       = None
        self.limit_ref = None
        self.ls_v      = None
        self.ls_i      = None
        self.ls_pwr    = None
        self.hs_v      = None

    def change_mode(self, mode: DrvEpcModeE, direction:str, limit: DrvEpcLimitE) -> None:
        print('\r\n...')
        print(end=LINE_CLEAR)
        print('Changing to {} {} with {} limit'.format(mode.name, direction, limit.name), end='\n\r')
        #ask for the reference. The units are mA for current, mV for voltage, ms for wait and dW for power
        units_ref = 'mA' if mode is DrvEpcModeE.CC_MODE else 'mV' if mode is DrvEpcModeE.CV_MODE else 'ms' if mode is DrvEpcModeE.WAIT else 'dW'
        ref = int(input('Set ref in {}: '.format(units_ref)))
        print(end=LINE_CLEAR)
        #ask for the limit. The units are mV for voltage, mA for current, ms for time and dW for power
        units_limit = 'mV' if limit is DrvEpcLimitE.VOLTAGE else 'mA' if limit is DrvEpcLimitE.CURRENT else 'ms' if limit is DrvEpcLimitE.TIME else 'dW'
        lim = int(input('Set limit in {}: '.format(units_limit)))
        #set the mode
        if mode is DrvEpcModeE.CC_MODE:
            epc.set_cc_mode(ref, limit, lim)
        elif mode is DrvEpcModeE.CV_MODE:
            epc.set_cv_mode(ref, limit, lim)
        elif mode is DrvEpcModeE.CP_MODE:
            epc.set_cp_mode(ref, limit, lim)
        else:
            epc.set_wait_mode(limit_type=limit, limit_ref=lim)
        print('Mode changed to {} {} in {} {} with {} limit in {} {}'.format(mode.name, direction, ref, units_ref,
                                                                     limit.name, lim, units_limit), end='\n\r')
    def print(self) -> None:
        print(end=LINE_CLEAR)
        print ("mode: {}, ls_v: {:.3f} V, ls_i: {:.3f} A, ls_pwr: {:.3f} W, hs_v: {:.3f} V".format(self.mode.name, self.ls_v,
                                                                           self.ls_i, self.ls_pwr, self.hs_v), end="\r")

    def to_csv (self) -> None:
        #write all atributes to a csv file
        #check if the file exists
        if (not os.path.isfile(self.file_path)):
            with open(self.file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                row = ["timestamp", "mode", "limit", "ref", "limit_ref", 
                    "ls_v", "ls_i", "ls_pwr", "hs_v"]
                writer.writerow(row)
        #if the file exists, append the data in the last row
        with open(self.file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            timestamp = datetime.now(timezone('Europe/Madrid')).strftime("%Y-%m-%d %H:%M:%S.%f")
            row = [timestamp, self.mode.name, self.limit.name, self.ref, self.limit_ref, 
                   self.ls_v, self.ls_i, self.ls_pwr, self.hs_v]
            writer.writerow(row)

    def update(self) -> None:
        self.last_mode = self.mode
        dict_status    = self.epc.get_mode()
        self.mode      = dict_status.mode
        self.limit     = dict_status.lim_mode
        self.ref       = dict_status.ref
        self.limit_ref = dict_status.lim_ref
        self.ls_v      = epc.get_elec_meas(periodic_flag = True).ls_voltage /1000
        self.ls_i      = epc.get_elec_meas(periodic_flag = True).ls_current /1000
        self.ls_pwr    = epc.get_elec_meas(periodic_flag = True).ls_power   /10
        self.hs_v      = epc.get_elec_meas(periodic_flag = True).hs_voltage /1000

if __name__ == '__main__':
    cmd = "sudo ip link set down can0"
    run(args=cmd, shell =True, stdout=PIPE, stderr=PIPE)
    cmd = "sudo ip link set up txqueuelen 1000000 can0 type can bitrate 125000"
    run(args=cmd, shell =True, stdout=PIPE, stderr=PIPE)

    can_queue = SysShdChanC(100000000)
    can_queue.delete_until_last()
    # Flag to know if the can is working
    _working_can = threading.Event()
    _working_can.set()
    #Create the thread for CAN
    can = DrvCanNodeC(can_queue, _working_can)

    path = os.path.join(os.getcwd(),'drv','drv_epc','example')
    dev_id = int(input("Introduce the can_id: "))
    log.info('Not devices introduced')

    epc = DrvEpcDeviceC(dev_id, SysShdChanC(500), can_queue)
    can.start()
    epc.open()
    time.sleep(0.1)
    epc.set_periodic(elect_en= True, elect_period=100, temp_en=True, temp_period=100)
    #ack_en=True, ack_period=5000,
    data = EpcData(epc, 'data_test_modes_epc_'+str(dev_id)+'.csv')
    epc.set_wait_mode(limit_type=DrvEpcLimitE.TIME, limit_ref=3000)
    tic = time.time()
    epc.get_ls_curr_limits()
    while(time.time()-tic <= 0.5):
        data.update()
        time.sleep(0.1)

    machine_status = 4
    mode_changed = True
    data.update()
    while(1):
        tic = time.time()
        data.print()
        #status machine
        if data.mode is DrvEpcModeE.IDLE and data.last_mode is not DrvEpcModeE.IDLE:
            print('\r\n...')
            print(end=LINE_CLEAR)
            new_mode = input('Do you want to change the mode? [y/n] ')
            if (new_mode == 'y'):
                machine_status +=1
            elif (new_mode == 'n'):
                pass
            else:
                try:
                    machine_status = int(new_mode)
                except:
                    machine_status = 99
            if machine_status == 1:
                mode      = DrvEpcModeE.CC_MODE
                direction = 'CHARGE'
                limit     = DrvEpcLimitE.VOLTAGE
            elif machine_status == 2:    
                mode      = DrvEpcModeE.CC_MODE
                direction = 'DISCHARGE'
                limit     = DrvEpcLimitE.VOLTAGE
            elif machine_status == 3:
                mode      = DrvEpcModeE.CC_MODE
                direction = 'CHARGE'
                limit     = DrvEpcLimitE.TIME
            elif machine_status == 4:
                mode      = DrvEpcModeE.CC_MODE
                direction = 'DISCHARGE'
                limit     = DrvEpcLimitE.TIME
            elif machine_status == 5:
                mode      = DrvEpcModeE.CC_MODE
                direction = 'CHARGE'
                limit     = DrvEpcLimitE.POWER
            elif machine_status == 6:
                mode      = DrvEpcModeE.CC_MODE
                direction = 'DISCHARGE'
                limit     = DrvEpcLimitE.POWER
            elif machine_status == 7:
                mode      = DrvEpcModeE.CV_MODE
                direction = 'CHARGE'
                limit     = DrvEpcLimitE.CURRENT
            elif machine_status == 8:
                mode      = DrvEpcModeE.CV_MODE
                direction = 'DISCHARGE'
                limit     = DrvEpcLimitE.CURRENT
            elif machine_status == 9:
                mode      = DrvEpcModeE.CV_MODE
                direction = 'CHARGE'
                limit     = DrvEpcLimitE.TIME
            elif machine_status == 10:
                mode      = DrvEpcModeE.CV_MODE
                direction = 'DISCHARGE'
                limit     = DrvEpcLimitE.TIME
            elif machine_status == 11:
                mode      = DrvEpcModeE.CV_MODE
                direction = 'CHARGE'
                limit     = DrvEpcLimitE.POWER
            elif machine_status == 12:
                mode      = DrvEpcModeE.CV_MODE
                direction = 'DISCHARGE'
                limit     = DrvEpcLimitE.POWER
            elif machine_status == 13:
                mode      = DrvEpcModeE.CP_MODE
                direction = 'CHARGE'
                limit     = DrvEpcLimitE.VOLTAGE
            elif machine_status == 14:
                mode      = DrvEpcModeE.CP_MODE
                direction = 'DISCHARGE'
                limit     = DrvEpcLimitE.VOLTAGE
            elif machine_status == 15:
                mode      = DrvEpcModeE.CP_MODE
                direction = 'CHARGE'
                limit     = DrvEpcLimitE.TIME
            elif machine_status == 16:
                mode      = DrvEpcModeE.CP_MODE
                direction = 'DISCHARGE'
                limit     = DrvEpcLimitE.TIME
            elif machine_status == 17:
                mode      = DrvEpcModeE.CP_MODE
                direction = 'CHARGE'
                limit     = DrvEpcLimitE.CURRENT
            elif machine_status == 18:
                mode      = DrvEpcModeE.CP_MODE
                direction = 'DISCHARGE'
                limit     = DrvEpcLimitE.CURRENT
            elif machine_status == 19:
                mode      = DrvEpcModeE.WAIT
                direction = 'DISCHARGE'
                limit     = DrvEpcLimitE.TIME
            else:
                epc.set_wait_mode(limit_type= DrvEpcLimitE.TIME, limit_ref=3000)
                machine_status = 0
            data.change_mode(mode, direction, limit)
            mode_changed = True
        #update epc status and measures
        data.update()
        data.to_csv()
        if mode_changed:
            tic = time.time()
            mode_changed = False
        wait(tic, 0.1, data)
    print("fin")
