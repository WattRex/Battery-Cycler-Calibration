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
import yaml

#######################       THIRD PARTY IMPORTS        #######################


#######################          MODULE IMPORTS          #######################
from STM_FLASH import STM_FLASH_Epc_Conf_c, STM_FLASH_c
from POWER import *
from CONFIG import *
from TERM import TERM_c, TERM_Option_e

#######################          PROJECT IMPORTS         #######################


#######################          CONSTANTS               #######################

#######################              CLASSES             #######################

class MANAGER_c():
    '''Class to manage the state machine'''
    def __init__(self) -> None:
        self.__epc_config: STM_FLASH_Epc_Conf_c = None
        self.__status: TERM_Option_e = TERM_Option_e.CONF_DEV
        self.__power = PWR_c()
        self.__stm: STM_FLASH_c = STM_FLASH_c()


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
            self.__power.calibVoltHS()
        elif mode is PWR_Mode_e.VOLT_LS:
            log.info(f"Calibrating voltage low side")
            self.__power.calibVoltLS()
        elif mode is PWR_Mode_e.CURR:
            log.info(f"Calibrating current")
            self.__power.calibCurr()
        elif mode is PWR_Mode_e.TEMP_ANOD:
            log.info(f"Calibrating temperature anode")
            pass
        elif mode is PWR_Mode_e.TEMP_AMB:
            log.info(f"Calibrating temperature ambient")
            pass
        elif mode is PWR_Mode_e.TEMP_BODY:
            log.info(f"Calibrating temperature body")
            pass


    def __confDevice(self) -> CONFIG_Result_e:
        '''Configure the device
        Args:
            - None
        Returns:
            - result (CONFIG_Result_e): Result of the configuration in the device
        Raises:
            - None
        '''
        global CONFIG_DEFAULT_INFO_EPC
        log.info(f"Configuring device")
        self.__epc_config = TERM_c.queryEPCConf()
        CONFIG_WS_c.updatePath(sn = self.__epc_config.sn)
        result: CONFIG_Result_e = CONFIG_Result_e.Error

        info_file_path = CONFIG_WS_c.getInfoFilePath()
        if os.path.exists(info_file_path):
            with open(info_file_path, 'r') as file:
                info_epc = yaml.load(file, Loader = yaml.FullLoader)
        else:
            info_epc = CONFIG_DEFAULT_INFO_EPC

        info_epc['device_version']['sw'] = self.__epc_config.sw_ver
        info_epc['device_version']['hw'] = self.__epc_config.hw_ver
        info_epc['device_version']['can_ID'] = self.__epc_config.can_id
        info_epc['device_version']['s_n'] = self.__epc_config.sn

        if os.path.exists(info_file_path):
            with open(info_file_path, 'w') as file:
                log.info(f"Info file yaml with serial number: {self.__epc_config.sn} updated")            
                yaml.dump(info_epc, file)
            result = CONFIG_Result_e.NoError

        if result is CONFIG_Result_e.Error:
            log.error(f"Error updating info file yaml with serial number: {self.__epc_config.sn}")
            TERM_c.showError(status = TERM_Option_e.CONF_DEV, message = f"Error updating info file yaml with serial number: {self.__epc_config.sn}")
        else:
            result = self.__stm.configureDev(epc_config = self.__epc_config)
            if result is CONFIG_Result_e.Error:
                log.error(f"Error configuring device")
                TERM_c.showError(status = TERM_Option_e.CONF_DEV, message = "Error configuring device")
        return result


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
        # check_calib = {PWR_Mode_e.VOLT_HS: True, PWR_Mode_e.VOLT_LS: True, PWR_Mode_e.CURR: True,
        #                PWR_Mode_e.TEMP_ANOD: True, PWR_Mode_e.TEMP_AMB: True, PWR_Mode_e.TEMP_BODY: True} #TODO: Remove this line
        
        guided = False

        while self.__status is not TERM_Option_e.EXIT:
            #Guided mode option
            if guided is True:
                option_guided = [None, TERM_Option_e.FLASH_ORIG, TERM_Option_e.CONF_DEV, TERM_Option_e.CALIB, TERM_Option_e.FLASH_CALIB, TERM_Option_e.EXIT]
                self.__status = option_guided[option_guided.index(self.__status) + 1]
            else:
                self.__status = TERM_c.queryOptions()

            #Flash original program
            if self.__status is TERM_Option_e.FLASH_ORIG:
                log.info(f"Flashing original program")
                result_flash = self.__stm.flashUC(binary_name = 'STM32_orig.bin')
                if result_flash is CONFIG_Result_e.Error:
                    log.error(f"Error flashing original program")
                    TERM_c.showError(status = TERM_Option_e.FLASH_ORIG, message = "Error flashing original program")


            #Configure device
            elif self.__status is TERM_Option_e.CONF_DEV:
                self.__confDevice()


            #Calibrate device
            elif self.__status is TERM_Option_e.CALIB:
                log.info(f"Calibrating device")
                #Check if device is configured
                if self.__epc_config is None:
                    log.error("EPC configuration not set")
                    return_conf_dev = self.__confDevice()

                if return_conf_dev is CONFIG_Result_e.NoError:
                    #Guided mode
                    if guided is True:
                        options_calib_mode = [PWR_Mode_e.VOLT_HS, PWR_Mode_e.VOLT_LS, PWR_Mode_e.CURR, PWR_Mode_e.TEMP_ANOD, PWR_Mode_e.TEMP_AMB, PWR_Mode_e.TEMP_BODY]
                        for calib_mode in options_calib_mode:
                            self._calibStatus(calib_mode)
                            check_calib[calib_mode] = True
                    #Manual mode
                    else:
                        calib_mode = TERM_c.queryCalibMode()
                        self._calibStatus(PWR_Mode_e(calib_mode))
                        check_calib[calib_mode] = True
                else:
                    TERM_c.showError(status = TERM_Option_e.CALIB, message = "Device could not be calibrated")


            #Flash with calibration data
            elif self.__status is TERM_Option_e.FLASH_CALIB:
                log.info(f"Flashing with calibration data")
                #Check if device is configured
                if self.__epc_config is None:   #TODO: This condition should check if EPC sent info is the same as the __epc_config
                    log.error("EPC configuration not set")
                    return_conf_dev = self.__confDevice()

                if return_conf_dev is CONFIG_Result_e.NoError:
                    #Check if all calibration data are set
                    if False in check_calib.values():
                        log.error("Not all calibration data are set")
                        TERM_c.showError(status = TERM_Option_e.FLASH_CALIB, message = "Not all calibration data are set")
                        for calib in check_calib:
                            if check_calib[calib] is False:
                                self._calibStatus(mode = calib)
                    else:
                        #Apply calibration data
                        result_calib: CONFIG_Result_e = self.__stm.applyCalib()
                        if result_calib is CONFIG_Result_e.Error:
                            log.error(f"Error applying calibration data")
                            TERM_c.showError(status = TERM_Option_e.FLASH_CALIB, message = "Error applying calibration data")
                        else:
                            #Build project
                            result_build: CONFIG_Result_e = self.__stm.buildProject()
                            if result_build is CONFIG_Result_e.Error:
                                log.error(f"Error building project")
                                TERM_c.showError(status = TERM_Option_e.FLASH_CALIB, message = "Error building project")
                            else:
                                #Flash with calibration data
                                result_flash: CONFIG_Result_e = self.__stm.flashUC(binary_name='STM32.bin')
                                if result_flash is CONFIG_Result_e.Error:
                                    log.error(f"Error flashing with calibration data")
                                    TERM_c.showError(status = TERM_Option_e.FLASH_CALIB, message = "Error flashing with calibration data")
                else:
                    log.error(f"Device could not be calibrated")
                    TERM_c.showError(status = TERM_Option_e.FLASH_CALIB, message = "Device could not be calibrated")


            #Guided mode
            elif self.__status is TERM_Option_e.GUIDED_MODE:
                log.info(f"Guided mode activated")
                guided = True
                self.__status = None






if __name__ == '__main__':
    print(CONFIG_WS_c.getInfoFilePath())
    # TERM_c.showIntro()
    man = MANAGER_c()
    man.executeMachineStatus()