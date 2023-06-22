#!/usr/bin/python3

#######################        MANDATORY IMPORTS         #######################
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
from PWR_CALIB import PWR_CALIB_c

#######################          PROJECT IMPORTS         #######################


#######################              ENUMS               #######################

class _DEFAULTS():
    FILE_PATH_CONFIG = 'config.yaml'


#######################              CLASSES             #######################
def _signal_handler(sig, frame):
    log.critical('You pressed Ctrl+C! If you want to exit the program, use the 5th option...')

def _readConfig() -> dict:
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

def main():
    ports: dict = _readConfig()
    no_epc_number = True
    option = None

    while option != 5:
        option = _option()
        if option == 1 or no_epc_number == True:
            epc = str(input(f"serial number of EPC:")) #TODO: validar numero de serie
            no_epc_number = False
        try:
            calib: PWR_CALIB_c = PWR_CALIB_c(source_port = ports['source_port'], multimeter_port = ports['multimeter_port'], epc_number = epc)
        
            if option == 1:
                calib.SetupCalibStation(epc)
            elif option == 2:
                pass
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
            print(f"Error in program.")
            print(e)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, _signal_handler)
    main()
    print("End of program.")