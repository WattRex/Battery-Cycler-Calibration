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
from time import sleep
from enum import Enum
from consolemenu import SelectionMenu, Screen

#######################       THIRD PARTY IMPORTS        #######################


#######################          MODULE IMPORTS          #######################
from STM_FLASH.STM_FLASH import STM_FLASH_Epc_Conf_c


#######################          PROJECT IMPORTS         #######################


#######################              CONSTANTS           #######################
_LOGO_INTRO = """

      ____        _   _                      _____           _               _____      _ _ _               _   _             
     |  _ \      | | | |                    / ____|         | |             / ____|    | (_) |             | | (_)            
     | |_) | __ _| |_| |_ ___ _ __ _   _   | |    _   _  ___| | ___ _ __   | |     __ _| |_| |__  _ __ __ _| |_ _  ___  _ __  
     |  _ < / _` | __| __/ _ \ '__| | | |  | |   | | | |/ __| |/ _ \ '__|  | |    / _` | | | '_ \| '__/ _` | __| |/ _ \| '_ \ 
     | |_) | (_| | |_| ||  __/ |  | |_| |  | |___| |_| | (__| |  __/ |     | |___| (_| | | | |_) | | | (_| | |_| | (_) | | | |
     |____/ \__,_|\__|\__\___|_|   \__, |   \_____\__, |\___|_|\___|_|      \_____\__,_|_|_|_.__/|_|  \__,_|\__|_|\___/|_| |_|
                                    __/ |          __/ |                                                                      
                                   |___/          |___/                                                                       

                                                      Version 1.0
                                             Calibration for Battery Cycler                               
        """


#######################              ENUMS               #######################
class TERM_Option_e(Enum):
    FLASH_ORIG  = 0
    CONF_DEV    = 1
    CALIB       = 2
    FLASH_CALIB = 3
    GUIDED_MODE = 4
    EXIT        = 5

#######################             CLASSES              #######################


class TERM_c():
    ''' Class to manage the terminal interface. '''

    @staticmethod
    def showIntro() -> None:
        ''' Shows the intro of the program.
        Args:
            - None
        Returns:
            - None
        Raises:
            - None
        '''
        Screen.clear()
        intro_text = "Battery  Cycler  Calibration"
        intro_ascii = _LOGO_INTRO
        lines = intro_ascii.split("\n")
        padding = " " * 50
        for i in range(len(lines)):
            Screen.clear()
            print(padding + "\n".join(lines[:i]))
            sleep(0.1)
        sleep(3)
        Screen.clear()
        print(padding + intro_text)


    @staticmethod
    def showProgressBar(iteration, total) -> None:
        ''' Loop to create terminal progress bar
        Args:
            - iteration (Int): current iteration
            - total (Int): total iterations
        Returns:
            - None
        Raises:
            - None
        '''
        fill = '█'
        decimals = 1
        prefix = 'Progress:'
        suffix = 'Complete'
        length = 50
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = "\r")
        # Print New Line on Complete
        if iteration == total: 
            print()


    @staticmethod
    def queryOptions() -> TERM_Option_e:
        ''' Shows the principal options of the program and returns the chosen one.
        Args:
            - None
        Returns:
            - result (TERM_Option_e): chosen option
        Raises:
            - None
        '''
        sleep(10)
        a_list = ["Flash original program", "Configure device", "Calibrate device", "Flash with calibration data", "Guided mode"]
        menu = SelectionMenu(a_list,"Select an option:")
        menu.show()
        menu.join()
        return TERM_Option_e(menu.selected_option)


    @staticmethod
    def queryEPCConf() -> STM_FLASH_Epc_Conf_c:
        ''' Displays the EPC configuration options and returns the EPC configuration
        Args:
            - None
        Returns:
            - result (STM_FLASH_Epc_Conf_c): chosen option
        Raises:
            - None
        '''
        
        while True:
            try:
                sn     = int(input(f"- Serial number of EPC: ")) #TODO: validar numero de serie
                hw_ver = int(input(f"- Hardware version: "))
                sw_ver = int(input(f"- Software version: "))
                can_id = int(input(f"- CAN ID: "))
                break
            except:
                log.error(f"Invalid data.")
        result = STM_FLASH_Epc_Conf_c(software = sw_ver, hardware = hw_ver, can_id = can_id, serial_number = sn)
        return result


    @staticmethod
    def queryCalibMode() -> int:
        ''' Shows the calibration options of the program and returns the chosen one.
        Args:
            - None
        Returns:
            - result (PWR_Mode_e): chosen option
        Raises:
            - None
        '''
        a_list = ["Voltage high side", "Voltage low side", "Current", "Anode temperature", "Ambient temperature", "Body temperature"]
        menu = SelectionMenu(a_list,"Select an option of calibration:")
        menu.show()
        menu.join()
        return menu.selected_option
    
    @staticmethod
    def showError(status: TERM_Option_e, message: str) -> None:
        ''' Shows an error message.
        Args:
            - status (TERM_Option_e): current status
            - message (str): error message
        Returns:
            - None
        Raises:
            - None
        '''
        print(f"Error raise on status: {status}. Message: {message}")
        sleep(3)