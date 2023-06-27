#!/usr/bin/python3

#######################        MANDATORY IMPORTS         #######################
import sys, os
sys.path.append(os.getcwd())  #get absolute path
from pathlib import Path

#######################      LOGGING CONFIGURATION       #######################
from SYS.SYS_LOG import SYS_LOG_Logger_c, SYS_LOG_LoggerGetModuleLogger
if __name__ == '__main__':
    cycler_logger = SYS_LOG_Logger_c('./SYS/SYS_LOG/logginConfig.conf')
log = SYS_LOG_LoggerGetModuleLogger(__name__, config_by_module_filename="./log_config.yaml")

#######################         GENERIC IMPORTS          #######################

import time
from enum import Enum
import pandas as pd
import numpy as np
from statistics import mean
import yaml

#######################       THIRD PARTY IMPORTS        #######################


#######################          MODULE IMPORTS          #######################

#######################          PROJECT IMPORTS         #######################
from TERMINAL import printProgressBar
from DRV.DRV_BK_PREC import *
from DRV.DRV_EA import DRV_EA_PS_Source_c, DRV_EA_PS_c
from .WS_CONFIG import *
from STM_FLASH import EPC_CONF_c

#######################              ENUMS               #######################
class _DEFAULTS():
    ERROR_RANGE = 50 #mUnits


class _CALIB_e(Enum):
    VOLT_HS = 'VOLT_HS'
    VOLT_LS = 'VOLT_LS'
    CURR = 'CURR'

class _Params_e(Enum):
    VOLT_HS_MIN = 10000 #mV
    VOLT_HS_MAX = 15000
    VOLT_HS_STEP = 1000
    VOLT_LS_MIN = 30000
    VOLT_LS_MAX = 35000
    VOLT_LS_STEP = 1000
    CURR_MIN = 300
    CURR_MAX = 350
    CURR_STEP = 10


#######################              CLASSES             #######################
class DRV_EPC():
    pass

class PWR_CALIB_c():
    ''' Class to calibrate the voltage and current of EPC.
    Args:
        source_port (str): Serial port of the power supply.
        multimeter_port (str): Serial port of the multimeter.
        epc_number (str): Serial number of the EPC.
    '''
    def __init__(self, source_port: DRV_EA_PS_c, multimeter_port: DRV_BK_Meter_c) -> None:
        self._source: DRV_EA_PS_c   = source_port
        self._meter: DRV_BK_Meter_c = multimeter_port
        self._epc: DRV_EPC          = 0 #TODO: QUE VA??
    

    def CalibVoltHS(self) -> None:
        ''' Calibration of the high side voltage of the model.
        Args:
            - None
        Returns:
            - None
        Raises:
            - None
        '''
        log.info(f"Model high side voltage calibration begins.")
        check_write = self._chekExistData(type_cal = _CALIB_e.VOLT_HS)
        if check_write:
            calib = self._calibration(type_cal = _CALIB_e.VOLT_HS)
            line: tuple = self._parametersLine(calib)
            self._saveCalibData(type_cal = _CALIB_e.VOLT_HS, df = calib, factor = line[0], offset = line[1])

    
    def CalibVoltLS(self) -> None:
        ''' Calibration of the low side voltage of the model.
        Args:
            - None
        Returns:
            - None
        Raises:
            - None
        '''
        log.info(f"Model low side voltage calibration begins.")
        check_write = self._chekExistData(type_cal = _CALIB_e.VOLT_LS)
        if check_write:
            calib = self._calibration(type_cal = _CALIB_e.VOLT_LS)
            line: tuple = self._parametersLine(calib)
            self._saveCalibData(type_cal = _CALIB_e.VOLT_LS, df = calib, factor = line[0], offset = line[1])

    def CalibCurr(self):
        '''Calibration of the current of the model.
        Args:
            - None
        Returns:
            - None
        Raises:
            - None
        '''
        log.info(f"Model current calibration begins.")
        check_write = self._chekExistData(type_cal = _CALIB_e.CURR)
        if check_write:
            calib = self._calibration(type_cal = _CALIB_e.CURR)
            line: tuple = self._parametersLine(calib)
            self._saveCalibData(type_cal = _CALIB_e.CURR, df = calib, factor = line[0], offset = line[1])


    def _calibration(self, type_cal: _CALIB_e) -> pd.DataFrame:
        ''' Obtain voltage of multimeter and EPC.
        Args:
            - type_cal (_CALIB_e): Type of calibration to be done.

        Returns:
            - result (pd.DataFrame): Dataframe with the voltage of the source, voltage measured with the multimeter and the one measured with the EPC.
        Raises:
            - None
        '''
        val_min = _Params_e.__getitem__(f"{type_cal.value}_MIN").value
        step = _Params_e.__getitem__(f"{type_cal.value}_STEP").value
        val_max = _Params_e.__getitem__(f"{type_cal.value}_MAX").value

        if type_cal is _CALIB_e.VOLT_HS or type_cal is _CALIB_e.VOLT_LS:
            type_columns = ['voltage source', 'voltage multimeter', 'voltage EPC']
            self._meter.setMode(DRV_BK_MODE_e.VOLT_AUTO)
        else:
            type_columns = ['current source', 'current multimeter', 'current EPC']
            self._meter.setMode(DRV_BK_MODE_e.CURR_R2A)
        result = pd.DataFrame(columns = type_columns)

        val_source = val_min
        self._source.setOutput(True)
        while val_source <= val_max:
            time.sleep(2)
            if type_cal is _CALIB_e.VOLT_HS or type_cal is _CALIB_e.VOLT_LS:
                self._source.setCVMode(val_source)
                while abs(val_source - self._source.getVoltage()) > _DEFAULTS.ERROR_RANGE:
                    time.sleep(0.5)
            else:
                self._source.setCCMode(val_source)
                current = self._source.getCurrent()
                while abs(val_source - self._source.getCurrent()) > _DEFAULTS.ERROR_RANGE:
                    time.sleep(0.5)
            av_meter: list= []
            av_epc: list= []
            for _ in range(0,9, 1):
                if type_cal == _CALIB_e.VOLT_HS or type_cal == _CALIB_e.VOLT_LS:
                    val_meter = self._meter.getMeas().voltage
                else:
                    val_meter = self._meter.getMeas().current
                av_meter.append(val_meter)
                av_epc.append(val_meter)    #TODO: Cambiarlo por lo obtenido del EPC
            result = pd.concat([result, pd.DataFrame([[val_source, int(mean(av_meter)), int(mean(av_epc))]], columns = type_columns)], ignore_index=True)

            printProgressBar(iteration = (val_source - val_min), total = (val_max - val_min))
            val_source += step
        self._source.setOutput(False)
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


    def _chekExistData(self, type_cal: _CALIB_e) -> bool:
        ''' Check if the calibration data already exists.
        Args:
            - type_cal (_CALIB_e): Type of calibration to be done.
        Returns:
            - result (bool): True if the calibration data already exists, False if not.
        Raises:
            - None
        '''
        global INFO_FILE_PATH
        type_cal = type_cal.value
        with open(INFO_FILE_PATH, 'r') as file:
            conf_dev = yaml.load(file, Loader=yaml.FullLoader)
            if conf_dev['calib_data'][type_cal]['factor'] == None and conf_dev['calib_data'][type_cal]['offset'] == None and conf_dev['calib_data'][type_cal]['date'] == None:
                exist_dates = True
            else:
                exist_dates = False
        if exist_dates:
            while True:
                try:
                    check = str(input(f"Calibration data for {type_cal} already exists. ¿Do you want to replace it? (y/n): "))
                    if check == 'y' or check == 'Y':
                        result = True
                        break
                    elif check == 'n' or check == 'N':
                        result = False
                        break
                    else:
                        log.error("Invalid option.")
                except:
                    log.error("Invalid option.")
        else:
            result = True
        return result

    def _saveCalibData(self, type_cal: _CALIB_e, df: pd.DataFrame, factor: int, offset: int) -> None:
        ''' Save the calibration data in a csv file and in a yaml file.
        Args:
            - type_cal (str): Type of calibration to be saved.
            - df (pd.DataFrame): Dataframe with the voltage of the source, voltage measured with the multimeter and the one measured with the EPC.
            - factor (int): Factor of the line obtain.
            - offset (int): Offset of the line obtain.
        Returns:
            - None
        Raises:
            - None
        '''
        type_cal = type_cal.value
        global INFO_FILE_PATH, V_LS_CALIB_FILE_PATH, V_HS_CALIB_FILE_PATH, I_CALIB_FILE_PATH
        with open(INFO_FILE_PATH, 'r') as file:
            conf_dev = yaml.load(file, Loader=yaml.FullLoader)

        conf_dev['calib_data'][type_cal]['factor'] = factor
        conf_dev['calib_data'][type_cal]['offset'] = offset
        conf_dev['calib_data'][type_cal]['date'] = time.strftime("%d/%m/%Y %H:%M:%S")
        with open(INFO_FILE_PATH, 'w') as file:
            yaml.dump(conf_dev, file)
        
        if type_cal == _CALIB_e.VOLT_HS:
            calib_file =  V_HS_CALIB_FILE_PATH
        elif type_cal == _CALIB_e.VOLT_LS:
            calib_file = V_LS_CALIB_FILE_PATH
        elif type_cal == _CALIB_e.CURR:
            calib_file = I_CALIB_FILE_PATH
        df.to_csv(calib_file, index=False)