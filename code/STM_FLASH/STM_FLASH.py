import yaml
from PWR_CALIB.WS_CONFIG import *
from SYS.SYS_LOG import SYS_LOG_Logger_c, SYS_LOG_LoggerGetModuleLogger
if __name__ == '__main__':
    cycler_logger = SYS_LOG_Logger_c('./SYS/SYS_LOG/logginConfig.conf')
log = SYS_LOG_LoggerGetModuleLogger(__name__, config_by_module_filename="./log_config.yaml")



class EPC_CONF_c():
    def __init__(self) -> None:
        self.sw_ver: int = None
        self.hw_ver: int = None
        self.can_id: int = None
        self.sn: int = None
        self._updateInfo()

    def _updateInfo(self):
        while True:
            try:
                self.sn     = int(input(f"- Serial number of EPC: ")) #TODO: validar numero de serie
                self.sw_ver = int(input(f"- Hardware version: "))
                self.hw_ver = int(input(f"- Software version: "))
                self.can_id = int(input(f"- CAN ID: "))
                break
            except:
                log.error(f"Invalid data.")


class STM_FLASH_c():
    def __init__(self) -> None:
        pass
    def ConfigureProject(epc_config: EPC_CONF_c):
        pass
    def BuildProject():
        pass
    def Flash_uC():
        pass
    def _applyCalib():
        pass



# Lo que hay que tocar:
# firmware/sources/EPC_CONF

# Para compilar:
# firmeware/build  y ejecutar: make all
