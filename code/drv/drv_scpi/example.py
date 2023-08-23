#!/usr/bin/python3

# -*- coding: utf-8 -*-

"""
Example of use of the driver for SCPI devices.
"""

#######################        MANDATORY IMPORTS         #######################
import sys
import os

#######################      SYSTEM ABSTRACTION IMPORTS  #######################
sys.path.append(os.getcwd())
from sys_abs.sys_log import sys_log_logger_get_module_logger
if __name__ == '__main__':
    from sys_abs.sys_log import SysLogLoggerC
    cycler_logger = SysLogLoggerC('./sys_abs/sys_log/logginConfig.conf')
log = sys_log_logger_get_module_logger(__name__)

#######################         GENERIC IMPORTS          #######################


#######################       THIRD PARTY IMPORTS        #######################

#######################          MODULE IMPORTS          #######################
from drv.drv_scpi import DrvScpiHandlerC

#######################          PROJECT IMPORTS         #######################


#######################              ENUMS               #######################

#######################              CLASSES             #######################

def example():
    '''Example of the remote SCPI.
    '''
    multimeter = DrvScpiHandlerC(port='/dev/ttyUSB0', separator='\n', baudrate = 38400)
    log.info("multimeter")
    # multimeter.send_msg('VOLT:DC:NPLC 1')
    # multimeter.send_msg('FETCH?')
    # multimeter.receive_msg()
    # multimeter.send_and_read('FETCH?')
    log.info(f"{multimeter.read_device_info()}")

    source = DrvScpiHandlerC(port = '/dev/ttyACM0', separator = '\n', baudrate = 9600)
    log.info("source")
    # source.send_msg('SYSTem:LOCK: ON')
    # source.send_msg('SYSTem:LOCK: OFF')
    # source.send_and_read('MEASure:VOLTage?')
    log.info(f"{source.read_device_info()}")


if __name__ == '__main__':
    example()
