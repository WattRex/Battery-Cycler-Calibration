#!/usr/bin/python3
'''
Driver of stm flash.
'''
#######################        MANDATORY IMPORTS         #######################
import sys
import os
import re
#######################         GENERIC IMPORTS          #######################
from subprocess import run, PIPE
from yaml import load, FullLoader

#######################       THIRD PARTY IMPORTS        #######################

#######################      SYSTEM ABSTRACTION IMPORTS  #######################
sys.path.append(os.getcwd())
from system_logger_tool import sys_log_logger_get_module_logger # pylint: disable=wrong-import-position
log = sys_log_logger_get_module_logger(__name__)

#######################          PROJECT IMPORTS         #######################

#######################          MODULE IMPORTS          #######################
from config import ConfigWsC, ConfigResultE # pylint: disable=wrong-import-position

#######################              ENUMS               #######################
_EPC_CONF_PATH= "/home/pi004/GIT_luroche/Battery-Cycler-Calibration/fw_code"+\
                "/firmware/Sources/EPC_CONF/epc_conf.c"

#######################              CLASSES             #######################

class StmFlashEpcConfC:
    "Class to store the configuration of the EPC"
    def __init__(self, software: int, hardware: int, can_id: int, serial_number: int) -> None:
        log.info("Creating a new EPC configuration")
        self.sw_ver: int = software
        self.hw_ver: int = hardware
        self.can_id: int = can_id
        self.sn: int     = serial_number # pylint: disable=invalid-name


class StmFlashC:
    "Class method for flash the epc"
    def __init__(self) -> None:
        log.info("Creating a new STM flash")
        self.__epc_conf: StmFlashEpcConfC = None
        last_release = self._get_last_release()
        check_build = self.build_project()
        if check_build is ConfigResultE.ERROR:
            log.error("Error building STM32.bin file")
        else:
            if last_release or not os.path.exists("../fw_code/build/STM32_orig.bin"):
                os.rename("../fw_code/build/STM32.bin", "../fw_code/build/STM32_orig.bin")


    def configure_dev(self, epc_config: StmFlashEpcConfC) -> ConfigResultE:
        '''Configure the device with the specified configuration
        Args:
            - epc_config (StmFlashEpcConfC): Configuration to apply
        Returns:
            - result_apply_dev (ConfigResultE): Result of the configuration
        Raises:
            - None
        '''
        log.info("Configuring the device")
        print("Configuring the device.")
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
                info_epc = load(file, Loader = FullLoader)
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
                # Modify maximun values of the calibration data
                if 'EPC_CONF_MEAS_max_value' in line:
                    i_max_value = i
                    while content[i_max_value] != '};\n':
                        if '//lsVolt' in content[i_max_value]:
                            content[i_max_value] = '4095,\t//lsVolt\n'
                        elif '//lsCurr' in content[i_max_value]:
                            content[i_max_value] = '4095,\t//lsCurr\n'
                        elif '//hsVolt' in content[i_max_value]:
                            content[i_max_value] = '4095,\t//hsVolt\n'
                        elif '//tempBody' in content[i_max_value]:
                            content[i_max_value] = '4095,\t//tempBody\n'
                        elif '//tempAnod' in content[i_max_value]:
                            content[i_max_value] = '4095,\t//tempAnod\n'
                        elif '//tempAmb' in content[i_max_value]:
                            content[i_max_value] = '4095\t//tempAmb\n'
                        i_max_value += 1

                # Modify the factor of the calibration data
                if 'EPC_CONF_MEAS_factors' in line:
                    i_factor = i
                    while content[i_factor] != '};\n':
                        if '//hsVolt' in content[i_factor]:
                            content[i_factor] = f"\t{info_epc['calib_data']['VOLT_HS']['factor']}"+\
                            ",\t//hsVolt\n"
                        elif '//lsVolt' in content[i_factor]:
                            content[i_factor] = f"\t{info_epc['calib_data']['VOLT_LS']['factor']}"+\
                                ",\t//lsVolt\n"
                        elif '//lsCurr' in content[i_factor]:
                            content[i_factor] = f"\t{info_epc['calib_data']['CURR']['factor']}"+\
                                ",\t//lsCurr\n"
                        i_factor += 1

                # Modify the offset of the calibration data
                elif 'EPC_CONF_MEAS_offset' in line:
                    i_offset = i
                    while content[i_offset] != '};\n':
                        if '//hsVolt' in content[i_offset]:
                            content[i_offset] = f"\t{info_epc['calib_data']['VOLT_HS']['offset']}"+\
                                ",\t//hsVolt\n"
                        elif '//lsVolt' in content[i_offset]:
                            content[i_offset] = f"\t{info_epc['calib_data']['VOLT_LS']['offset']}"+\
                                ",\t//lsVolt\n"
                        elif '//lsCurr' in content[i_offset]:
                            content[i_offset] = f"\t{info_epc['calib_data']['CURR']['offset']}"+\
                                ",\t//lsCurr\n"
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
        archive_bin = os.path.exists("../fw_code/build/STM32.bin")

        console = run(args=cmd, shell =True, stdout=PIPE, stderr=PIPE, check=False)
        if console.returncode == 0: #Check if the command produced an error. 0 is no error
            archive_bin = os.path.exists("../fw_code/build/STM32.bin")
            if archive_bin:
                log.info("STM32.bin file created")
                result = ConfigResultE.NO_ERROR
            else:
                log.error("STM32.bin file not created")
                print("STM32.bin file not created.")
        else:
            log.error(f"Error: {console.stderr.decode('utf-8')}")


        return result


    def flash_uc(self, binary_name: str) -> ConfigResultE:
        '''Flash the STM32.
        Args:
            - binary_name (str): Name of the binary to flash
        Returns:
            - result (ConfigResultE): Result of the flashing
        Raises:
            - None
        '''
        log.info(f"Flashing {binary_name} file")
        print(f"Flashing {binary_name} file.")
        result = ConfigResultE.ERROR
        exist = os.path.exists(f"../fw_code/build/{binary_name}")
        if exist:
            cmd = f"cd ../fw_code/build &&  st-flash --connect-under-reset write {binary_name} 0x08000000" # pylint: disable=line-too-long
            console = run(args=cmd, shell =True, stdout=PIPE, stderr=PIPE, check=False)
            if console.returncode == 0:
                if "jolly good" in console.stderr.decode('utf-8'):
                    log.info(f"{binary_name} file flashed: {console.stdout.decode('utf-8')}")
                    #now reset the device
                    result = ConfigResultE.NO_ERROR
                else:
                    log.error(f"{binary_name} file not flashed")
            else:
                log.error(f"Error: {console.stderr.decode('utf-8')}")
        else:
            log.error(f"{binary_name} file not found")
        return result


    def _get_last_release(self) -> bool:
        #Download the latest release
        console = run(args = "./stm_flash/get_release.sh", shell =True, stdout=PIPE, \
                        stderr=PIPE, check=True)
        stdout = console.stdout.decode('utf-8')

        name_targz = re.search(r'\S+\.tar\.gz', stdout)
        name_targz = name_targz.group()
        name_targz = name_targz.replace("'", "")
        file = name_targz.replace('.tar.gz', '')

        #Decompress the file and delete the .tar.gz
        cmd = f"tar -xvf {name_targz } && rm {name_targz}"
        console = run(args = cmd, shell =True, stdout=PIPE, stderr=PIPE, check=True)

        #Move the firmware folder
        cmd = f"rm -r ../fw_code/firmware/ && mv {file}/firmware/ ../fw_code/ && rm -r {file}"
        console = run(args = cmd, shell =True, stdout=PIPE, stderr=PIPE, check=True)

        #Move the EPC_CONF from project_config to Sources folder
        cmd = "cp -r ../fw_code/firmware/project_config/EPC_CONF/ ../fw_code/firmware/Sources/"
        console = run(args = cmd, shell =True, stdout=PIPE, stderr=PIPE, check=True)
        if console.returncode == 0:
            result = True
        else:
            result = False
        return result


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
            hw_ver = bin(self.__epc_conf.hw_ver)
            print(hw_ver)
            for i, line in enumerate(content):
                if '/*		ID CONF		*/' in line:
                    i_info = i
                    while content[i_info] != '};\n':
                        if '#define _CAN_ID' in content[i_info]:
                            content[i_info] = f"#define _CAN_ID\t{self.__epc_conf.can_id}\n"
                        elif '#define _FW_VER' in content[i_info]:
                            content[i_info] = f"#define _FW_VER\t{self.__epc_conf.sw_ver}\n"
                        elif '#define _S_N' in content[i_info]:
                            content[i_info] = f"#define _S_N\t{self.__epc_conf.sn}\n"
                        elif '#define _HW_REVIEW' in content[i_info]:
                            content[i_info] = f"#define _HW_REVIEW\t{int(hw_ver[-3:],2)}\t // Review\n" # pylint: disable=line-too-long
                        elif '#define _HW_VENT' in content[i_info]:
                            content[i_info] = f"#define _HW_VENT\t{int(hw_ver[-4],2)}\t // Vent\n"
                        elif '#define _HW_CONNECTOR' in content[i_info]:
                            content[i_info] = f"#define _HW_CONNECTOR\t{int(hw_ver[-7:-4],2)}\t // Connector\n" # pylint: disable=line-too-long
                        elif '#define _HW_ANODE' in content[i_info]:
                            content[i_info] = f"#define _HW_ANODE\t{int(hw_ver[-9:-7],2)}\t // T anode type\n" # pylint: disable=line-too-long
                        elif '#define _HW_STS' in content[i_info]:
                            content[i_info] = f"#define _HW_STS\t{int(hw_ver[-10],2)}\t // T body\n"
                        elif '#define _HW_AMB' in content[i_info]:
                            try:
                                amb= int(hw_ver[-11],2)
                            except:
                                amb= 0
                            content[i_info] = f"#define _HW_AMB\t{amb}\t // T amb\n"
                        i_info += 1

            # Rewrite the file
            with open(_EPC_CONF_PATH, 'w', encoding="utf-8") as file:
                # Escribe el content modificado en el archivo
                file.writelines(content)
            # Close the file
            file.close()
        return result
