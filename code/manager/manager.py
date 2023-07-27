#!/usr/bin/python3
'''
Principal program.
'''
#######################        MANDATORY IMPORTS         #######################
import sys
import os

#######################         GENERIC IMPORTS          #######################
import yaml

#######################       THIRD PARTY IMPORTS        #######################

#######################      SYSTEM ABSTRACTION IMPORTS  #######################
sys.path.append(os.getcwd())
from sys_abs.sys_log import sys_log_logger_get_module_logger
if __name__ == '__main__':
    from sys_abs.sys_log import SysLogLoggerC
    cycler_logger = SysLogLoggerC('./sys_abs/sys_log/logginConfig.conf')
log = sys_log_logger_get_module_logger(__name__)

#######################          PROJECT IMPORTS         #######################

#######################          MODULE IMPORTS          #######################
from stm_flash import *
from power import *
from config import *
from term import *

#######################              ENUMS               #######################

#######################              CLASSES             #######################

class ManagerC:
    "Class to manage the state machine"
    def __init__(self) -> None:
        self.__epc_config: StmFlash_EpcConfC = None
        self.__status: TermOptionE           = TermOptionE.CONF_DEV
        self.__power                         = PwrC()
        self.__stm: StmFlashC                = StmFlashC()


    def _calib_status(self, mode: PwrModeE) -> ConfigResultE:
        '''Calibrate the EPC in the specified mode

        Args:
            - mode (PwrModeE): Mode to calibrate
        Returns:    
            - None
        Raises:
            - None
        '''
        result: ConfigResultE = ConfigResultE.ERROR
        if mode is PwrModeE.VOLT_HS:
            result = self.__power.calib_volt_hs()
        elif mode is PwrModeE.VOLT_LS:
            result = self.__power.calib_volt_ls()
        elif mode is PwrModeE.CURR:
            result = self.__power.calib_curr()
        return result


    def __conf_device(self) -> ConfigResultE:
        '''Configure the device
        Args:
            - None
        Returns:
            - result (ConfigResultE): Result of the configuration in the device
        Raises:
            - None
        '''
        log.info("Configuring device")
        self.__epc_config = TermC.query_epc_conf()
        ConfigWsC.update_path(serial_number = self.__epc_config.sn)
        result: ConfigResultE = ConfigResultE.ERROR

        info_file_path = ConfigWsC.get_info_file_path()
        if os.path.exists(info_file_path):
            with open(info_file_path, 'r', encoding = "utf-8") as file:
                info_epc = yaml.load(file, Loader = yaml.FullLoader)
        else:
            info_epc = CONFIG_DEFAULT_INFO_EPC

        info_epc['device_version']['sw'] = self.__epc_config.sw_ver
        info_epc['device_version']['hw'] = self.__epc_config.hw_ver
        info_epc['device_version']['can_ID'] = self.__epc_config.can_id
        info_epc['device_version']['s_n'] = self.__epc_config.sn

        if os.path.exists(info_file_path):
            with open(info_file_path, 'w', encoding = "utf-8") as file:
                log.info(f"Info file yaml with serial number: {self.__epc_config.sn} updated")
                yaml.dump(info_epc, file)
            result = ConfigResultE.NO_ERROR

        if result is ConfigResultE.ERROR:
            log.error(f"Error updating info file yaml with serial number: {self.__epc_config.sn}")
            TermC.show_error(status = TermOptionE.CONF_DEV, \
                             message = f"Error updating info file yaml with serial number: \
                             {self.__epc_config.sn}")
        else:
            result = self.__stm.configure_dev(epc_config = self.__epc_config)
            if result is ConfigResultE.ERROR:
                log.error("Error configuring device")
                TermC.show_error(status = TermOptionE.CONF_DEV, \
                                 message = "Error configuring device")
        return result


    def execute_machine_status(self) -> None:
        '''Execute the state machine
        Args:
            - None
        Returns:
            - None
        Raises:
            - None
        '''
        check_calib = {PwrModeE.VOLT_HS: False,
                       PwrModeE.VOLT_LS: False,
                       PwrModeE.CURR: False}
        guided = False

        while self.__status is not TermOptionE.EXIT:
            #Guided mode option
            if guided is True:
                option_guided = [None, TermOptionE.FLASH_ORIG, TermOptionE.CONF_DEV, \
                                 TermOptionE.CALIB, TermOptionE.FLASH_CALIB, TermOptionE.EXIT]
                self.__status = option_guided[option_guided.index(self.__status) + 1]
            else:
                self.__status = TermC.query_options()

            #Flash original program
            if self.__status is TermOptionE.FLASH_ORIG:
                log.info("Flashing original program")
                result_flash = self.__stm.flash_uc('STM32_orig.bin')
                if result_flash is ConfigResultE.ERROR:
                    log.error("Error flashing original program")
                    TermC.show_error(status = TermOptionE.FLASH_ORIG, \
                                     message = "Error flashing original program")

            #Configure device
            elif self.__status is TermOptionE.CONF_DEV:
                self.__conf_device()

            #Calibrate device
            elif self.__status is TermOptionE.CALIB:
                log.info("Calibrating device")
                #Check if device is configured
                if self.__epc_config is None:
                    log.error("EPC configuration not set")
                    print("EPC configuration not set, please configure device first")
                    return_conf_dev = self.__conf_device()
                else:
                    return_conf_dev = ConfigResultE.NO_ERROR

                if return_conf_dev is ConfigResultE.NO_ERROR:
                    #Guided mode
                    if guided is True:
                        options_calib_mode = [PwrModeE.VOLT_HS, PwrModeE.VOLT_LS, PwrModeE.CURR]
                        for calib_mode in options_calib_mode:
                            result_calib = self._calib_status(calib_mode)
                            if result_calib is ConfigResultE.ERROR:
                                TermC.show_error(status = TermOptionE.CALIB, \
                                                 message = f"Error calibrating device in mode \
                                                 {calib_mode}")
                            else:
                                check_calib[calib_mode] = True
                    #Manual mode
                    else:
                        calib_mode = TermC.query_calib_mode()
                        result_calib = self._calib_status(PwrModeE(calib_mode))
                        if result_calib is ConfigResultE.ERROR:
                            TermC.show_error(status = TermOptionE.CALIB, \
                                             message = f"Error calibrating device in mode \
                                             {calib_mode}")
                        else:
                            check_calib[calib_mode] = True
                else:
                    TermC.show_error(status = TermOptionE.CALIB, \
                                     message = "Device could not be calibrated")


            #Flash with calibration data
            elif self.__status is TermOptionE.FLASH_CALIB:
                log.info("Flashing with calibration data")
                #Check if device is configured
                if self.__epc_config is None:   #TODO: This condition should check if EPC sent info is the same as the __epc_config
                    log.error("EPC configuration not set")
                    return_conf_dev = self.__conf_device()

                if return_conf_dev is ConfigResultE.NO_ERROR:
                    #Check if all calibration data are set
                    if False in check_calib.values():
                        log.error("Not all calibration data are set")
                        TermC.show_error(status = TermOptionE.FLASH_CALIB, \
                                         message = "Not all calibration data are set")
                        for key, value in check_calib.items(): #TODO: Check if this is correct
                            if value is False:
                                log.error(f"Calibration data for {key} is not set")
                                result_calib = self._calib_status(mode = key)
                                if result_calib is ConfigResultE.ERROR:
                                    TermC.show_error(status = TermOptionE.CALIB, \
                                                     message = f"Error calibrating device in mode \
                                                     {key}")
                    else:
                        #Apply calibration data
                        result_calib: ConfigResultE = self.__stm.apply_calib()
                        if result_calib is ConfigResultE.ERROR:
                            log.error("Error applying calibration data")
                            TermC.show_error(status = TermOptionE.FLASH_CALIB, \
                                        message = "Error applying calibration data")
                        else:
                            #Build project
                            result_build: ConfigResultE = self.__stm.build_project()
                            if result_build is ConfigResultE.ERROR:
                                log.error("Error building project")
                                TermC.show_error(status = TermOptionE.FLASH_CALIB, \
                                                message = "Error building project")
                            else:
                                #Flash with calibration data
                                result_flash = self.__stm.flash_uc('STM32.bin')
                                if result_flash is ConfigResultE.ERROR:
                                    log.error("Error flashing with calibration data")
                                    TermC.show_error(status = TermOptionE.FLASH_CALIB, \
                                                message = "Error flashing with calibration data")
                else:
                    log.error("Device could not be calibrated")
                    TermC.show_error(status = TermOptionE.FLASH_CALIB, \
                                      message = "Device could not be calibrated")


            #Guided mode
            elif self.__status is TermOptionE.GUIDED_MODE:
                log.info("Guided mode activated")
                guided = True
                self.__status = None


if __name__ == '__main__':
    # TermC.show_intro()
    inn = input ('Connect source to high voltage side on EPC. Press enter to continue')
    while inn != '':
        inn = input ('Press enter to continue')

    man = ManagerC()
    man.execute_machine_status()
