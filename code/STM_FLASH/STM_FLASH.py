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


# #######################          PROJECT IMPORTS         #######################


# #######################              ENUMS               #######################

# #######################              CLASSES             #######################

class STM_FLASH_Epc_Conf_c():
    def __init__(self, software: int, hardware: int, can_id: int, serial_number: int) -> None:
        self.sw_ver: int = software
        self.hw_ver: int = hardware
        self.can_id: int = can_id
        self.sn: int = serial_number


class STM_FLASH_c():
    def __init__(self, epc_conf) -> None:
        self._epc_conf: STM_FLASH_Epc_Conf_c = epc_conf


    def configureDev(self, epc_config: STM_FLASH_Epc_Conf_c):
        pass
    def applyCalib(self) -> None:
        pass
    def buildProject(self) -> None:
        pass
    def flashUC(self) -> None:
        pass
