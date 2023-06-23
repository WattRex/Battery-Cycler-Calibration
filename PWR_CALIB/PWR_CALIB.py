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

    def SetupCalibStation(self, serial_number: str):
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
        #calib: pd.DataFrame = self._calibVolts(v_min = _Params_e.VOLT_HS_MIN.value, step = _Params_e.VOLT_HS_STEP.value, v_max = _Params_e.VOLT_HS_MAX.value)
        calib = BORRAR
        line: tuple = self._parameters_line(calib)
        self._save_calib_data(type_cal = _CALIB_DATA_e.VOLT_HS.value, df = calib, factor = line[0], offset = line[1])

        
    def CalibVoltLS(self) -> None:
        ''' Calibration of the low side voltage of the model.
        Args:
            - None
        Returns:
            - None
        Raises:
            - #TODO: ¿¿¿¿????
        '''
        #calib: pd.DataFrame = self._calibVolts(v_min = _Params_e.VOLT_LS_MIN.value, step = _Params_e.VOLT_LS_STEP.value, v_max = _Params_e.VOLT_LS_MAX.value)
        calib = BORRAR
        line: tuple = self._parameters_line(calib)
        self._save_calib_data(type_cal = _CALIB_DATA_e.VOLT_LS.value, df = calib, factor = line[0], offset = line[1])

    def CalibCurr(self):
        '''Calibration of the current of the model.
        Args:
            - None
        Returns:
            - None
        Raises:
            - #TODO: ¿¿¿¿????
        '''
        self._meter.setMode(DRV_BK_MODE_e.CURR_AUTO)


    def _calibVolts(self, v_min: int, step: int, v_max: int) -> pd.DataFrame:
        ''' Obtain voltage of multimeter and EPC.
        Args:
            - v_min (int): Minimum voltage to be measured.
            - step (int): Step between measurements.
            - v_max (int): Maximum voltage to be measured.

        Returns:
            - result (pd.DataFrame): Dataframe with the voltage of the source, voltage measured with the multimeter and the one measured with the EPC.
        Raises:
            - #TODO: ¿¿¿¿????
        '''
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
            for _ in range(0,9, 1):
                voltage_multimeter = self._meter.getMeas().voltage
                av_volt_meter.append(voltage_multimeter)
                av_volt_epc.append(voltage_multimeter) #TODO: Cambiarlo por lo obtenido del EPC
            av_volt_meter = int(statistics.mean(av_volt_meter))
            av_volt_epc = int(statistics.mean(av_volt_epc))
            result = pd.concat([result, pd.DataFrame([[volt_source, av_volt_meter, av_volt_epc]],\
                                                    columns=['voltage source', 'voltage multimeter', 'voltage EPC'])], ignore_index=True)
            volt_source += step
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
        x = np.array(df['voltage multimeter']).tolist()
        y = np.array(df['voltage EPC']).tolist()
        
        factor, intersection = np.polyfit(x, y, 1)
        offset = intersection - (factor * x[0])
        factor = float(round(factor, 3))
        offset = float(round(offset, 3))
        return factor, offset


    def _save_calib_data(self, type_cal: str, df: pd.DataFrame, factor: int, offset: int) -> None:
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