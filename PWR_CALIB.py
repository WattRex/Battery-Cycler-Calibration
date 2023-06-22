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
import statistics
import time

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



#######################              CLASSES             #######################
class DRV_EPC():
    pass

class PWR_CALIB_c():
    def __init__(self, source_port: str, multimeter_port: str, epc_number: str) -> None:
        self._source: DRV_EA_PS_c   = DRV_EA_PS_c(model = 'EA-PS 2384-05 B' , serial_port = source_port)
        self._meter: DRV_BK_Meter_c = DRV_BK_Meter_c(multimeter_port)
        self._epc: DRV_EPC          = epc_number
        self._epc_ser_number = None

    def SetupCalibStation(self, serial_number):
        self._epc_ser_number = serial_number
        pass
    
    def CalibVoltHS(self):
        self._calibVolts(v_min = _Params_e.VOLT_HS_MIN.value, step = _Params_e.VOLT_HS_STEP.value, v_max = _Params_e.VOLT_HS_MAX.value)
    
    def CalibVoltLS(self):
        self._calibVolts(v_min = _Params_e.VOLT_LS_MIN.value, step = _Params_e.VOLT_LS_STEP.value, v_max = _Params_e.VOLT_LS_MAX.value)

    def CalibCurr(self):
        self._meter.setMode(DRV_BK_MODE_e.CURR_AUTO)
        pass

    def _calibVolts(self, v_min: int, step: int, v_max: int):
        total_meas = pd.DataFrame(columns=['voltage source', ' voltage multimeter'])

        print(f'lelleleleelga')
        self._meter.setMode(DRV_BK_MODE_e.VOLT_AUTO)
        volt_source = v_min
        
        self._source.setOutput(True)
        while volt_source <= v_max:
            self._source.setCVMode(volt_source)
            time.sleep(5)
            while abs(volt_source - self._source.getVoltage()) > _DEFAULTS.ERROR_RANGE:
                time.sleep(0.5)
            
            i = 0
            av_voltage = []
            while i < 10:
                voltage_multimeter = self._meter.getMeas().voltage
                av_voltage = av_voltage.append(voltage_multimeter)
                i += 1
            total_meas = pd.concat([total_meas, pd.DataFrame([[volt_source, statistics.mean(av_voltage)]], columns=['voltage source', ' voltage multimeter'])], ignore_index=True)
            print(total_meas)
            print('\n')
            volt_source += step


        self._source.setOutput(False)
        

# def main():
#     multimeter = DRV_BK_Meter_c('/dev/ttyUSB0')
#     source = DRV_EA_PS_c(model = 'EA-PS 2384-05 B' , serial_port = source_port)
    
    
#     source.setCVMode(8 * 1000)
#     source.setOutput(True)
#     time.sleep(5)
#     print( source.getMeasures())
#     print('VOLTAJE: ', source.getVoltage())


#     multimeter.setMode(DRV_BK_MODE_e.VOLT_AUTO)
#     meas : DRV_BK_Measure_c = multimeter.getMeas()
#     log.info(f"Meas voltaje: {meas.voltage}, corriente: {meas.current}, mode: {meas.mode}, status: {meas.status}")



# if __name__ == '__main__':
#     main()