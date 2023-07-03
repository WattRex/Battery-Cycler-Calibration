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


#######################       THIRD PARTY IMPORTS        #######################

#######################          MODULE IMPORTS          #######################
from TERM import TERM_c, TERM_Option_e
from STM_FLASH import STM_FLASH_Epc_Conf_c
from POWER import *
#######################          PROJECT IMPORTS         #######################


#######################              ENUMS               #######################



#######################              CLASSES             #######################

class MANAGER_c():
    '''Class to manage the state machine'''
    def __init__(self) -> None:
        self.__epc_config: STM_FLASH_Epc_Conf_c = None
        self.__status: TERM_Option_e = TERM_Option_e.CONF_DEV
        self.__power = PWR_c(config_path_file = f"") #TODO: check path
    
    
    def _calibStatus(self, mode: PWR_Mode_e) -> None:
        '''Calibrate the EPC in the specified mode

        Args:
            - mode (PWR_Mode_e): Mode to calibrate
        Returns:    
            - None
        Raises:
            - None
        '''
        if mode is PWR_Mode_e.VOLT_HS:
            log.info(f"Calibrating voltage high side")
            self.__power.calibVoltHS
        elif mode is PWR_Mode_e.VOLT_LS:
            log.info(f"Calibrating voltage low side")
            self.__power.calibVoltLS
        elif mode is PWR_Mode_e.CURR:
            log.info(f"Calibrating current")
            self.__power.calibCurr
        elif mode is PWR_Mode_e.TEMP_ANOD:
            log.info(f"Calibrating temperature anode")
            pass
        elif mode is PWR_Mode_e.TEMP_AMB:
            log.info(f"Calibrating temperature ambient")
            pass
        elif mode is PWR_Mode_e.TEMP_BODY:
            log.info(f"Calibrating temperature body")
            pass


    def executeMachineStatus(self) -> None:
        '''Execute the state machine
        Args:
            - None
        Returns:
            - None
        Raises:
            - None
        '''
        check_calib = {PWR_Mode_e.VOLT_HS: False, PWR_Mode_e.VOLT_LS: False, PWR_Mode_e.CURR: False,
                       PWR_Mode_e.TEMP_ANOD: False, PWR_Mode_e.TEMP_AMB: False, PWR_Mode_e.TEMP_BODY: False}
        guided = False
        term = TERM_c()

        while self.__status is not TERM_Option_e.EXIT:
            #Guided mode option
            if guided is True:
                option_guided = [None, TERM_Option_e.FLASH_ORIG, TERM_Option_e.CONF_DEV, TERM_Option_e.CALIB, TERM_Option_e.FLASH_CALIB, TERM_Option_e.EXIT]
                self.__status = option_guided[option_guided.index(self.__status) + 1]
            else:
                self.__status = term.queryOptions()

            #Flash original program
            if self.__status is TERM_Option_e.FLASH_ORIG:
                log.info(f"Flashing original program")
                pass

            #Configure device
            elif self.__status is TERM_Option_e.CONF_DEV:
                log.info(f"Configuring device")
                self.__epc_config = term.queryEPCConf()

            #Calibrate device
            elif self.__status is TERM_Option_e.CALIB:
                log.info(f"Calibrating device")
                if self.__epc_config is None:
                    log.error("EPC configuration not set")
                else:
                    if guided is True:
                        options_calib_mode = [PWR_Mode_e.VOLT_HS, PWR_Mode_e.VOLT_LS, PWR_Mode_e.CURR, PWR_Mode_e.TEMP_ANOD, PWR_Mode_e.TEMP_AMB, PWR_Mode_e.TEMP_BODY]
                        for calib_mode in options_calib_mode:
                            self._calibStatus(calib_mode)
                            check_calib[calib_mode] = True
                    else:
                        calib_mode = self.__status = term.queryCalibMode()
                        self._calibStatus(calib_mode)
                        check_calib[calib_mode] = True

            #Flash with calibration data
            elif self.__status is TERM_Option_e.FLASH_CALIB:
                log.info(f"Flashing with calibration data")
                if self.__epc_config is None:
                    log.error("EPC configuration not set")
                else:
                    if False in check_calib.values():
                        log.error("Not all calibration data are set")
                    else:
                        pass

            #Guided mode
            elif self.__status is TERM_Option_e.GUIDED_MODE:
                log.info(f"Guided mode activated")
                guided = True
                self.__status = None





if __name__ == '__main__':
    man = MANAGER_c()
    man.executeMachineStatus()