#!/usr/bin/python3
'''
Driver for communication with SCPI devices.
'''
#######################        MANDATORY IMPORTS         #######################
from __future__ import annotations
import sys
import os
import re

#######################         GENERIC IMPORTS          #######################
from typing import List
import serial
from time import sleep

#######################       THIRD PARTY IMPORTS        #######################
from enum import Enum

#######################      SYSTEM ABSTRACTION IMPORTS  #######################
sys.path.append(os.getcwd())
from sys_abs.sys_log import sys_log_logger_get_module_logger
if __name__ == '__main__':
    from sys_abs.sys_log import SysLogLoggerC
    cycler_logger = SysLogLoggerC('./sys_abs/sys_log/logginConfig.conf')
log = sys_log_logger_get_module_logger(__name__)

#######################          PROJECT IMPORTS         #######################
from sys_abs.sys_shd import SysShdChanC


#######################          MODULE IMPORTS          #######################
from drv.drv_scpi import DrvScpiHandlerC

#######################              ENUMS               #######################
class DrvScipiCmdTypeE(Enum):
    '''Types of commands to be sent to the device.'''
    WRITE = 0
    READ = 1
    WRITE_READ = 2
    ADD_DEV = 3

#######################             CLASSES              #######################
class DrvScpiCmdDataC:
    '''
    Hold the data to be sent to the device.
    '''
    def __init__(self, data_type: DrvScipiCmdTypeE, port: str, payload: str|DrvScpiHandlerC):
        self.data_type: DrvScipiCmdTypeE = data_type
        self.port: str = port
        self.payload: str|DrvScpiHandlerC = payload


class DrvScpiDeviceC:
    '''
    Principal class of the driver.
    '''
    def __init__(self, port: str, payload: DrvScpiHandlerC, chan: SysShdChanC):
        self.payload: DrvScpiHandlerC = payload
        self.chan: SysShdChanC = chan
