#!/usr/bin/python3
'''
Driver of power.
'''
#######################        MANDATORY IMPORTS         #######################
from __future__ import annotations
import sys
import os

#######################         GENERIC IMPORTS          #######################
import threading
from enum import Enum
from statistics import mean
from time import sleep, strftime
from typing import Any
import numpy as np
import yaml
import pandas as pd
import serial

#######################       THIRD PARTY IMPORTS        #######################

#######################      SYSTEM ABSTRACTION IMPORTS  #######################
sys.path.append(os.getcwd())
from sys_abs.sys_shd import SysShdChanC
from sys_abs.sys_log import sys_log_logger_get_module_logger
if __name__ == '__main__':
    from sys_abs.sys_log import SysLogLoggerC
    cycler_logger = SysLogLoggerC('./sys_abs/sys_log/logginConfig.conf')
log = sys_log_logger_get_module_logger(__name__)

#######################          PROJECT IMPORTS         #######################

#######################          MODULE IMPORTS          #######################
from config import *
from term import TermC
from drv.drv_bk import *
from drv.drv_ea import *
from drv.drv_epc import *
from drv.drv_scpi import *
from drv.drv_can import DrvCanNodeC
from drv.drv_epc import DrvEpcDeviceC, DrvEpcLimitE, DrvEpcModeE
#######################              ENUMS               #######################
_ERROR_RANGE = 50 #mUnits

class PwrModeE(Enum):
    "Enum to select the type of calibration to be done."
    VOLT_HS     = 0
    VOLT_LS     = 1
    CURR        = 2
    NONE        = 3

class _PwrParamsE(Enum):
    "Values of calibration."
    VOLT_HS_MIN = 10000 #mV         TODO: check values
    VOLT_HS_MAX = 12000 #mV         TODO: check values #15000
    VOLT_HS_STEP = 1000 #no units   TODO: check values
    VOLT_LS_MIN = 30000 #mV         TODO: check values
    VOLT_LS_MAX = 35000 #mV         TODO: check values
    VOLT_LS_STEP = 1000 #no units   TODO: check values
    CURR_MIN = 300      #mA         TODO: check values
    CURR_MAX = 350      #mA         TODO: check values
    CURR_STEP = 10      #no units   TODO: check values

#######################              CLASSES             #######################
class PwrC:
    "Class to manage the power devices."
    def __init__(self) -> None:
        self.__meter: DrvBkDeviceC = None
        self.__source: DrvEaDeviceC = None
        self.__epc: DrvEpcDeviceC = None
        self._config_power_devices()


    def check_devices(self) -> ConfigResultE:
        '''Check if the power devices are connected.
        Args:
            - None
        Returns:
            - result (ConfigResultE): Result of the check.
        Raises:
            - None
        '''
        if self.__source is None or self.__meter is None or self.__epc is None:
            result = ConfigResultE.ERROR
        else:
            result = ConfigResultE.NO_ERROR
        return result


    def calib_volt_hs(self) -> ConfigResultE:
        '''Calibrate the high voltage source.
        Args:
            - None
        Returns:
            - result_calib (ConfigResultE): Result of the calibration.
        Raises:
            - None
        '''
        log.info("Calibrating voltage high side")
        result = self._steps_of_calibration(mode = PwrModeE.VOLT_HS)
        return result


    def calib_volt_ls(self) -> ConfigResultE:
        '''Calibrate the low voltage source.
        Args:
            - None
        Returns:
            - result (ConfigResultE): Result of the calibration.
        Raises:
            - None
        '''
        log.info("Calibrating voltage low side")
        result = self._steps_of_calibration(mode = PwrModeE.VOLT_LS)
        return result


    def calib_curr(self) -> ConfigResultE:
        '''Calibrate the current source.
        Args:
            - None
        Returns:
            - result (ConfigResultE): Result of the calibration.
        Raises:
            - None
        '''
        log.info("Calibrating current")
        result = self._steps_of_calibration(mode = PwrModeE.CURR)
        return result


    def _config_power_devices(self) -> None:
        '''Configure the DRV devices.
        Args:
            - None
        Returns:
            - None
        Raises:
            - None
        '''
        ports_path = ConfigWsC.get_file_conf_ports()
        if os.path.exists(ports_path):
            with open(ports_path, 'r', encoding="utf-8") as file:
                ports = yaml.load(file, Loader=yaml.FullLoader)
            try:
                #Multimeter configuration
                scpi_bk = DrvScpiHandlerC(port = ports['multimeter_port'], separator='\n', \
                                          baudrate=38400, timeout=1, write_timeout=1)
                self.__meter = DrvBkDeviceC(handler = scpi_bk)

                #Source configuration
                scpi_ea = DrvScpiHandlerC(port = ports['source_port'], separator = '\n', \
                                          timeout = 0.8, write_timeout = 2, \
                                          parity = serial.PARITY_ODD, baudrate = 9600)
                self.__source: DrvEaDeviceC = DrvEaDeviceC(handler = scpi_ea)

                #EPC configuration
                can_queue = SysShdChanC(100000000)
                can_queue.delete_until_last()
                # Flag to know if the can is working
                _working_can = threading.Event()
                _working_can.set()
                #Create the thread for CAN
                can = DrvCanNodeC(can_queue, _working_can)
                can.start()
                self.__epc = DrvEpcDeviceC(dev_id=0x3, \
                                           device_handler=SysShdChanC(500),
                                           tx_can_queue=can_queue)
                self.__epc.open(addr= 0x030, mask= 0x7F0)

            except Exception as err:
                log.error(f"Error opening ports. {err}")

        else:
            log.error("File {ports_path} does not exist.")


    def _steps_of_calibration(self, mode: PwrModeE) -> ConfigResultE:
        '''Steps of calibration.
        Args:
            - mode (PwrModeE): Type of calibration to be done.
        Returns:
            - result_calib (ConfigResultE): Result of the calibration.
        Raises:
            - None
        '''
        result_calib: ConfigResultE = ConfigResultE.ERROR
        if self._rewrite_calib(mode = mode):
            calib: pd.DataFrame = self._obtain_values(mode = mode)
            line: tuple = self._parameters_line(calib)
            result_calib = self._save_calib_data(mode = mode, data = calib, \
                                               factor = line[0], offset = line[1])
            if result_calib == ConfigResultE.NO_ERROR:
                log.info(f"Calibration of {mode.name} finished.")
            else:
                log.error(f"Calibration of {mode.name} failed.")
        else:
            log.info(f"Calibration of {mode.name} canceled.")

        return result_calib


    def _rewrite_calib(self, mode: PwrModeE) -> bool:
        ''' Check if the calibration data already exists.
        Args:
            - mode (PwrModeE): Type of calibration to be done.
        Returns:
            - result (bool): True if the calibration data already exists, False if not.
        Raises:
            - None
        '''
        info_path = ConfigWsC.get_info_file_path()

        if os.path.exists(info_path):
            with open(info_path, 'r', encoding="utf-8") as file:
                conf_dev = yaml.load(file, Loader=yaml.FullLoader)
                if conf_dev['calib_data'][mode.name]['factor'] is None and \
                   conf_dev['calib_data'][mode.name]['offset'] is None and \
                   conf_dev['calib_data'][mode.name]['date'] is None:
                    exist_dates = False
                else:
                    exist_dates = True

            if exist_dates:
                while True:
                    try:
                        check = str(input(f"Calibration data for {mode.name} already exists. \
                                          ¿Do you want to replace it? (y/n): ")).lower()
                        if check == 'y':
                            result = True
                            break
                        elif check == 'n':
                            result = False
                            break
                        else:
                            print("Invalid option.")
                    except ValueError:
                        print("Invalid option.")
            else:
                result = True
        else:
            log.error(f"File {info_path} does not exist.")
        return result


    def _obtain_values(self, mode: PwrModeE) -> pd.DataFrame:
        ''' Obtain voltage of multimeter and EPC.
        Args:
            - mode (PwrModeE): Type of calibration to be done.

        Returns:
            - result (pd.DataFrame): Dataframe with the voltage of the source,
                                     voltage measured with the multimeter and
                                     the one measured with the EPC.
        Raises:
            - None
        '''
        val_min = _PwrParamsE.__getitem__(f"{mode.name}_MIN").value
        step = _PwrParamsE.__getitem__(f"{mode.name}_STEP").value
        val_max = _PwrParamsE.__getitem__(f"{mode.name}_MAX").value

        if mode is PwrModeE.VOLT_HS or mode is PwrModeE.VOLT_LS:
            type_columns = ['voltage source', 'voltage multimeter', 'voltage EPC']
            self.__meter.set_mode(DrvBkModeE.VOLT_AUTO)
            self.__epc.set_wait_mode(limit_type = DrvEpcLimitE.TIME, limit_ref = 3000)

        elif mode is PwrModeE.CURR:
            type_columns = ['current source', 'current multimeter', 'current EPC']
            self.__meter.set_mode(DrvBkModeE.CURR_R2_A)
        result = pd.DataFrame(columns = type_columns)

        val_source = val_min


        #Iteration to obtain the voltage or current of the multimeter and the EPC
        while val_source <= val_max:
            sleep(2)
            if mode is PwrModeE.VOLT_HS or mode is PwrModeE.VOLT_LS:
                self.__source.set_cv_mode(volt_ref = val_source, current_limit = 500) #TODO: check limit
                while abs(val_source - self.__source.get_data().voltage) > _ERROR_RANGE:
                    sleep(0.5)

            elif mode is PwrModeE.CURR:
                self.__source.set_cc_mode(curr_ref = val_source, voltage_limit = 12000) #TODO: check limit
                self.__epc.set_cc_mode(ref = val_min, limit_type= DrvEpcLimitE.TIME, limit_ref=3000) #TODO: check
                while abs(val_source - self.__source.get_data().Current) > _ERROR_RANGE:
                    sleep(0.5)

            av_meter: list= []
            av_epc: list= []
            for _ in range(0,9, 1):
                #Data voltage high side calibration
                if mode is PwrModeE.VOLT_HS:
                    val_meter = self.__meter.get_data().voltage
                    val_epc = self.__epc.get_data().hs_voltage

                #Data voltage low side calibration
                elif mode is PwrModeE.VOLT_HS or mode is PwrModeE.VOLT_LS:
                    val_meter = self.__meter.get_data().voltage
                    val_epc = self.__epc.get_data().ls_voltage

                #Data current calibration
                elif mode is PwrModeE.CURR:
                    val_meter = self.__meter.get_data().current
                    val_epc = self.__epc.get_data().ls_current

                av_meter.append(val_meter)
                av_epc.append(val_epc)

            new_row = pd.DataFrame([[val_source, int(mean(av_meter)), int(mean(av_epc))]], \
                                   columns = type_columns)
            result = pd.concat([result,new_row], ignore_index=True)

            TermC.show_progress_bar(iteration = val_source - val_min, total = val_max - val_min)
            val_source += step

        self.__source.disable()
        return result


    def _parameters_line(self, data: pd.DataFrame) -> tuple:
        ''' Obtain the parameters of the line that best fits the data.
        Args:
            - data (pd.DataFrame): Dataframe with the voltage of the source,
                                   voltage measured with the multimeter and
                                   the one measured with the EPC.
        Retuns (tuple):
            - factor (int): Factor of the line obtain.
            - offset (int): Offset of the line obtain.
        Raises:
            - None
        '''
        axis_x = np.array(data.iloc[:,1]).tolist() #Column of multimeter
        axis_y = np.array(data.iloc[:,2]).tolist() #Column of EPC

        factor, intersection = np.polyfit(axis_x, axis_y, 1)
        offset = intersection - (factor * axis_x[0])
        factor = float(round(factor, 3))
        offset = float(round(offset, 3))
        return factor, offset


    def _save_calib_data(self, mode: PwrModeE, data: pd.DataFrame, factor: int, offset: int) \
        -> ConfigResultE:
        ''' Save the calibration data in a csv file and in a yaml file.
        Args:
            - mode (str): Type of calibration to be saved.
            - data (pd.DataFrame): Dataframe with the voltage of the source,
                                   voltage measured with the multimeter and
                                   the one measured with the EPC.
            - factor (int): Factor of the line obtain.
            - offset (int): Offset of the line obtain.
        Returns:
            - result (ConfigResultE): Result of the calibration.
        Raises:
            - None
        '''
        result: ConfigResultE = ConfigResultE.ERROR
        info_path = ConfigWsC.get_info_file_path()
        if os.path.exists(info_path):
            with open(info_path, 'r', encoding="utf-8") as file:
                conf_dev = yaml.load(file, Loader=yaml.FullLoader)
            conf_dev['calib_data'][mode.name]['factor'] = factor
            conf_dev['calib_data'][mode.name]['offset'] = offset
            conf_dev['calib_data'][mode.name]['date'] = strftime("%d/%m/%Y %H:%M:%S")
            with open(info_path, 'w', encoding="utf-8") as file:
                yaml.dump(conf_dev, file)

            if mode == PwrModeE.VOLT_HS:
                calib_file = ConfigWsC.get_volt_high_side_path()
            elif mode == PwrModeE.VOLT_LS:
                calib_file = ConfigWsC.get_volt_low_side_path()
            elif mode == PwrModeE.CURR:
                calib_file = ConfigWsC.get_calib_current_path()

            data.to_csv(calib_file, index=False)
            result = ConfigResultE.NO_ERROR
        else:
            log.error(f"File {info_path} does not exist.")
        return result
