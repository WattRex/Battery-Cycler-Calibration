#!/usr/bin/python3
'''
Driver of ea power supply.
'''
#######################        MANDATORY IMPORTS         #######################
from __future__ import annotations
import sys
import os

#######################         GENERIC IMPORTS          #######################


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
from drv.drv_scpi import DrvScpiHandlerC
from drv.drv_pwr import *

#######################          MODULE IMPORTS          #######################


#######################              ENUMS               #######################
class _CONSTANTS:
    MILI_UNITS = 1000

class DrvEaModeE(Enum):
    "Modes of the device"
    STANDBY = 0
    CV_MODE = 1
    CC_MODE = 2

#######################             CLASSES              #######################
class DrvEaPropertiesC(DrvPwrPropertiesC):
    "Properties of ea power supply device"
    def __init__(self, model: str|None = None, serial_number: str|None = None,
                 max_volt_limit: int = 0, max_current_limit: int = 0,
                 max_power_limit: int = 0) -> None:
        super().__init__(model, serial_number, max_volt_limit, max_current_limit, max_power_limit)


class DrvEaDataC(DrvPwrDataC):
    "Data class of ea power supply device"
    def __init__(self, mode: DrvEaModeE, status: DrvPwrStatusC,\
                 voltage: int, current: int, power: int) -> None:
        super().__init__(status = status, mode = mode, voltage = voltage,\
                         current = current, power = power)
        self.mode: DrvEaModeE = mode


class DrvEaDeviceC(DrvPwrDeviceC):
    "Principal class of ea power supply device"
    def __init__(self, handler: DrvScpiHandlerC) -> None:
        self.device_handler: DrvScpiHandlerC
        super().__init__(handler)
        self.__actual_data: DrvEaDataC = DrvEaDataC(mode = DrvEaModeE.STANDBY, \
                                                     status=DrvPwrStatusC(DrvPwrStatusE.OK), \
                                                     current=0, voltage=0, power=0)
        self.__properties: DrvEaPropertiesC = DrvEaPropertiesC(model = None, serial_number = None, \
                                                                max_volt_limit = 0, \
                                                                max_current_limit = 0, \
                                                                max_power_limit = 0)
        self.__initialize_control()
        self.__read_device_properties()


    def __read_device_properties(self) -> DrvEaPropertiesC:
        '''Read the device properties.
        Args:
            - None.
        Returns:
            - (DrvEaPropertiesC): Returns the device properties.
        Raises:
            - None.
        '''
        model: str|None = None
        serial_number: str|None = None
        max_current_limit: float = 0
        max_voltage_limit: float = 0
        max_power_limit: float = 0
        #Model and serial number
        info = self.device_handler.read_device_info()
        if info is not None:
            info = info[0].split(',')
            model = info[1]
            serial_number = info[2]
        #Max current limit
        read_curr = self.device_handler.send_and_read('SYSTem:NOMinal:CURRent?')
        if read_curr is not None:
            max_current_limit = self.device_handler.decode_numbers(read_curr[0])
            max_current_limit = int(max_current_limit * _CONSTANTS.MILI_UNITS)
        #Max voltage limit
        read_volt = self.device_handler.send_and_read('SYSTem:NOMinal:VOLTage?')
        if read_volt is not None:
            max_voltage_limit = self.device_handler.decode_numbers(read_volt[0])
            max_voltage_limit = int(max_voltage_limit * _CONSTANTS.MILI_UNITS)
        #Max power limit
        read_power = self.device_handler.send_and_read('SYSTem:NOMinal:POWer?')
        if read_power is not None:
            max_power_limit = self.device_handler.decode_numbers(read_power[0])
            max_power_limit = int(max_power_limit * _CONSTANTS.MILI_UNITS)

        self.__properties = DrvEaPropertiesC(model = model, serial_number = serial_number, \
                                            max_volt_limit = max_voltage_limit, \
                                            max_current_limit = max_current_limit, \
                                            max_power_limit = max_power_limit)
        return self.__properties


    def __initialize_control(self) -> None:
        ''' Enable remote control and turn it off.
        Args:
            - None.
        Returns:
            - None.
        Raises:
            - None.
        '''
        self.device_handler.send_msg('SYSTem:LOCK: ON')
        self.device_handler.send_msg('OUTPut: OFF')


    def disable(self) -> None:
        ''' Set the device in standby mode.
        Args:
            - None
        Returns:
            - None
        Raises:
            - None 
        '''
        self.device_handler.send_msg('OUTPut OFF')
        self.__actual_data.mode = DrvEaModeE.STANDBY


    def set_cc_mode(self, curr_ref: int, voltage_limit: int) -> None:
        '''
        Use source in constant current mode.
        Sink mode will be set with negative current values.
        Security voltage limit can be also set.
        Args:
            - curr_ref (int): current consign (milli Amps)
            - voltage_limit (int): voltage limit (millivolts)
        Returns:
            - None
        Raises:
            - None
        '''
        current = round(float(curr_ref)/_CONSTANTS.MILI_UNITS, 2)
        voltage = round(float(voltage_limit/_CONSTANTS.MILI_UNITS), 2)
        #Check if the power limit is exceeded
        if self.__properties.max_power_limit != 0:
            max_power_limit = self.__properties.max_power_limit/_CONSTANTS.MILI_UNITS
            if current * voltage > max_power_limit:
                voltage = max_power_limit / curr_ref
        else:
            current = 0
            voltage = 0

        self.device_handler.send_msg(f"CURRent {current}")
        self.device_handler.send_msg(f"VOLTage {voltage}")
        self.device_handler.send_msg('OUTPut ON')
        self.__actual_data.mode = DrvEaModeE.CC_MODE


    def set_cv_mode(self, volt_ref: int, current_limit: int) -> None:
        '''
        Use source in constant voltage mode .
        Security current limit can be also set for both sink and source modes. 
        It is recommended to set both!
        Args:
            - volt_ref (int): voltage consign (millivolts)
            - current_limit (int): current limit (milli Amps)
        Returns:
            - None
        Raises:
            - None
        '''
        voltage = round(float(volt_ref)/_CONSTANTS.MILI_UNITS, 2)
        current = round(float(current_limit/_CONSTANTS.MILI_UNITS), 2)
        #Check if the power limit is exceeded
        if self.__properties.max_power_limit != 0:
            max_power_limit = self.__properties.max_power_limit/_CONSTANTS.MILI_UNITS
            if voltage * current > max_power_limit:
                current = max_power_limit / volt_ref
        else:
            current = 0
            voltage = 0

        self.device_handler.send_msg(f"VOLTage {voltage}")
        self.device_handler.send_msg(f"CURRent {current}")
        self.device_handler.send_msg('OUTPut ON')
        self.__actual_data.mode = DrvEaModeE.CV_MODE


    def get_data(self) -> DrvEaDataC:
        '''Read the device data.
        Args:
            - None.
        Returns:
            - (DrvEaDataC): Returns the device data.
        Raises:
            - None.
        '''
        current = 0
        voltage = 0
        power = 0
        status = DrvPwrStatusC(DrvPwrStatusE.COMM_ERROR)

        read_all = self.device_handler.send_and_read('MEASure:ARRay?')
        read_all = read_all[0].split(',')
        if len(read_all) == 0 and read_all[0] is None:
            status = DrvPwrStatusC(DrvPwrStatusE.COMM_ERROR)
        else:
            voltage = int(self.device_handler.decode_numbers(read_all[0]) * _CONSTANTS.MILI_UNITS)
            current = int(self.device_handler.decode_numbers(read_all[1]) * _CONSTANTS.MILI_UNITS)
            power = int(self.device_handler.decode_numbers(read_all[2]) * _CONSTANTS.MILI_UNITS)

        self.__actual_data = DrvEaDataC(mode = self.__actual_data.mode, \
                                         status = status, \
                                         voltage = voltage, \
                                         current = current, \
                                         power = power)
        return self.__actual_data


    def get_properties(self) -> DrvEaPropertiesC:
        '''Read the device properties.
        Args:
            - None.
        Returns:
            - (DrvEaPropertiesC): Returns the device properties.
        Raises:
            - None.
        '''
        return self.__read_device_properties()


    def close(self) -> None:
        '''Close communication with the device.
        Args:
            - None
        Returns:
            - None
        Raises:
            - None
        '''
        self.disable()
        self.device_handler.close()
