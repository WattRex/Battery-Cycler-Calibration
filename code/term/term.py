#!/usr/bin/python3
'''
Driver of commands for terminal.
'''
#######################        MANDATORY IMPORTS         #######################
import sys
import os

#######################         GENERIC IMPORTS          #######################
from time import sleep
from enum import Enum
from consolemenu import SelectionMenu, Screen

#######################       THIRD PARTY IMPORTS        #######################

#######################      SYSTEM ABSTRACTION IMPORTS  #######################
sys.path.append(os.getcwd())

#######################          PROJECT IMPORTS         #######################

#######################          MODULE IMPORTS          #######################
from stm_flash import StmFlash_EpcConfC # pylint: disable=wrong-import-position

#######################              ENUMS               #######################
_LOGO_INTRO = r"""

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

class TermOptionE(Enum):
    "Enum for the principal options"
    FLASH_ORIG  = 0
    CONF_DEV    = 1
    CALIB       = 2
    FLASH_CALIB = 3
    GUIDED_MODE = 4
    EXIT        = 5

#######################             CLASSES              #######################


class TermC:
    "Class to manage the terminal interface"

    @staticmethod
    def show_intro() -> None:
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
    def show_progress_bar(iteration, total) -> None:
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
        filled_length = int(length * iteration // total)
        show_bar = fill * filled_length + '-' * (length - filled_length)
        print(f'\r{prefix} |{show_bar}| {percent}% {suffix}', end = "\r")
        # Print New Line on Complete
        if iteration == total:
            print()


    @staticmethod
    def query_rewrite_calib() -> bool:
        ''' Shows the rewrite options of the program and returns the chosen one.
        Args:
            - None
        Returns:
            - result (bool): chosen option
        Raises:
            - None
        '''
        a_list = ["No", "Yes"]
        menu = SelectionMenu(a_list,"Do you want to rewrite the calibration data?")
        menu.show()
        menu.join()
        return bool(menu.selected_option)


    @staticmethod
    def query_options() -> TermOptionE:
        ''' Shows the principal options of the program and returns the chosen one.
        Args:
            - None
        Returns:
            - result (TermOptionE): chosen option
        Raises:
            - None
        '''
        sleep(10)
        a_list = ["Flash original program", "Configure device", \
                  "Calibrate device", "Flash with calibration data", "Guided mode"]
        menu = SelectionMenu(a_list,"Select an option:")
        menu.show()
        menu.join()
        return TermOptionE(menu.selected_option)


    @staticmethod
    def query_epc_conf() -> StmFlash_EpcConfC:
        ''' Displays the EPC configuration options and returns the EPC configuration
        Args:
            - None
        Returns:
            - result (StmFlash_EpcConfC): chosen option
        Raises:
            - None
        '''
        while True:
            try:
                serial_number = int(input("- Serial number of EPC: "))
                sw_ver = int(input("- Software version: "))
                can_id = int(input("- CAN ID: "))
                hw_ver = TermC.hardware_version()
                break
            except ValueError:
                print("Invalid data.")
        result = StmFlash_EpcConfC(software = sw_ver, hardware = hw_ver, can_id = can_id, \
                                      serial_number = serial_number)
        return result


    @staticmethod
    def hardware_version() -> int:
        ''' Shows the hardware options of the program and returns the chosen one.
        Args:
            - None
        Returns:
            - result (int): chosen option
        Raises:
            - None
        '''
        query = {  "fan"        : (["No", "Yes"],
                                   "¿Does the EPC have a fan?\nSelect an option:"),
                    "connector" : (["18650", "Banana"],
                                   "What type of connector does the EPC have?\nSelect an option:"),
                    "temp_anode": (["No anode", "Ring NTC", "Plastic NTC"],
                                   "What type of temperature sensor in anode does the EPC have?\n\
                                    Select an option:"),
                    "temp_body" : (["No STS", "STS Sens"],
                                   "What type of temperature sensor in body does the EPC have?\n\
                                    Select an option:"),
                    "temp_amb"  : (["No sensor", "Plastic NTC"],
                                   "What type of temperature sensor in ambient does the EPC have?\n\
                                    Select an option:")
        }
        hw_version = 0
        fan         = TermC.query_hardware(options = query["fan"][0], \
                                            message = query["fan"][1])
        connector   = TermC.query_hardware(options = query["connector"][0], \
                                            message = query["connector"][1])
        temp_anode  = TermC.query_hardware(options = query["temp_anode"][0], \
                                            message = query["temp_anode"][1])
        temp_body   = TermC.query_hardware(options = query["temp_body"][0], \
                                            message = query["temp_body"][1])
        temp_amb    = TermC.query_hardware(options = query["temp_amb"][0], \
                                            message = query["temp_amb"][1])

        temp_amb = format(temp_amb, '01b')
        temp_body = format(temp_body, '01b')
        temp_anode = format(temp_anode, '02b')
        connector = format(connector, '03b')
        fan = format(fan, '01b')
        hw_version = format(hw_version, '03b')

        number = temp_amb + temp_body + temp_anode + connector + fan + hw_version
        return int(number, 2)

    @staticmethod
    def query_hardware(options: list, message: str) -> int:
        '''Show the query of the hardware.
        Args:
            - options (list): Options to choose
            - message (str): Message to show
        Returns:
            - (int): chosen option
        Raises:
            - None
        '''
        menu = SelectionMenu(options, message, show_exit_option = False)
        menu.show()
        menu.join()
        return menu.selected_option


    @staticmethod
    def query_calib_mode() -> int:
        ''' Shows the calibration options of the program and returns the chosen one.
        Args:
            - None
        Returns:
            - result (int): chosen option
        Raises:
            - None
        '''
        a_list = ["Voltage high side", "Voltage low side", "Current"]
        menu = SelectionMenu(a_list,"Select an option of calibration:")
        menu.show()
        menu.join()
        return menu.selected_option

    @staticmethod
    def show_error(status: TermOptionE, message: str) -> None:
        ''' Shows an error message.
        Args:
            - status (TermOptionE): current status
            - message (str): error message
        Returns:
            - None
        Raises:
            - None
        '''
        print(f"Error raise on status: {status}. Message: {message}")
        sleep(3)
