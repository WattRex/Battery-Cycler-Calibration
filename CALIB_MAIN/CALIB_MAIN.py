#!/usr/bin/python3

#######################        MANDATORY IMPORTS         #######################
from pathlib import Path
import sys, os
import yaml
sys.path.append(os.getcwd())  #get absolute path

#######################      LOGGING CONFIGURATION       #######################
from SYS.SYS_LOG import SYS_LOG_Logger_c, SYS_LOG_LoggerGetModuleLogger
if __name__ == '__main__':
    cycler_logger = SYS_LOG_Logger_c('./SYS/SYS_LOG/logginConfig.conf')
log = SYS_LOG_LoggerGetModuleLogger(__name__, config_by_module_filename="./log_config.yaml")


#######################         GENERIC IMPORTS          #######################
import time
import signal
#######################       THIRD PARTY IMPORTS        #######################


#######################          MODULE IMPORTS          #######################
from PWR_CALIB import *
from STM_FLASH import *
#######################          PROJECT IMPORTS         #######################


#######################              ENUMS               #######################

class _DEFAULTS():
    FILE_PATH_CONFIG = './CALIB_MAIN/config.yaml'

default_settings = {'device_version':  {'hw': None, 'sw': None, 'can_ID': None, 's_n': None},
                    'calib_data':      {'volt_hs': {'factor': None, 'offset': None, 'date': None},
                                        'volt_ls': {'factor': None, 'offset': None, 'date': None},
                                        'curr':    {'factor': None, 'offset': None, 'date': None}}}

#######################              CLASSES             #######################
def _signal_handler(sig, frame):
    log.critical('You pressed Ctrl+C! If you want to exit the program, use the 5th option...')

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


def _option() -> int:
    print(f"Select an option:\n\
    1. Flash original program.\n\
    2. Configure device.\n\
    3. Calibrate device.\n\
    4. Flash with calibration data.\n\
    5. Exit.")
    option = None
    try:
        option = int(input("Chosen option: "))
        if option < 1 or option > 5:
            print(f"Invalid option.")
    except:
        print(f"Invalid option.")
    if option == 3:
        print(f"Select an option:\n\
        1. Voltage high side.\n\
        2. Voltage low side.\n\
        3. Current low side.\n\
        4. Anodo temperature.\n\
        5. Ambient temperature.\n\
        6. Body temperature.")
        try:
            option_calib = int(input("Chosen option: "))
            if option_calib < 1 or option_calib > 6:
                print(f"Invalid option.")
            else:
                option = int(str(option) + str(option_calib))
        except:
            print(f"Invalid option.")
    return option


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
    log.info(f"VIVA")
    log.info(f"VIVA")
    log.info(f"VIVA")
    log.info(f"VIVA")
    log.warning(f"UCRANIA")
    log.warning(f"UCRANIA")
    log.warning(f"UCRANIA")
    log.warning(f"UCRANIA")
    ports: dict = _readConfigPorts()
    
    option = 2
    while option != 5:
        try:
            if option == 1:
                calib.SetupCalibStation()
            elif option == 2:
                epc_sn = _configDevice()
                calib: PWR_CALIB_c = PWR_CALIB_c(source_port = ports['source_port'], multimeter_port = ports['multimeter_port'], epc_sn = epc_sn)
            elif option == 4:
                pass
            elif option == 31:
                calib.CalibVoltHS()
            elif option == 32:
                calib.CalibVoltLS()
            elif option == 33:
                calib.CalibCurr()
            elif option == 34:
                pass
            elif option == 35:
                pass
            elif option == 36:
                pass

        except Exception as e:
            print(f"Error in program: {e}.")
        option = _option()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, _signal_handler)
    main()
    print("End of program.")