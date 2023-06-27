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
from TERMINAL import clear_terminal, print_intro
from PWR_CALIB import PWR_CALIB_c
from STM_FLASH import EPC_CONF_c, STM_FLASH_c
from DRV.DRV_EA import DRV_EA_PS_c
from DRV.DRV_BK_PREC import DRV_BK_Meter_c
from PWR_CALIB.WS_CONFIG import WS_PATH, DATA_PATH, INFO_FILE_PATH
#######################          PROJECT IMPORTS         #######################


#######################              ENUMS               #######################
class _PORTS_e(Enum):
    SOURCE_PORT = '1'
    MULTIMETER_PORT = '2'

class _OPTIONS_e(Enum):
    CONF_DEV                = '1'
    FLASH_ORIG_PROGR        = '2'
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
    BACK                    = '37'


class _DEFAULTS():
    FILE_PATH_CONFIG_PORTS = '../config.yaml'
    EPC = { 'device_version':  {'hw': None, 'sw': None, 'can_ID': None, 's_n': None},
            'calib_data':      {'VOLT_HS': {'factor': None, 'offset': None, 'date': None},
                                'VOLT_LS': {'factor': None, 'offset': None, 'date': None},
                                'CURR':    {'factor': None, 'offset': None, 'date': None}}}

#######################              CLASSES             #######################
def _signal_handler(sig, frame):
    log.critical(f'You pressed Ctrl+C! If you want to exit the program, use the 5th option...')


def _configPorts() -> dict:
    '''AI is creating summary for _configPorts
    Args:
        - None
    Returns:
        - result (dict): Dictionary with the ports of the devices
    Raises:
        - None
    '''
    # Verificar si el archivo ya existe
    if not os.path.exists(_DEFAULTS.FILE_PATH_CONFIG_PORTS):
        print(f" File {_DEFAULTS.FILE_PATH_CONFIG_PORTS} does not exist.")
    else:
        try:
            with open(_DEFAULTS.FILE_PATH_CONFIG_PORTS, 'r') as file:
                ports = yaml.load(file, Loader=yaml.FullLoader)
        except:
            print(f"Error reading file {_DEFAULTS.FILE_PATH_CONFIG_PORTS}.")
    try:
        source: DRV_EA_PS_c   = DRV_EA_PS_c(model = 'EA-PS 2384-05 B' , serial_port = ports['source_port'])
        multimeter: DRV_BK_Meter_c = DRV_BK_Meter_c(serial_port = ports['multimeter_port'])
    except:
        log.error(f"Error opening ports.")
        source = None
        multimeter = None
    result = {_PORTS_e.SOURCE_PORT: source, _PORTS_e.MULTIMETER_PORT: multimeter}
    return result


def _automaticProgam() -> bool:
    while True:
        try:
            automatic = input(f"Do you want to run the automatic program? (y/n): ")
            if automatic == 'y' or automatic == 'Y':
                automatic = True
                log.info(f"Automatic program selected.")
            elif automatic == 'n' or automatic == 'N':
                automatic = False
            else:
                raise Exception
            break
        except:
            log.error(f"Invalid option.")
    return automatic


def _option() -> Enum:
    #clear_terminal()
    print(f"Select an option:\n\
    1. Configure device.\n\
    2. Flash original program.\n\
    3. Calibrate device.\n\
    4. Flash with calibration data.\n\
    5. Exit.")
    try:
        result = _OPTIONS_e(input(f"Chosen option: "))
        clear_terminal()
        if result is _OPTIONS_e.CALIB_DEV:
            print(f"Select an option of calibration:\n\
    1. Voltage high side.\n\
    2. Voltage low side.\n\
    3. Current low side.\n\
    4. Anode temperature.\n\
    5. Ambient temperature.\n\
    6. Body temperature.\n\
    7. Back.")
            try:
                op_cal = input(f"Chosen option: ")
                result = _OPTIONS_CALIB_e(_OPTIONS_e.CALIB_DEV.value + op_cal)
                #clear_terminal()
            except:
                log.error(f"Invalid option of calibration.")
    except:
        log.error(f"Invalid option.")
        result = None
    #clear_terminal()
    return result


def setupCalibStation(epc: EPC_CONF_c) -> None:
    ''' Sets up the calibration serial_number.
    Args:
        - epc (EPC_CONF_c): EPC_CONF_c object.
    Returns:
        - None
    Raises:
        - None
    '''
    global DATA_PATH, INFO_FILE_PATH, V_LS_CALIB_FILE_PATH, V_HS_CALIB_FILE_PATH, I_CALIB_FILE_PATH

    DATA_PATH = f"{WS_PATH}/raw_data/epc_{epc.sn}"
    INFO_FILE_PATH = f"{DATA_PATH}/epc_calib_info_{epc.sn}.yaml"
    V_LS_CALIB_FILE_PATH = f"{DATA_PATH}/epc_calib_VOLT_LS_{epc.sn}.csv"
    V_HS_CALIB_FILE_PATH = f"{DATA_PATH}/epc_calib_VOLT_HS_{epc.sn}.csv"
    I_CALIB_FILE_PATH = f"{DATA_PATH}/epc_calib_CURR_{epc.sn}.csv"

    if not os.path.exists(DATA_PATH):
        Path(DATA_PATH).mkdir(parents=True, exist_ok=True)
    
    if os.path.exists(INFO_FILE_PATH):
        with open(INFO_FILE_PATH, 'r') as file:
            conf_dev = yaml.load(file, Loader=yaml.FullLoader)
    else:
        conf_dev: dict = _DEFAULTS.EPC
    
    conf_dev['device_version']['s_n'] = epc.sn
    conf_dev['device_version']['hw'] = epc.hw_ver
    conf_dev['device_version']['sw'] = epc.sw_ver
    conf_dev['device_version']['can_ID'] = epc.can_id

    with open(INFO_FILE_PATH, 'w') as file:
        yaml.dump(conf_dev, file)
    log.info(f"setup done")



def man():
    ports: dict = _configPorts()
    if ports[_PORTS_e.SOURCE_PORT] is None or ports[_PORTS_e.MULTIMETER_PORT] is None:
        option = _OPTIONS_e.EXIT
    else:
        epc = EPC_CONF_c()
        option = _OPTIONS_e.CONF_DEV

    #automatic = _automaticProgam()
    automatic = False
    option_automatic = [_OPTIONS_e.CONF_DEV, _OPTIONS_e.FLASH_ORIG_PROGR, _OPTIONS_CALIB_e.VOLT_HS, _OPTIONS_CALIB_e.VOLT_LS, _OPTIONS_CALIB_e.CURR, _OPTIONS_e.FLASH_WITH_CALIB_DATA, _OPTIONS_e.EXIT]
    
    while option is not _OPTIONS_e.EXIT:
        try:
            if option == _OPTIONS_e.CONF_DEV:
                setupCalibStation(epc)
                calib = PWR_CALIB_c(source_port = ports[_PORTS_e.SOURCE_PORT], multimeter_port = ports[_PORTS_e.MULTIMETER_PORT])
            elif option == _OPTIONS_e.FLASH_ORIG_PROGR:
                pass
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
            elif option == _OPTIONS_CALIB_e.BACK:
                pass
        except Exception as e:
            log.error(f"Error in program: {e}.")

        if automatic:
            option = option_automatic[option_automatic.index(option) + 1]
        else:
            option = _option()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, _signal_handler)
    clear_terminal()
    #print_intro()
    man()
    log.info("End of program.")