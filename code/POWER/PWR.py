#!/usr/bin/python3

#######################        MANDATORY IMPORTS         #######################
import sys, os
sys.path.append(os.getcwd())  #get absolute path

#######################      LOGGING CONFIGURATION       #######################
from SYS.SYS_LOG import SYS_LOG_Logger_c, SYS_LOG_LoggerGetModuleLogger
if __name__ == '__main__':
    root_logger = SYS_LOG_Logger_c('./SYS/SYS_LOG/logginConfig.conf')
log = SYS_LOG_LoggerGetModuleLogger(__name__, config_by_module_filename="./CONFIG/log_config.yaml")

#######################         GENERIC IMPORTS          #######################
from enum import Enum
import pandas as pd
import numpy as np
from statistics import mean
import yaml
from time import sleep, strftime
#######################       THIRD PARTY IMPORTS        #######################


#######################          MODULE IMPORTS          #######################
from CONFIG import *
from TERM import TERM_c
from DRV.DRV_BK_PREC import *
from DRV.DRV_EA import *

#######################          PROJECT IMPORTS         #######################


#######################              ENUMS               #######################
_ERROR_RANGE = 50 #mUnits

class PWR_Mode_e(Enum):
    VOLT_HS     = 0
    VOLT_LS     = 1
    CURR        = 2
    TEMP_ANOD   = 3
    TEMP_AMB    = 4
    TEMP_BODY   = 5
    NONE        = 6


class _PWR_Params_e(Enum):
    VOLT_HS_MIN = 10000 #mV #TODO: check values
    VOLT_HS_MAX = 12000 #mV #TODO: check values #15000
    VOLT_HS_STEP = 1000 #TODO: check values
    VOLT_LS_MIN = 30000 #mV #TODO: check values
    VOLT_LS_MAX = 35000 #mV #TODO: check values
    VOLT_LS_STEP = 1000 #TODO: check values
    CURR_MIN = 300      #mA #TODO: check values
    CURR_MAX = 350      #mA #TODO: check values
    CURR_STEP = 10      #TODO: check values

#######################              CLASSES             #######################
class PWR_c():
    '''Class to manage the power devices.
    '''
    def __init__(self) -> None:
        self.__source: DRV_EA_PS_c      = None
        self.__meter: DRV_BK_Meter_c    = None
        self.__epc                      = None
        self._configPowerDevices()


    def calibVoltHS(self) -> CONFIG_Result_e:
        '''Calibrate the high voltage source.
        Args:
            - None
        Returns:
            - result_calib (CONFIG_Result_e): Result of the calibration.
        Raises:
            - None
        '''
        result = self._stepsOfCalibration(mode = PWR_Mode_e.VOLT_HS)
        return result


    def calibVoltLS(self) -> CONFIG_Result_e:
        '''Calibrate the low voltage source.
        Args:
            - None
        Returns:
            - result (CONFIG_Result_e): Result of the calibration.
        Raises:
            - None
        '''
        result = self._stepsOfCalibration(mode = PWR_Mode_e.VOLT_LS)
        return result

    def calibCurr(self) -> CONFIG_Result_e:
        '''Calibrate the current source.
        Args:
            - None
        Returns:
            - result (CONFIG_Result_e): Result of the calibration.
        Raises:
            - None
        '''
        result = self._stepsOfCalibration(mode = PWR_Mode_e.CURR)
        return result


    def _configPowerDevices(self) -> None:
        '''Configure the DRV devices.
        Args:
            - None
        Returns:
            - None
        Raises:
            - None
        '''
        ports_path = CONFIG_WS_c.getFileConfPorts()
        if os.path.exists(ports_path):
            with open(ports_path, 'r') as file:
                ports = yaml.load(file, Loader=yaml.FullLoader)
            try:
                self.__source: DRV_EA_PS_c   = DRV_EA_PS_c(model = 'EA-PS 2384-05 B' , serial_port = ports['source_port'])
                self.__meter: DRV_BK_Meter_c = DRV_BK_Meter_c(serial_port = ports['multimeter_port'])
            except:
                log.error(f"Error opening ports.")
        else:
            log.error(f"File {ports_path} does not exist.")


    def _stepsOfCalibration(self, mode: PWR_Mode_e) -> CONFIG_Result_e:
        '''Steps of calibration.
        Args:
            - mode (PWR_Mode_e): Type of calibration to be done.
        Returns:
            - result_calib (CONFIG_Result_e): Result of the calibration.
        Raises:
            - None
        '''
        result_calib: CONFIG_Result_e = CONFIG_Result_e.Error
        if self._rewriteCalib(mode = mode):
            calib: pd.DataFrame = self._obtainValues(mode = mode)
            line: tuple = self._parametersLine(calib)
            result_calib = self._saveCalibData(mode = mode, df = calib, factor = line[0], offset = line[1])
            if result_calib == CONFIG_Result_e.NoError:
                log.info(f"Calibration of {mode.name} finished.")
            else:
                log.error(f"Calibration of {mode.name} failed.")
        else:
            log.info(f"Calibration of {mode.name} canceled.")

        return result_calib


    def _rewriteCalib(self, mode: PWR_Mode_e) -> bool:
        ''' Check if the calibration data already exists.
        Args:
            - mode (PWR_Mode_e): Type of calibration to be done.
        Returns:
            - result (bool): True if the calibration data already exists, False if not.
        Raises:
            - None
        '''
        info_path = CONFIG_WS_c.getInfoFilePath() 

        if os.path.exists(info_path):
            with open(info_path, 'r') as file:
                conf_dev = yaml.load(file, Loader=yaml.FullLoader)
                if conf_dev['calib_data'][mode.name]['factor'] == None and conf_dev['calib_data'][mode.name]['offset'] == None and conf_dev['calib_data'][mode.name]['date'] == None:
                    exist_dates = False
                else:
                    exist_dates = True
            if exist_dates:
                while True:
                    try:
                        check = str(input(f"Calibration data for {mode.name} already exists. ¿Do you want to replace it? (y/n): ")).lower()
                        if check == 'y':
                            result = True
                            break
                        elif check == 'n':
                            result = False
                            break
                        else:
                            print("Invalid option.")
                    except:
                        print("Invalid option.")
            else:
                result = True
        else:
            log.error(f"File {info_path} does not exist.")
        return result


    def _obtainValues(self, mode: PWR_Mode_e) -> pd.DataFrame:
        ''' Obtain voltage of multimeter and EPC.
        Args:
            - mode (PWR_Mode_e): Type of calibration to be done.

        Returns:
            - result (pd.DataFrame): Dataframe with the voltage of the source, voltage measured with the multimeter and the one measured with the EPC.
        Raises:
            - None
        '''
        val_min = _PWR_Params_e.__getitem__(f"{mode.name}_MIN").value
        step = _PWR_Params_e.__getitem__(f"{mode.name}_STEP").value
        val_max = _PWR_Params_e.__getitem__(f"{mode.name}_MAX").value
        
        if mode is PWR_Mode_e.VOLT_HS or mode is PWR_Mode_e.VOLT_LS:
            type_columns = ['voltage source', 'voltage multimeter', 'voltage EPC']
            self.__meter.setMode(DRV_BK_MODE_e.VOLT_AUTO)
        elif mode is PWR_Mode_e.CURR:
            type_columns = ['current source', 'current multimeter', 'current EPC']
            self.__meter.setMode(DRV_BK_MODE_e.CURR_R2A)
        result = pd.DataFrame(columns = type_columns)

        val_source = val_min
        self.__source.setOutput(True)

        #Iteration to obtain the voltage or current of the multimeter and the EPC
        while val_source <= val_max:
            sleep(2)
            if mode is PWR_Mode_e.VOLT_HS or mode is PWR_Mode_e.VOLT_LS:
                self.__source.setCVMode(val_source)
                while abs(val_source - self.__source.getVoltage()) > _ERROR_RANGE:
                    sleep(0.5)
            elif mode is PWR_Mode_e.CURR:
                self.__source.setCCMode(val_source)
                current = self.__source.getCurrent()
                while abs(val_source - self.__source.getCurrent()) > _ERROR_RANGE:
                    sleep(0.5)
            av_meter: list= []
            av_epc: list= []
            for _ in range(0,9, 1):
                if mode == PWR_Mode_e.VOLT_HS or mode == PWR_Mode_e.VOLT_LS:
                    val_meter = self.__meter.getMeas().voltage
                elif mode == PWR_Mode_e.CURR:
                    val_meter = self.__meter.getMeas().current
                av_meter.append(val_meter)
                av_epc.append(val_meter)    #TODO: Cambiarlo por lo obtenido del EPC
            result = pd.concat([result, pd.DataFrame([[val_source, int(mean(av_meter)), int(mean(av_epc))]], columns = type_columns)], ignore_index=True)

            TERM_c.showProgressBar(iteration = (val_source - val_min), total = (val_max - val_min))
            val_source += step
        self.__source.setOutput(False)
        return result


    def _parametersLine(self, df: pd.DataFrame) -> tuple:
        ''' Obtain the parameters of the line that best fits the data.
        Args:
            - df (pd.DataFrame): Dataframe with the voltage of the source, voltage measured with the multimeter and the one measured with the EPC.
        Retuns (tuple):
            - factor (int): Factor of the line obtain.
            - offset (int): Offset of the line obtain.
        Raises:
            - None
        '''
        x = np.array(df.iloc[:,1]).tolist() #Column of multimeter
        y = np.array(df.iloc[:,2]).tolist() #Column of EPC

        factor, intersection = np.polyfit(x, y, 1)
        offset = intersection - (factor * x[0])
        factor = float(round(factor, 3))
        offset = float(round(offset, 3))
        
        return factor, offset


    def _saveCalibData(self, mode: PWR_Mode_e, df: pd.DataFrame, factor: int, offset: int) -> CONFIG_Result_e:
        ''' Save the calibration data in a csv file and in a yaml file.
        Args:
            - mode (str): Type of calibration to be saved.
            - df (pd.DataFrame): Dataframe with the voltage of the source, voltage measured with the multimeter and the one measured with the EPC.
            - factor (int): Factor of the line obtain.
            - offset (int): Offset of the line obtain.
        Returns:
            - result (CONFIG_Result_e): Result of the calibration.
        Raises:
            - None
        '''
        result: CONFIG_Result_e = CONFIG_Result_e.Error

        info_path = CONFIG_WS_c.getInfoFilePath() 
        if os.path.exists(info_path):
            with open(info_path, 'r') as file:
                conf_dev = yaml.load(file, Loader=yaml.FullLoader)
            conf_dev['calib_data'][mode.name]['factor'] = factor
            conf_dev['calib_data'][mode.name]['offset'] = offset
            conf_dev['calib_data'][mode.name]['date'] = strftime("%d/%m/%Y %H:%M:%S")
            with open(info_path, 'w') as file:
                yaml.dump(conf_dev, file)
            
            if mode == PWR_Mode_e.VOLT_HS:
                calib_file = CONFIG_WS_c.getVoltHighSidePath()
            elif mode == PWR_Mode_e.VOLT_LS:
                calib_file = CONFIG_WS_c.getVoltLowSidePath()
            elif mode == PWR_Mode_e.CURR:
                calib_file = CONFIG_WS_c.getCalibCurrentPath()

            df.to_csv(calib_file, index=False)
            result = CONFIG_Result_e.NoError
        else:
            log.error(f"File {info_path} does not exist.")
        return result