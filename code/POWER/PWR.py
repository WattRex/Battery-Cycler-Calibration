# #!/usr/bin/python3

# #######################        MANDATORY IMPORTS         #######################
import sys, os
sys.path.append(os.getcwd())  #get absolute path

# #######################      LOGGING CONFIGURATION       #######################
from SYS.SYS_LOG import SYS_LOG_Logger_c, SYS_LOG_LoggerGetModuleLogger
if __name__ == '__main__':
    root_logger = SYS_LOG_Logger_c('./SYS/SYS_LOG/logginConfig.conf')
log = SYS_LOG_LoggerGetModuleLogger(__name__, config_by_module_filename="./CONFIG/log_config.yaml")

# #######################         GENERIC IMPORTS          #######################
from enum import Enum

# #######################       THIRD PARTY IMPORTS        #######################


# #######################          MODULE IMPORTS          #######################

# #######################          PROJECT IMPORTS         #######################


# #######################              ENUMS               #######################
class PWR_Mode_e(Enum):
    VOLT_HS     = 0
    VOLT_LS     = 1
    CURR        = 2
    TEMP_ANOD   = 3
    TEMP_AMB    = 4
    TEMP_BODY   = 5
    NONE        = 6


class _PWR_Params_e(Enum):
    VOLT_HS_MIN = 10000 #mV #TODO: check values
    VOLT_HS_MAX = 15000 #mV #TODO: check values
    VOLT_HS_STEP = 1000 #TODO: check values
    VOLT_LS_MIN = 30000 #mV #TODO: check values
    VOLT_LS_MAX = 35000 #mV #TODO: check values
    VOLT_LS_STEP = 1000 #TODO: check values
    CURR_MIN = 300      #mA #TODO: check values
    CURR_MAX = 350      #mA #TODO: check values
    CURR_STEP = 10      #TODO: check values

# #######################              CLASSES             #######################
class PWR_c():
    def __init__(self, config_path_file: str) -> None:
        self._source = None
        self._meter = None
        self._epc = None
        self._config_devices(config_path_file)
    

    def _config_devices(self) -> None:
        pass


    def _writeData(self) -> None:
        pass


    def _checkExistCalib(mode:PWR_Mode_e) -> bool:
        pass


    def calibVoltHS(self) -> None:
        pass