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

# #######################       THIRD PARTY IMPORTS        #######################

# #######################          MODULE IMPORTS          #######################
from TERM import TERM_Option_e
from STM_FLASH import STM_FLASH_Epc_Conf_c

# #######################          PROJECT IMPORTS         #######################


# #######################              ENUMS               #######################

# #######################              CLASSES             #######################

class MANAGER_c():
    def __init__(self) -> None:
        self._epc_config: STM_FLASH_Epc_Conf_c = None
        self._status: TERM_Option_e = None

    def _calibStatus(self):
        pass


    def executeMachineStatus(self):
        pass