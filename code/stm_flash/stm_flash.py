#!/usr/bin/python3
'''
Driver of stm flash.
'''
#######################        MANDATORY IMPORTS         #######################
import sys
import os

#######################         GENERIC IMPORTS          #######################
from subprocess import run, PIPE
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
from config import ConfigWsC, ConfigResultE

#######################              ENUMS               #######################
_EPC_CONF_PATH= f"/home/pi004/GIT_luroche/Battery-Cycler-Calibration/fw_code/firmware/project_config/EPC_CONF/epc_conf.c"

#######################              CLASSES             #######################

class StmFlash_EpcConfC:
    '''Class to store the configuration of the EPC
    '''
    def __init__(self, software: int, hardware: int, can_id: int, serial_number: int) -> None:
        log.info("Creating a new EPC configuration")
        self.sw_ver: int = software
        self.hw_ver: int = hardware
        self.can_id: int = can_id
        self.sn: int = serial_number


class StmFlashC:
    def __init__(self) -> None:
        log.info("Creating a new STM flash")
        self.__epc_conf: StmFlash_EpcConfC = None
        last_release = self._get_last_release()
        check_build = self.build_project()
        if check_build is ConfigResultE.ERROR:
            log.error("Error building STM32.bin file")
        else:
            if last_release or not os.path.exists("../fw_code/build/STM32_orig.bin"):
                os.rename("../fw_code/build/STM32.bin", "../fw_code/build/STM32_orig.bin")


    def configure_dev(self, epc_config: StmFlash_EpcConfC) -> ConfigResultE:
        '''Configure the device with the specified configuration
        Args:
            - epc_config (StmFlash_EpcConfC): Configuration to apply
        Returns:
            - result_apply_dev (ConfigResultE): Result of the configuration
        Raises:
            - None
        '''
        log.info("Configuring the device")
        print("Configuring the device")
        self.__epc_conf = epc_config
        result_apply_dev: ConfigResultE = self._apply_dev_config()
        return result_apply_dev


    def apply_calib(self) -> ConfigResultE:
        '''Apply the calibration data to the C file
        Args:
            - None
        Returns:
            - result (ConfigResultE): Result of the configuration
        Raises:
            - None
        '''
        log.info("Applying calibration data to the C file")
        result: ConfigResultE = ConfigResultE.ERROR
        
        info_file_path = ConfigWsC.get_info_file_path()
        if os.path.exists(info_file_path):
            #Open the EPC yaml.
            with open(ConfigWsC.get_info_file_path(), 'r', encoding="utf-8") as file:
                info_epc = yaml.load(file, Loader=yaml.FullLoader)
            if os.path.exists(_EPC_CONF_PATH):
                # Open the C file in read mode
                with open(_EPC_CONF_PATH, 'r', encoding="utf-8") as file:
                    content = file.readlines()
                result = ConfigResultE.NO_ERROR
            else:
                log.error(f"File {_EPC_CONF_PATH} not found")
        else:
            log.error(f"File {info_file_path} not found")

        if result is ConfigResultE.NO_ERROR:
            for i, line in enumerate(content):
                # Modify the factor of the calibration data
                if 'EPC_CONF_MEAS_factors' in line:
                    i_factor = i
                    while content[i_factor] != '};\n':
                        if '//hsVolt' in content[i_factor]:
                            content[i_factor] = f"\t{info_epc['calib_data']['VOLT_HS']['factor']},\t//hsVolt\n"
                        elif '//lsVolt' in content[i_factor]:
                            content[i_factor] = f"\t{info_epc['calib_data']['VOLT_LS']['factor']},\t//lsVolt\n"
                        elif '//lsCurr' in content[i_factor]:
                            content[i_factor] = f"\t{info_epc['calib_data']['CURR']['factor']},\t//lsCurr\n"
                        i_factor += 1

                # Modify the offset of the calibration data
                elif 'EPC_CONF_MEAS_offset' in line:
                    i_offset = i
                    while content[i_offset] != '};\n':
                        if '//hsVolt' in content[i_offset]:
                            content[i_offset] = f"\t{info_epc['calib_data']['VOLT_HS']['offset']},\t//hsVolt\n"
                        elif '//lsVolt' in content[i_offset]:
                            content[i_offset] = f"\t{info_epc['calib_data']['VOLT_LS']['offset']},\t//lsVolt\n"
                        elif '//lsCurr' in content[i_offset]:
                            content[i_offset] = f"\t{info_epc['calib_data']['CURR']['offset']},\t//lsCurr\n"
                        i_offset += 1

            # Rerwite the file
            with open(_EPC_CONF_PATH, 'w', encoding="utf-8") as file:
                file.writelines(content)

            # Close the file
            file.close()
        return result


    def build_project(self) -> ConfigResultE:
        ''' Build STM32.bin
        Args:
            - None
        Returns:
            - result (ConfigResultE): Result of the building
        Raises:
            - None
        '''
        log.info("Building STM32.bin file")
        result: ConfigResultE = ConfigResultE.ERROR
        cmd = "cd ../fw_code/build && make all"
        console = run(args=cmd, shell =True, stdout=PIPE, stderr=PIPE)

        if console.returncode == 0: #Check if the command produced an error. 0 is no error
            exist = os.path.exists("../fw_code/build/STM32.bin")
            if exist:
                log.info("STM32.bin file created")
                print("STM32.bin file created")
                result = ConfigResultE.NO_ERROR
            else:
                log.error("STM32.bin file not created")
                print("STM32.bin file not created")
        else:
            log.error(f"Error: {console.stderr.decode('utf-8')}")
        return result


    def flash_uc(self, binary_name: str) -> ConfigResultE:
        '''Flash the STM32.
        Args:
            - None
        Returns:
            - result (ConfigResultE): Result of the flashing
        Raises:
            - None
        '''
        log.info(f"Flashing {binary_name} file")
        print(f"Flashing {binary_name} file")
        result = ConfigResultE.ERROR
        exist = os.path.exists(f"../fw_code/build/{binary_name}")
        if exist:
            cmd = f"cd ../fw_code/build &&  st-flash --connect-under-reset write {binary_name} 0x08000000"
            console = run(args=cmd, shell =True, stdout=PIPE, stderr=PIPE)

            if console.returncode == 0:
                if "jolly good" in console.stderr.decode('utf-8'):
                    log.info(f"{binary_name} file flashed")
                    result = ConfigResultE.NO_ERROR
                    log.error(f"Error: {console.stdout.decode('utf-8')}")
                else:
                    log.error(f"{binary_name} file not flashed")
            else:
                log.error(f"Error: {console.stderr.decode('utf-8')}")
        else:
            log.error(f"{binary_name} file not found")
        return result


    def _get_last_release(self) -> bool:
        #TODO: necesitamos la ultima release para poder descargar el codigo
        log.info("Getting last release")
        print("Getting last release")
        return False


    def _apply_dev_config(self) -> ConfigResultE:
        '''Apply the configuration of the device to the C file
        Args:
            - None
        Returns:
            - None
        Raises:
            - None
        '''
        result: ConfigResultE = ConfigResultE.ERROR

        info_file_path = ConfigWsC.get_info_file_path()
        if os.path.exists(info_file_path):
            with open(info_file_path, 'r', encoding="utf-8") as file:
                info_epc = yaml.load(file, Loader=yaml.FullLoader)
            # Open the C file in read mode
            if os.path.exists(_EPC_CONF_PATH):
                with open(_EPC_CONF_PATH, 'r', encoding="utf-8") as file:
                    content = file.readlines()
                result = ConfigResultE.NO_ERROR
            else:
                log.error(f"File {_EPC_CONF_PATH} not found")
        else:
            log.error(f"File {info_file_path} not found")

        if result is ConfigResultE.NO_ERROR:
            # Modify the information of the device
            for i, line in enumerate(content):
                if 'EPC_CONF_info' in line:
                    i_info = i
                    while content[i_info] != '};\n':
                        if '//id' in content[i_info]:
                            content[i_info] = f"{self.__epc_conf.can_id},\t//id\n"
                        elif '//fwVer' in content[i_info]:
                            content[i_info] = f"{self.__epc_conf.sw_ver},\t//fwVer\n"
                        elif '//hwVer' in content[i_info]:
                            content[i_info] = f"{self.__epc_conf.hw_ver},\t//hwVer\n"
                        elif '//sn' in content[i_info]:
                            content[i_info] = f"{self.__epc_conf.sn},\t//sn\n"
                        i_info += 1

            # Rerwite the file
            with open(_EPC_CONF_PATH, 'w', encoding="utf-8") as file:
                # Escribe el content modificado en el archivo
                file.writelines(content)
            # Close the file
            file.close()
        return result
