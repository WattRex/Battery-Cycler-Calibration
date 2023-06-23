#!/usr/bin/python3

#######################        MANDATORY IMPORTS         #######################
import sys, os
sys.path.append(os.getcwd())  #get absolute path

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
from DRV.DRV_BK_PREC import *
from DRV.DRV_EA import DRV_EA_PS_Source_c, DRV_EA_PS_c

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
    def __init__(self, source_port: str, multimeter_port: str, epc_sn: str) -> None:
        self._source: DRV_EA_PS_c   = DRV_EA_PS_c(model = 'EA-PS 2384-05 B' , serial_port = source_port)
        self._meter: DRV_BK_Meter_c = DRV_BK_Meter_c(multimeter_port)
        self._epc: DRV_EPC          = 0 #TODO: QUE VA??
        self._epc_sn: int = epc_sn


    def SetupCalibStation(self, serial_number: int):
        ''' Sets up the calibration serial_number.
        Args:
            - serial_number (str): Serial number of the EPC.
        Returns:
            - None
        Raises:
            - #TODO: ¿¿¿¿????
        '''
        self._epc_sn = serial_number
        pass
    
    def CalibVoltHS(self) -> None:
        ''' Calibration of the high side voltage of the model.
        Args:
            - None
        Returns:
            - None
        Raises:
            - #TODO: ¿¿¿¿????
        '''
        calib = self._calibration(type_cal = _CALIB_e.VOLT_HS)
        line: tuple = self._parameters_line(calib)
        self._save_calib_data(type_cal = _CALIB_e.VOLT_HS, df = calib, factor = line[0], offset = line[1])

    
    def CalibVoltLS(self) -> None:
        ''' Calibration of the low side voltage of the model.
        Args:
            - None
        Returns:
            - None
        Raises:
            - #TODO: ¿¿¿¿????
        '''
        calib = self._calibration(type_cal = _CALIB_e.VOLT_LS)
        line: tuple = self._parameters_line(calib)
        self._save_calib_data(type_cal = _CALIB_e.VOLT_LS, df = calib, factor = line[0], offset = line[1])

    def CalibCurr(self):
        '''Calibration of the current of the model.
        Args:
            - None
        Returns:
            - None
        Raises:
            - #TODO: ¿¿¿¿????
        '''
        calib = self._calibration(type_cal = _CALIB_e.CURR)
        line: tuple = self._parameters_line(calib)
        self._save_calib_data(type_cal = _CALIB_e.CURR, df = calib, factor = line[0], offset = line[1])

    def _calibration(self, type_cal: _CALIB_e) -> pd.DataFrame:
        ''' Obtain voltage of multimeter and EPC.
        Args:
            - type_cal (_CALIB_e): Type of calibration to be done.

        Returns:
            - result (pd.DataFrame): Dataframe with the voltage of the source, voltage measured with the multimeter and the one measured with the EPC.
        Raises:
            - #TODO: ¿¿¿¿?????
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

            val_source += step
        self._source.setOutput(False)
        return result


    def _parameters_line(self, df: pd.DataFrame) -> tuple:
        ''' Obtain the parameters of the line that best fits the data.
        Args:
            - df (pd.DataFrame): Dataframe with the voltage of the source, voltage measured with the multimeter and the one measured with the EPC.
        Retuns (tuple):
            - factor (int): Factor of the line obtain.
            - offset (int): Offset of the line obtain.
        Raises:
            - #TODO: ¿¿¿¿????
        '''
        x = np.array(df.iloc[:,1]).tolist() #Column of multimeter
        y = np.array(df.iloc[:,2]).tolist() #Column of EPC
        

        factor, intersection = np.polyfit(x, y, 1)
        offset = intersection - (factor * x[0])
        factor = float(round(factor, 3))
        offset = float(round(offset, 3))
        return factor, offset


    def _save_calib_data(self, type_cal: _CALIB_e, df: pd.DataFrame, factor: int, offset: int) -> None:
        ''' Save the calibration data in a csv file and in a yaml file.
        Args:
            - type_cal (str): Type of calibration to be saved.
            - df (pd.DataFrame): Dataframe with the voltage of the source, voltage measured with the multimeter and the one measured with the EPC.
            - factor (int): Factor of the line obtain.
            - offset (int): Offset of the line obtain.
        Returns:
            - None
        Raises:
            - #TODO: ¿¿¿¿????
        '''
        type_cal = type_cal.value
        name_path = f"CALIB_MAIN/DATAS/data_{self._epc_sn}"
        name_path_info = f"{name_path}/epc_calib_info_{self._epc_sn}.yaml"
        name_path_dates = f"{name_path}/epc_calib_{type_cal}_{self._epc_sn}.csv"
        with open(name_path_info, 'r') as file:
            conf_dev = yaml.load(file, Loader=yaml.FullLoader)
            if conf_dev['calib_data'][type_cal]['factor'] == None or conf_dev['calib_data'][type_cal]['offset'] == None or conf_dev['calib_data'][type_cal]['date'] == None:
                with_dates = False
                write_dates = True
            else:
                with_dates = True
        if with_dates:
            while True:
                try:
                    check = str(input(f"Calibration data for {type_cal} already exists. ¿Do you want to replace it? (y/n): "))
                    if check == 'y' or check == 'Y':
                        write_dates = True
                        break
                    elif check == 'n' or check == 'N':
                        write_dates = False
                        break
                    else:
                        print("Invalid option.")
                except:
                    print("Invalid option.")

        if write_dates:
            conf_dev['calib_data'][type_cal]['factor'] = factor
            conf_dev['calib_data'][type_cal]['offset'] = offset
            conf_dev['calib_data'][type_cal]['date'] = time.strftime("%d/%m/%Y %H:%M:%S")
            with open(name_path_info, 'w') as file:
                yaml.dump(conf_dev, file)
                df.to_csv(name_path_dates, index=False)