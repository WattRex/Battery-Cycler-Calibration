#!/usr/bin/python3
'''
Driver of power.
'''

#######################        MANDATORY IMPORTS         #######################
import sys
import os

#######################         GENERIC IMPORTS          #######################
from subprocess import run, PIPE
from threading import Event
from enum import Enum
from statistics import median
from time import sleep, strftime
from numpy import array, polyfit
from yaml import load, dump, FullLoader
from pandas import DataFrame, concat
import serial

#######################       THIRD PARTY IMPORTS        #######################

#######################      SYSTEM ABSTRACTION IMPORTS  #######################
sys.path.append(os.getcwd())
from system_logger_tool import sys_log_logger_get_module_logger # pylint: disable=wrong-import-position
log = sys_log_logger_get_module_logger(__name__)
from system_shared_tool import SysShdChanC # pylint: disable=wrong-import-position
#######################          PROJECT IMPORTS         #######################

#######################          MODULE IMPORTS          #######################
from config import ConfigWsC, ConfigResultE             # pylint: disable=wrong-import-position
from term import TermC                                  # pylint: disable=wrong-import-position
from wattrex_driver_bk import DrvBkDeviceC, DrvBkModeE   # pylint: disable=wrong-import-position
from wattrex_driver_ea import DrvEaDeviceC               # pylint: disable=wrong-import-position
from wattrex_driver_epc import DrvEpcDeviceC, DrvEpcLimitE # pylint: disable=wrong-import-position
from scpi_sniffer import DrvScpiHandlerC                   # pylint: disable=wrong-import-position
from can_sniffer import DrvCanNodeC                        # pylint: disable=wrong-import-position

#######################              ENUMS               #######################
_ERROR_RANGE = 150 #mUnits

class PwrModeE(Enum):
    "Enum to select the type of calibration to be done."
    VOLT_HS     = 0
    VOLT_LS     = 1
    CURR        = 2
    NONE        = 3

class _PwrParamsE(Enum):
    "Values of calibration."
    VOLT_HS_MIN     = 5000      #mV
    VOLT_HS_MAX     = 14000     #mV 14000
    VOLT_HS_STEP    = 500       #no units
    VOLT_LS_MIN     = 500       #mV
    VOLT_LS_MAX     = 5000      #mV
    VOLT_LS_STEP    = 500       #no units
    CURR_MIN        = -1500     #mA
    CURR_MAX        = 1500      #mA
    CURR_STEP       = 100       #no units

#######################              CLASSES             #######################
class PwrC:
    "Class to manage the power devices."
    def __init__(self) -> None:
        self.__volt_meter: DrvBkDeviceC  = None
        self.__curr_meter: DrvBkDeviceC  = None
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
        print("Calibrating voltage high side.")
        self.__epc.set_wait_mode(limit_type = DrvEpcLimitE.TIME, limit_ref = 3000)
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
        print("Calibrating voltage low side.")
        self.__epc.set_wait_mode(limit_type = DrvEpcLimitE.TIME, limit_ref = 3000)
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
        print("Calibrating current.")
        self.off_power()
        result = self._steps_of_calibration(mode = PwrModeE.CURR)
        return result


    def on_power(self) -> None:
        '''Enable the power source.
        Args:
            - None
        Returns:
            - None
        Raises:
            - None
        '''
        self.__source.set_cv_mode(volt_ref = 7000, current_limit = 2000, channel = 1)


    def off_power(self) -> None:
        '''Disable the power source.
        Args:
            - None
        Returns:
            - None
        Raises:
            - None
        '''
        self.__source.disable(channel = 1)
        self.__source.disable(channel = 2)


    def add_epc(self, new_id_can: int) -> None:
        '''Add new epc.
        Args:
            - new_id_can (int): New can ID.
        Return:
            - None
        Raises:
            - None
        '''
        self.__epc = DrvEpcDeviceC(dev_id = new_id_can,
                                   device_handler = SysShdChanC(500),
                                   tx_can_queue = self.__can_queue)
        self.__epc.open()

    def reset_can(self) -> None:
        '''Reset CAN.
        Args:
            - None
        Return:
            - None
        Raises:
            - None
        '''
        log.info("Reset CAN")
        cmd = "sudo ip link set down can0"
        run(args=cmd, shell =True, stdout=PIPE, stderr=PIPE, check=False)
        cmd = "sudo ip link set up txqueuelen 1000000 can0 type can bitrate 125000"
        run(args=cmd, shell =True, stdout=PIPE, stderr=PIPE, check=False)

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
                ports = load(file, Loader = FullLoader)
            scpi_volt_meter = DrvScpiHandlerC(port = ports['voltage_multimeter'], \
                                              separator='\n', baudrate=38400, \
                                              timeout=1, write_timeout=1)
            self.__volt_meter = DrvBkDeviceC(handler = scpi_volt_meter)
            self.__volt_meter.set_mode(DrvBkModeE.VOLT_AUTO)
            scpi_curr_meter = DrvScpiHandlerC(port = ports['current_multimeter'], \
                                              separator='\n', baudrate=38400, \
                                              timeout=1, write_timeout=1)
            self.__curr_meter = DrvBkDeviceC(handler = scpi_curr_meter)
            self.__curr_meter.set_mode(DrvBkModeE.CURR_R2_A)
            #Source configuration
            scpi_ea = DrvScpiHandlerC(port = ports['source'], separator = '\n', \
                                      timeout = 0.8, write_timeout = 0.8, \
                                      parity = serial.PARITY_ODD, baudrate = 9600)
            self.__source = DrvEaDeviceC(scpi_ea)
            self.on_power()
            cmd = "sudo ip link set down can0"
            run(args=cmd, shell =True, stdout=PIPE, stderr=PIPE, check=False)
            cmd = "sudo ip link set up txqueuelen 1000000 can0 type can bitrate 125000"
            run(args=cmd, shell =True, stdout=PIPE, stderr=PIPE, check=False)
            #EPC configuration
            self.__can_queue = SysShdChanC(100000000)
            self.__can_queue.delete_until_last()
            # Flag to know if the can is working
            _working_can = Event()
            _working_can.set()
            #Create the thread for CAN
            can = DrvCanNodeC(self.__can_queue, _working_can)
            can.start()
            self.__epc = DrvEpcDeviceC(dev_id=0x00,
                                       device_handler=SysShdChanC(500),
                                       tx_can_queue=self.__can_queue)

            self.__epc.open()
            print("Power devices configured. EPC open.")

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
        TermC.check_wires()
        result_calib: ConfigResultE = ConfigResultE.ERROR
        #Check if the calibration has already been done
        info_path = ConfigWsC.get_info_file_path()
        if os.path.exists(info_path):
            with open(info_path, 'r', encoding="utf-8") as file:
                conf_dev = load(file, Loader = FullLoader)
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
            calib: DataFrame = self._obtain_values(mode = mode)
            #Obtain the parameters of the line
            axis_y = array(calib.iloc[:,1]).tolist() #Column of multimeter
            axis_x = array(calib.iloc[:,2]).tolist() #Column of EPC
            factor, offset = polyfit(axis_x, axis_y, 1)
            factor = factor * 4095
            result_calib = self._save_calib_data(mode = mode, data = calib, \
                                                 factor = round(factor), offset = round(offset))
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


    def _obtain_values(self, mode: PwrModeE) -> DataFrame:
        ''' Obtain voltage of multimeter and EPC.
        Args:
            - mode (PwrModeE): Type of calibration to be done.

        Returns:
            - result (DataFrame): Dataframe with the voltage of the source,
                                     voltage measured with the multimeter and
                                     the one measured with the EPC.
        Raises:
            - None
        '''
        val_min = _PwrParamsE.__getitem__(f"{mode.name}_MIN").value
        step    = _PwrParamsE.__getitem__(f"{mode.name}_STEP").value
        val_max = _PwrParamsE.__getitem__(f"{mode.name}_MAX").value
        name_columns = ['meas source', 'meas multimeter', 'meas EPC']

        result = DataFrame(columns = name_columns)
        val_to_send = val_min

        #Iteration to obtain the voltage or current of the multimeter and the EPC
        while val_to_send <= val_max:

            if mode is PwrModeE.VOLT_HS:
                self.__source.set_cv_mode(volt_ref = val_to_send, current_limit = 5000, channel = 1)
                while abs(val_to_send - self.__source.get_data(channel = 1).voltage) > _ERROR_RANGE:
                    sleep(0.1)

            if mode is PwrModeE.VOLT_LS:
                self.__source.set_cv_mode(volt_ref = val_to_send, current_limit = 1000, channel = 2)
                while abs(val_to_send - self.__source.get_data(channel = 2).voltage) > _ERROR_RANGE:
                    sleep(0.1)

            elif mode is PwrModeE.CURR:
                self.__epc.set_cc_mode(ref = val_to_send, limit_type = DrvEpcLimitE.TIME, \
                                       limit_ref = 8000)
                sleep(0.020)

            av_meter: list= []
            av_epc: list= []
            for _ in range(0,9, 1):
                #Data voltage high side calibration
                if mode is PwrModeE.VOLT_HS:
                    val_meter   = self.__volt_meter.get_data().voltage
                    val_epc     = self.__epc.get_elec_meas().hs_voltage

                #Data voltage low side calibration
                elif mode is PwrModeE.VOLT_LS:
                    val_meter   = self.__volt_meter.get_data().voltage
                    val_epc     = self.__epc.get_elec_meas().ls_voltage

                #Data current calibration
                elif mode is PwrModeE.CURR:
                    val_meter   = self.__curr_meter.get_data().current
                    val_epc     = self.__epc.get_elec_meas().ls_current

                if mode is PwrModeE.VOLT_HS:
                    max_meas_range = 15000
                    offset = 0
                elif mode is PwrModeE.VOLT_LS:
                    max_meas_range = 6000
                    offset = 0
                elif mode is PwrModeE.CURR:
                    max_meas_range = 33000
                    offset = -16000
                bits_epc = (val_epc - offset) * 4095 / max_meas_range
                av_meter.append(val_meter)
                av_epc.append(bits_epc)

            new_row = DataFrame([[val_to_send, round(median(av_meter)), round(median(av_epc))]], \
                                   columns = name_columns)
            result = concat([result,new_row], ignore_index=True)

            TermC.show_progress_bar(iteration = val_to_send - val_min, total = val_max - val_min)
            val_to_send += step

        # self.__source.disable()
        return result


    def _save_calib_data(self, mode: PwrModeE, data: DataFrame, factor: int, offset: int) \
        -> ConfigResultE:
        ''' Save the calibration data in a csv file and in a yaml file.
        Args:
            - mode (str): Type of calibration to be saved.
            - data (DataFrame): Dataframe with the voltage of the source,
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
                conf_dev = load(file, Loader = FullLoader)
            conf_dev['calib_data'][mode.name]['factor'] = factor
            conf_dev['calib_data'][mode.name]['offset'] = offset
            conf_dev['calib_data'][mode.name]['date'] = strftime("%d/%m/%Y %H:%M:%S")
            with open(info_path, 'w', encoding="utf-8") as file:
                dump(conf_dev, file)

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
