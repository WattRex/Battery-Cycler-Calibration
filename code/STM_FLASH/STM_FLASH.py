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
from subprocess import run, PIPE
import yaml

#######################       THIRD PARTY IMPORTS        #######################

#######################          MODULE IMPORTS          #######################
from CONFIG import CONFIG_WS_c, CONFIG_Result_e

#######################          PROJECT IMPORTS         #######################


#######################              ENUMS               #######################
_EPC_CONF_PATH= f"/home/pi004/GIT_luroche/Battery-Cycler-Calibration/fw_code/firmware/project_config/EPC_CONF/epc_conf.c"

#######################              CLASSES             #######################

class STM_FLASH_Epc_Conf_c():
    '''Class to store the configuration of the EPC
    '''
    def __init__(self, software: int, hardware: int, can_id: int, serial_number: int) -> None:
        self.sw_ver: int = software
        self.hw_ver: int = hardware
        self.can_id: int = can_id
        self.sn: int = serial_number


class STM_FLASH_c():
    def __init__(self) -> None:
        self.__epc_conf: STM_FLASH_Epc_Conf_c = None
        last_release = self._getLastRelease()
        check_build = self.buildProject()
        if check_build is CONFIG_Result_e.Error:
            log.error(f"Error building STM32.bin file")
        else:
            if last_release or not os.path.exists("../fw_code/build/STM32_orig.bin"):
                os.rename("../fw_code/build/STM32.bin", "../fw_code/build/STM32_orig.bin")

    def configureDev(self, epc_config: STM_FLASH_Epc_Conf_c) -> CONFIG_Result_e:
        '''Configure the device with the specified configuration
        Args:
            - epc_config (STM_FLASH_Epc_Conf_c): Configuration to apply
        Returns:
            - result_apply_dev (CONFIG_Result_e): Result of the configuration
        Raises:
            - None
        '''
        log.info(f"Configuring the device")
        self.__epc_conf = epc_config
        result_apply_dev: CONFIG_Result_e = self._applyDevConfig()
        return result_apply_dev

    def applyCalib(self) -> CONFIG_Result_e:
        '''Apply the calibration data to the C file
        Args:
            - None
        Returns:
            - result (CONFIG_Result_e): Result of the configuration
        Raises:
            - None
        '''
        log.info(f"Applying calibration data to the C file")
        result: CONFIG_Result_e = CONFIG_Result_e.Error
        
        info_file_path = CONFIG_WS_c.getInfoFilePath()
        if os.path.exists(info_file_path):
            #Open the EPC yaml.
            with open(CONFIG_WS_c.getInfoFilePath(), 'r') as file:
                info_epc = yaml.load(file, Loader=yaml.FullLoader)
            if os.path.exists(_EPC_CONF_PATH):
                # Open the C file in read mode
                with open(_EPC_CONF_PATH, 'r') as file:
                    content = file.readlines()
                result = CONFIG_Result_e.NoError
            else:
                log.error(f"File {_EPC_CONF_PATH} not found")
        else:
            log.error(f"File {info_file_path} not found")

        if result is CONFIG_Result_e.NoError:
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
            with open(_EPC_CONF_PATH, 'w') as file:
                file.writelines(content)

            # Close the file
            file.close()
        return result


    def buildProject(self) -> CONFIG_Result_e:
        ''' Build STM32.bin
        Args:
            - None
        Returns:
            - result (CONFIG_Result_e): Result of the building
        Raises:
            - None
        '''
        log.info(f"Building STM32.bin file")
        result: CONFIG_Result_e = CONFIG_Result_e.Error
        cmd = "cd ../fw_code/build && make all"
        console = run(args=cmd, shell =True, stdout=PIPE, stderr=PIPE)

        if console.returncode == 0: #Check if the command produced an error. 0 is no error
            if len(console.stderr.decode('utf-8').replace("\n", "")) > 0: #Check if the command produced an error. if len > 0 is error
                log.error(f"Warning: {console.stderr.decode('utf-8')}")
            else:
                exist = os.path.exists("../fw_code/build/STM32.bin")
                if exist:
                    log.info(f"STM32.bin file created")
                    result = CONFIG_Result_e.NoError
                else:
                    log.error(f"STM32.bin file not created")
        else:
            log.error(f"Error: {console.stderr.decode('utf-8')}")
        return result


    def flashUC(self, binary_name: str) -> CONFIG_Result_e:
        '''Flash the STM32.
        Args:
            - None
        Returns:
            - result (CONFIG_Result_e): Result of the flashing
        Raises:
            - None
        '''
        log.info(f"Flashing {binary_name} file")
        result = CONFIG_Result_e.Error
        exist = os.path.exists(f"../fw_code/build/{binary_name}")
        if exist:
            cmd = f"cd ../fw_code/build &&  st-flash --connect-under-reset write {binary_name} 0x08000000"
            console = run(args=cmd, shell =True, stdout=PIPE, stderr=PIPE)

            if console.returncode == 0:
                if "jolly good" in console.stderr.decode('utf-8'):
                    log.info(f"{binary_name} file flashed")
                    result = CONFIG_Result_e.NoError
                else:
                    log.error(f"{binary_name} file not flashed")
            else:
                log.error(f"Error: {console.stderr.decode('utf-8')}")
        else:
            log.error(f"{binary_name} file not found")
        return result


    def _getLastRelease(self) -> bool:
        #TODO: necesitamos la ultima release para poder descargar el codigo
        log.info(f"Getting last release")
        return False


    def _applyDevConfig(self) -> CONFIG_Result_e:
        '''Apply the configuration of the device to the C file
        Args:
            - None
        Returns:
            - None
        Raises:
            - None
        '''
        result: CONFIG_Result_e = CONFIG_Result_e.Error

        info_file_path = CONFIG_WS_c.getInfoFilePath()
        if os.path.exists(info_file_path):
            with open(info_file_path, 'r') as file:
                info_epc = yaml.load(file, Loader=yaml.FullLoader)
            # Open the C file in read mode
            if os.path.exists(_EPC_CONF_PATH):
                with open(_EPC_CONF_PATH, 'r') as file:
                    content = file.readlines()
                result = CONFIG_Result_e.NoError
            else:
                log.error(f"File {_EPC_CONF_PATH} not found")
        else:
            log.error(f"File {info_file_path} not found")

        if result is CONFIG_Result_e.NoError:
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
            with open(_EPC_CONF_PATH, 'w') as file:
                # Escribe el content modificado en el archivo
                file.writelines(content)
            # Close the file
            file.close()
        return result