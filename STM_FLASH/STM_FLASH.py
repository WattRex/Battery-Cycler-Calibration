import yaml


class EPC_CONF_c():
    def __init__(self, serial_number) -> None:
        self._sw_ver: int = None
        self._hw_ver: int = None
        self._can_id: int = None
        self._epc_sn: int = serial_number
        self._obtainInfo()


    def _obtainInfo(self):
        name_path = f"CALIB_MAIN/DATAS/data_{self._epc_sn}"
        name_path_info = f"{name_path}/epc_calib_info_{self._epc_sn}.yaml"
        with open(name_path_info, 'r') as file:
            conf_dev = yaml.load(file, Loader=yaml.FullLoader)
            self._sw_ver = conf_dev['device_version']['sw']
            self._hw_ver = conf_dev['device_version']['hw']
            self._can_id = conf_dev['device_version']['can_ID']


class STM_FLASH_c():
    def __init__(self) -> None:
        pass
    def ConfigureProject(epc_config: EPC_CONF_c):
        pass
    def BuildProject():
        pass
    def Flash_uC():
        pass