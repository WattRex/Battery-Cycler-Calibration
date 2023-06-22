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
from enum import Enum
import pandas as pd
import numpy as np
import statistics
import time
import yaml
#######################       THIRD PARTY IMPORTS        #######################


#######################          MODULE IMPORTS          #######################

#######################          PROJECT IMPORTS         #######################
from DRV.DRV_BK_PREC import *
from DRV.DRV_EA import *

#######################              ENUMS               #######################
config_calib = {'version':      {'hw': None, 'sw': None, 'dev': None, 's_n': None},
                'calib_data':   {'volt_hs': {'factor': None, 'offset': None, 'date': None},
                                 'volt_ls': {'factor': None, 'offset': None, 'date': None},
                                 'curr':    {'factor': None, 'offset': None, 'date': None}}}
class _DEFAULTS():
    ERROR_RANGE = 100 #mV

class _CALIB_DATA_e(Enum):
    VOLT_HS = 'volt_hs'
    VOLT_LS = 'volt_ls'
    CURR = 'curr'

class _Params_e(Enum):
    VOLT_HS_MIN = 10000 #mV
    VOLT_HS_MAX = 20000
    VOLT_HS_STEP = 1000
    VOLT_LS_MIN = 30000
    VOLT_LS_MAX = 40000
    VOLT_LS_STEP = 1000
    CURR_MIN = 6
    CURR_MAX = 7
    CURR_STEP = 8

dataaaa = {
    'voltage source': [30000, 31000, 32000, 33000, 34000, 35000, 36000, 37000, 38000, 39000, 40000],
    'voltage multimeter': [30007.7, 31019.6, 32018.1, 33018.4, 34015.5, 35012.7, 36022.4, 37020.5, 38015.2, 39019.9, 40018.7],
    'voltage EPC': [30040, 31060, 32120, 33007, 34030, 35056, 36020, 37000, 38030, 39100, 40000]
}

BORRAR = pd.DataFrame(dataaaa)

#######################              CLASSES             #######################
class DRV_EPC():
    pass

class PWR_CALIB_c():
    def __init__(self, source_port: str, multimeter_port: str, epc_number: str) -> None:
        self._source: DRV_EA_PS_c   = DRV_EA_PS_c(model = 'EA-PS 2384-05 B' , serial_port = source_port)
        self._meter: DRV_BK_Meter_c = DRV_BK_Meter_c(multimeter_port)
        self._epc: DRV_EPC          = epc_number
        self._epc_ser_number = epc_number

    def SetupCalibStation(self, serial_number):
        self._epc_ser_number = serial_number
        pass
    
    def CalibVoltHS(self):
        #calib: pd.DataFrame = self._calibVolts(v_min = _Params_e.VOLT_HS_MIN.value, step = _Params_e.VOLT_HS_STEP.value, v_max = _Params_e.VOLT_HS_MAX.value)
        calib = BORRAR
        line: tuple = self._parameters_line(calib)
        self._save_calib_data(type_cal = _CALIB_DATA_e.VOLT_HS.value, df = calib, factor = line[0], offset = line[1])

        
    def CalibVoltLS(self):
        #calib: pd.DataFrame = self._calibVolts(v_min = _Params_e.VOLT_LS_MIN.value, step = _Params_e.VOLT_LS_STEP.value, v_max = _Params_e.VOLT_LS_MAX.value)
        calib = BORRAR
        line: tuple = self._parameters_line(calib)
        self._save_calib_data(type_cal = _CALIB_DATA_e.VOLT_LS.value, df = calib, factor = line[0], offset = line[1])

    def CalibCurr(self):
        self._meter.setMode(DRV_BK_MODE_e.CURR_AUTO)


    def _calibVolts(self, v_min: int, step: int, v_max: int) -> pd.DataFrame:
        result = pd.DataFrame(columns=['voltage source', 'voltage multimeter', 'voltage EPC'])
        volt_source = v_min
        self._meter.setMode(DRV_BK_MODE_e.VOLT_AUTO)
        self._source.setOutput(True)
        while volt_source <= v_max:
            self._source.setCVMode(volt_source)
            time.sleep(5)
            while abs(volt_source - self._source.getVoltage()) > _DEFAULTS.ERROR_RANGE:
                time.sleep(0.5)
            
            av_volt_meter: list= []
            av_volt_epc: list= []
            for _ in range(0,10, 1):
                voltage_multimeter = self._meter.getMeas().voltage
                av_volt_meter.append(voltage_multimeter)
                av_volt_epc.append(0)
            result = pd.concat([result, pd.DataFrame([[volt_source, statistics.mean(av_volt_meter), statistics.mean(av_volt_epc)]],\
                                                             columns=['voltage source', 'voltage multimeter', 'voltage EPC'])], ignore_index=True)
            volt_source += step
        self._source.setOutput(False)
        return result


    def _parameters_line(self, df: pd.DataFrame) -> tuple:
        x = np.array(df['voltage multimeter'])
        y = np.array(df['voltage EPC'])
        factor, intersection = np.polyfit(x, y, 1)
        offset = intersection - (factor * x[0])
        factor = float(round(factor, 3))
        offset = float(round(offset, 3))
        return factor, offset


    def _save_calib_data(self, type_cal: str, df: pd.DataFrame, factor: int, offset: int):
        name_path_info = f"./PWR_CALIB/CALIBRATIONS/epc_calib_info_{self._epc_ser_number}.yaml"
        name_path_dates = f"./PWR_CALIB/CALIBRATIONS/epc_calib_{type_cal}_{self._epc_ser_number}.csv"

    
        if not os.path.exists(name_path_dates):
            df.to_csv(name_path_dates, index=False)

        if not os.path.exists(name_path_info):
            config = config_calib
            write_dates = True
        else:
            with open(name_path_info, 'r') as file:
                config = yaml.load(file, Loader=yaml.FullLoader)
                if config['calib_data'][type_cal]['factor'] == None or config['calib_data'][type_cal]['offset'] == None or config['calib_data'][type_cal]['date'] == None:
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
            config['version']['s_n'] = self._epc_ser_number
            config['calib_data'][type_cal]['factor'] = factor
            config['calib_data'][type_cal]['offset'] = offset
            config['calib_data'][type_cal]['date'] = time.strftime("%d/%m/%Y %H:%M:%S")
            with open(name_path_info, 'w') as file:
                yaml.dump(config, file)
                df.to_csv(name_path_dates, index=False)