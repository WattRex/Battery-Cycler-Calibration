#!/usr/bin/python3
'''
Driver of power.
'''
#######################        MANDATORY IMPORTS         #######################
from __future__ import annotations
import sys
import os

#######################         GENERIC IMPORTS          #######################
from subprocess import run, PIPE
import threading
from enum import Enum
from statistics import mean
from time import sleep, strftime
import numpy as np
import yaml
import pandas as pd
import serial

#######################       THIRD PARTY IMPORTS        #######################

#######################      SYSTEM ABSTRACTION IMPORTS  #######################
sys.path.append(os.getcwd())
from sys_abs.sys_shd import SysShdChanC # pylint: disable=wrong-import-position
from sys_abs.sys_log import sys_log_logger_get_module_logger # pylint: disable=wrong-import-position
if __name__ == '__main__':
    from sys_abs.sys_log import SysLogLoggerC
    cycler_logger = SysLogLoggerC('./sys_abs/sys_log/logginConfig.conf')
log = sys_log_logger_get_module_logger(__name__)

#######################          PROJECT IMPORTS         #######################

#######################          MODULE IMPORTS          #######################
from config import ConfigWsC, ConfigResultE             # pylint: disable=wrong-import-position
from term import TermC                                  # pylint: disable=wrong-import-position
from drv.drv_bk import DrvBkDeviceC, DrvBkModeE         # pylint: disable=wrong-import-position
from drv.drv_ea import DrvEaDeviceC                     # pylint: disable=wrong-import-position
from drv.drv_epc import DrvEpcDeviceC, DrvEpcLimitE     # pylint: disable=wrong-import-position
from drv.drv_scpi import DrvScpiHandlerC                # pylint: disable=wrong-import-position
from drv.drv_can import DrvCanNodeC                     # pylint: disable=wrong-import-position

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
    VOLT_HS_MIN     = 5400      #mV
    VOLT_HS_MAX     = 14000     #mV
    VOLT_HS_STEP    = 100       #no units
    VOLT_LS_MIN     = 500       #mV
    VOLT_LS_MAX     = 5000      #mV
    VOLT_LS_STEP    = 100       #no units
    CURR_MIN        = -15000    #mA
    CURR_MAX        = 15000     #mA
    CURR_STEP       = 100       #no units

#######################              CLASSES             #######################
class PwrC:
    "Class to manage the power devices."
    def __init__(self) -> None:
        self.__meter: DrvBkDeviceC  = None
        self.__source: DrvEaDeviceC = None
        self.__epc: DrvEpcDeviceC   = None
        self._config_power_devices()


    def calib_volt_hs(self) -> ConfigResultE:
        '''Calibrate the high voltage source.
        Args:
            - None
        Returns:
            - result (ConfigResultE): Result of the calibration.
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
                scpi_bk = DrvScpiHandlerC(port = ports['multimeter'], separator='\n', \
                                          baudrate=38400, timeout=1, write_timeout=1)
                self.__meter = DrvBkDeviceC(handler = scpi_bk)

                #Source configuration
                scpi_ea = DrvScpiHandlerC(port = ports['source'], separator = '\n', \
                                          timeout = 0.8, write_timeout = 0.8, \
                                          parity = serial.PARITY_ODD, baudrate = 9600)
                self.__source: DrvEaDeviceC = DrvEaDeviceC(handler = scpi_ea)

                self.__source.set_cv_mode(volt_ref = 6000, current_limit = 500)
                print("CAAAAAMAMAMAMAMAMAMMAMAMAMA.")

                cmd = "sudo ip link set up txqueuelen 1000000 can0 type can bitrate 125000"
                console = run(args=cmd, shell =True, stdout=PIPE, stderr=PIPE)
                #EPC configuration
                can_queue = SysShdChanC(100000000)
                can_queue.delete_until_last()
                # Flag to know if the can is working
                print("EEEEPPPPPPCCCCCCCCCCCCCCCCCCCC.")
                _working_can = threading.Event()
                _working_can.set()
                #Create the thread for CAN
                can = DrvCanNodeC(can_queue, _working_can)
                can.start()
                self.__epc = DrvEpcDeviceC(dev_id=0x3, \
                                           device_handler=SysShdChanC(500),
                                           tx_can_queue=can_queue)
                self.__epc.open(addr= 0x030, mask= 0x7F0)
                # self.__source.disable()
            except Exception as err:
                log.error(f"Error opening ports. {err}")
                print("Error opening ports.")

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
        #Check if the calibration has already been done
        info_path = ConfigWsC.get_info_file_path()
        if os.path.exists(info_path):
            with open(info_path, 'r', encoding="utf-8") as file:
                conf_dev = yaml.load(file, Loader=yaml.FullLoader)
                rewrite = True
                if conf_dev['calib_data'][mode.name]['factor'] is not None or \
                   conf_dev['calib_data'][mode.name]['offset'] is not None or \
                   conf_dev['calib_data'][mode.name]['date']   is not None:
                    rewrite = TermC.query_rewrite_calib()
        else:
            log.error(f"File {info_path} does not exist.")
            rewrite = False
        #Calibration
        if rewrite:
            calib: pd.DataFrame = self._obtain_values(mode = mode)
            #Obtain the parameters of the line
            axis_x = np.array(calib.iloc[:,1]).tolist() #Column of multimeter
            axis_y = np.array(calib.iloc[:,2]).tolist() #Column of EPC
            factor, intersection = np.polyfit(axis_x, axis_y, 1)
            offset = intersection - (factor * axis_x[0])
            #Save the calibration data
            result_calib = self._save_calib_data(mode = mode, data = calib, \
                                                factor = float(round(factor, 3)), \
                                                offset = float(round(offset, 3)))
            if result_calib == ConfigResultE.NO_ERROR:
                log.info(f"Calibration of {mode.name} finished.")
                print("Calibration finished.")
            else:
                log.error(f"Calibration of {mode.name} failed.")
                print("Calibration failed.")
        else:
            log.info(f"Calibration of {mode.name} canceled.")
            print("Calibration canceled.")
        return result_calib


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
        step    = _PwrParamsE.__getitem__(f"{mode.name}_STEP").value
        val_max = _PwrParamsE.__getitem__(f"{mode.name}_MAX").value

        if mode is PwrModeE.VOLT_HS or mode is PwrModeE.VOLT_LS:
            type_columns = ['voltage source', 'voltage multimeter', 'voltage EPC']
            self.__meter.set_mode(DrvBkModeE.VOLT_AUTO)
            self.__epc.set_wait_mode(limit_type = DrvEpcLimitE.TIME, limit_ref = 3000)

        elif mode is PwrModeE.CURR:
            type_columns = ['current source', 'current multimeter', 'current EPC']
            self.__meter.set_mode(DrvBkModeE.CURR_R2_A)

        result = pd.DataFrame(columns = type_columns)
        val_to_send = val_min
        #Iteration to obtain the voltage or current of the multimeter and the EPC
        while val_to_send <= val_max:
            sleep(1)
            if mode is PwrModeE.VOLT_HS or mode is PwrModeE.VOLT_LS:
                self.__source.set_cv_mode(volt_ref = val_to_send, current_limit = 500)
                while abs(val_to_send - self.__source.get_data().voltage) > _ERROR_RANGE:
                    sleep(0.1)

            elif mode is PwrModeE.CURR:
                #PRINT DE PONER DOS BATERÍAS
                self.__epc.set_cc_mode(ref = val_to_send, limit_type = DrvEpcLimitE.TIME, \
                                       limit_ref = 8000)
                while abs(val_to_send - self.__meter.get_data().current) > _ERROR_RANGE:
                    sleep(0.1)

            av_meter: list= []
            av_epc: list= []
            for _ in range(0,9, 1):
                #Data voltage high side calibration
                if mode is PwrModeE.VOLT_HS:
                    val_meter   = self.__meter.get_data().voltage
                    val_epc     = self.__epc.get_data().hs_voltage

                #Data voltage low side calibration
                elif mode is PwrModeE.VOLT_HS or mode is PwrModeE.VOLT_LS:
                    val_meter   = self.__meter.get_data().voltage
                    val_epc     = self.__epc.get_data().ls_voltage

                #Data current calibration
                elif mode is PwrModeE.CURR:
                    val_meter   = self.__meter.get_data().current
                    val_epc     = self.__epc.get_data().ls_current

                av_meter.append(val_meter)
                av_epc.append(val_epc)

            new_row = pd.DataFrame([[val_to_send, int(mean(av_meter)), int(mean(av_epc))]], \
                                   columns = type_columns)
            result = pd.concat([result,new_row], ignore_index=True)

            TermC.show_progress_bar(iteration = val_to_send - val_min, total = val_max - val_min)
            val_to_send += step

        self.__source.disable()
        return result


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
            log.info(f"Saved data. Mode:{mode.name}")
            print("Saved data.")
        else:
            log.error(f"File {info_path} does not exist.")
            print("Data could not be saved.")
        return result
