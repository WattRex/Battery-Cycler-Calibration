#!/usr/bin/python3

#######################        MANDATORY IMPORTS         #######################
import sys, os
sys.path.append(os.getcwd())  #get absolute path

#######################      LOGGING CONFIGURATION       #######################

#######################         GENERIC IMPORTS          #######################
from enum import Enum
import yaml
from pathlib import Path

#######################       THIRD PARTY IMPORTS        #######################

#######################          MODULE IMPORTS          #######################

#######################          PROJECT IMPORTS         #######################

#######################              ENUMS               #######################
_WS_PATH= f"/home/pi004/GIT_luroche/Battery-Cycler-Calibration"
_CONF_PORTS_FILE_PATH = f"{_WS_PATH}/code/CONFIG/config_ports.yaml"
_DATA_PATH = f"{_WS_PATH}"
_INFO_FILE_PATH = f"{_WS_PATH}"
_V_LS_CALIB_FILE_PATH = f"{_WS_PATH}"
_V_HS_CALIB_FILE_PATH = f"{_WS_PATH}"
_I_CALIB_FILE_PATH = f"{_WS_PATH}"

CONFIG_DEFAULT_INFO_EPC = { 'device_version':  {'hw': None, 'sw': None, 'can_ID': None, 's_n': None},
                            'calib_data':      {'VOLT_HS': {'factor': None, 'offset': None, 'date': None},
                                                'VOLT_LS': {'factor': None, 'offset': None, 'date': None},
                                                'CURR':    {'factor': None, 'offset': None, 'date': None}}}

class CONFIG_Result_e(Enum):
    Error = 0
    NoError = 1


#######################              CLASSES             #######################
class CONFIG_WS_c:
    '''Configure the files path for the workspace
    '''
    @staticmethod
    def updatePath(sn: int) -> None:
        '''Update the path for the workspace
        Args:
            - sn (int): serial number of the EPC
        Returns:
            - None
        Raises:
            - None
        '''
        global _DATA_PATH, _INFO_FILE_PATH, _V_LS_CALIB_FILE_PATH, _V_HS_CALIB_FILE_PATH, _I_CALIB_FILE_PATH
        _DATA_PATH = f"{_WS_PATH}/data/epc_{sn}"
        _INFO_FILE_PATH = f"{_DATA_PATH}/epc_{sn}_info.yaml"
        _V_LS_CALIB_FILE_PATH = f"{_DATA_PATH}/epc_{sn}_ls_volt.csv"
        _V_HS_CALIB_FILE_PATH = f"{_DATA_PATH}/epc_{sn}_hs_volt.csv"
        _I_CALIB_FILE_PATH = f"{_DATA_PATH}/epc_{sn}_curr.csv"
        
        if not os.path.exists(_DATA_PATH):
            Path(_DATA_PATH).mkdir(parents=True, exist_ok=True)

        if not os.path.exists(_INFO_FILE_PATH):
            with open(_INFO_FILE_PATH, 'w') as file:
                info_epc = CONFIG_DEFAULT_INFO_EPC
                info_epc['device_version']['s_n'] = sn
                yaml.dump(info_epc, file)

    @staticmethod
    def getFileConfPorts() -> str:
        '''Get the path of the file containing the ports configuration
        Args:
            - None
        Returns:
            - (str): path of the file containing the ports configuration
        Raises:
            - None
        '''
        return _CONF_PORTS_FILE_PATH

    @staticmethod
    def getInfoFilePath() -> str:
        '''Get the path of the file containing the information
        Args:
            - None
        Returns:
            - (str): Path of the file containing the information
        Raises:
            - None
        '''
        return _INFO_FILE_PATH

    @staticmethod
    def getVoltLowSidePath() -> str:
        '''Returns the path to the low side voltage.
        Args:
            - None
        Returns:
            - (str): Path to the low side voltage
        Raises:
            - None
        '''
        return _V_LS_CALIB_FILE_PATH

    @staticmethod
    def getVoltHighSidePath() -> str:
        '''Returns the path to the high side voltage.
        Args:
            - None
        Returns:
            - (str): Path to the high side voltage
        Raises:
            - None
        '''
        return _V_HS_CALIB_FILE_PATH

    @staticmethod
    def getCalibCurrentPath() -> str:
        '''Returns the path to the current file.
        Args:
            - None
        Returns:
            - (str): Path to the current
        Raises:
            - None
        '''
        return _I_CALIB_FILE_PATH