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
import signal
import yaml
from pathlib import Path
from enum import Enum
#######################       THIRD PARTY IMPORTS        #######################


#######################          MODULE IMPORTS          #######################

from PWR_CALIB import PWR_CALIB_c
from STM_FLASH import EPC_CONF_c, STM_FLASH_c
#######################          PROJECT IMPORTS         #######################


#######################              ENUMS               #######################
class _OPTIONS_e(Enum):
    FLASH_ORIG_PROGR        = '1'
    CONF_DEV                = '2'
    CALIB_DEV               = '3'
    FLASH_WITH_CALIB_DATA   = '4'
    EXIT                    = '5'

class _OPTIONS_CALIB_e(Enum):
    VOLT_HS                 = '31'
    VOLT_LS                 = '32'
    CURR                    = '33'
    AN_TEMP                 = '34'
    AMB_TEMP                = '35'
    BODY_TEMP               = '36'


class _DEFAULTS():
    FILE_PATH_CONFIG = './CALIB_MAIN/config.yaml'

default_settings = {'device_version':  {'hw': None, 'sw': None, 'can_ID': None, 's_n': None},
                    'calib_data':      {'VOLT_HS': {'factor': None, 'offset': None, 'date': None},
                                        'VOLT_LS': {'factor': None, 'offset': None, 'date': None},
                                        'CURR':    {'factor': None, 'offset': None, 'date': None}}}

#######################              CLASSES             #######################
def _signal_handler(sig, frame):
    log.critical(f'You pressed Ctrl+C! If you want to exit the program, use the 5th option...')

def _readConfigPorts() -> dict:
    # Verificar si el archivo ya existe
    result = None
    if not os.path.exists(_DEFAULTS.FILE_PATH_CONFIG):
        print(f" File {_DEFAULTS.FILE_PATH_CONFIG} does not exist.")
    else:
        try:
            with open(_DEFAULTS.FILE_PATH_CONFIG, 'r') as archivo:
                result = yaml.load(archivo, Loader=yaml.FullLoader)
        except:
            print(f"Error reading file {_DEFAULTS.FILE_PATH_CONFIG}.")

    return result


def _option() -> Enum:
    print(f"Select an option:\n\
    1. Flash original program.\n\
    2. Configure device.\n\
    3. Calibrate device.\n\
    4. Flash with calibration data.\n\
    5. Exit.")
    try:
        result = _OPTIONS_e(input(f"Chosen option: "))
        if result is _OPTIONS_e.CALIB_DEV:
            print(f"Select an option of calibration:\n\
            1. Voltage high side.\n\
            2. Voltage low side.\n\
            3. Current low side.\n\
            4. Anodo temperature.\n\
            5. Ambient temperature.\n\
            6. Body temperature.")
            try:
                op_cal = input(f"Chosen option: ")
                result = _OPTIONS_CALIB_e(_OPTIONS_e.CALIB_DEV.value + op_cal)
            except:
                print(f"Invalid option of calibration.")
    except:
        print(f"Invalid option.")
        result = None
    return result


def _configDevice() -> int:
    #TODO: Can pedir y mostrar la info de la placa que tienes conectada
    while True:
        try:
            epc_sn = int(input(f"serial number of EPC: ")) #TODO: validar numero de serie
            break
        except:
            print(f"Invalid data.")
    
    name_path = f"CALIB_MAIN/DATAS/data_{epc_sn}"
    if not os.path.exists(name_path):
        Path(name_path).mkdir(parents=True, exist_ok=True)
        
    name_path_info = f"{name_path}/epc_calib_info_{epc_sn}.yaml"
    if os.path.exists(name_path_info):
        with open(name_path_info, 'r') as file:
            conf_dev = yaml.load(file, Loader=yaml.FullLoader)
    else:
        conf_dev: dict = default_settings

    while True:
        try:
            conf_dev['device_version']['hw']        = int(input(f"Hardware version: "))
            conf_dev['device_version']['sw']        = int(input(f"Software version: "))
            conf_dev['device_version']['can_ID']    = int(input(f"CAN ID: "))
            conf_dev['device_version']['s_n']       = epc_sn
            break
        except:
            print(f"Invalid data.")
    with open(name_path_info, 'w') as file:
        yaml.dump(conf_dev, file)
        print(f"Configuration done")

    EPC_CONF_c(serial_number = epc_sn)
    return epc_sn

def main():
    ports: dict = _readConfigPorts()
    
    option = _OPTIONS_e.CONF_DEV
    while option is not _OPTIONS_e.EXIT:
        try:
            if option == _OPTIONS_e.FLASH_ORIG_PROGR:
                calib.SetupCalibStation(serial_number = epc_sn)
            elif option == _OPTIONS_e.CONF_DEV:
                epc_sn = _configDevice()
                calib: PWR_CALIB_c = PWR_CALIB_c(source_port = ports['source_port'], multimeter_port = ports['multimeter_port'], epc_sn = epc_sn)
            elif option == _OPTIONS_e.FLASH_WITH_CALIB_DATA:
                pass
            elif option == _OPTIONS_CALIB_e.VOLT_HS:
                calib.CalibVoltHS()
            elif option == _OPTIONS_CALIB_e.VOLT_LS:
                calib.CalibVoltLS()
            elif option == _OPTIONS_CALIB_e.CURR:
                calib.CalibCurr()
            elif option == _OPTIONS_CALIB_e.AN_TEMP:
                pass
            elif option == _OPTIONS_CALIB_e.AMB_TEMP:
                pass
            elif option == _OPTIONS_CALIB_e.BODY_TEMP:
                pass

        except Exception as e:
            print(f"Error in program: {e}.")
        option = _option()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, _signal_handler)
    main()
    print("End of program.")