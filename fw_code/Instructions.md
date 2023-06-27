## 1. Step to compile and flash STM32CubeIDE project from command line:
- Change desired configuration on `fw_code/firmware/Sources/EPC_CONF/epc_conf.*`
- Compile the project: 
```sh
cd fw_code/build
make all
```

It will generate an STM32.elf binary file, that will be flashed to uC.
- Flash binary: `st-flash write STM32.bin 0x08000000`
- Flash reset uC: `st-flash reset` 

## 4. Install Pack GNU Arm Embedded GCC
- Install xpm (XPack packet manager): `npm install --global xpm@latest`
- Install GCC compiler: 
```
mkdir -p <compiler_base_folder>
cd <compiler_base_folder>
xpm init # Only at first use.

xpm install @xpack-dev-tools/arm-none-eabi-gcc@latest --verbose
```


## 2. Install ST-LINK framework:
Source: [Compiling from sources documentation](https://github.com/stlink-org/stlink/blob/develop/doc/compiling.md)
Source: [Flash a ST board with STLINK and Linux](https://stackoverflow.com/questions/63011922/flash-a-st-board-with-stlink-and-linux)
- Clone git repo: `git clone https://github.com/stlink-org/stlink.git`
- Install libusb lib: `sudo apt install libusb-1.0-0-dev` 
- Change `--Wmissing-variable-declarations` compilation flag to `-Wmissing-declarations` on `~/build/cmake/modules/c_flags.cmake`
- Comment flag `-Wshorten-64-to-32`
- Make project: `make clean && make release`
- Install package: `sudo make install`
- Build a Debian Package: `sudo make package`
- Execute rules to accomplish the minimum access privilege: 
```
    $ sudo cp -a config/udev/rules.d/* /etc/udev/rules.d/
    $ sudo udevadm control --reload-rules
    $ sudo udevadm trigger
```

## 3. Upgrade nodejs
Souirce: [Updating Node.js on a Raspberry Pi Zero](https://yatil.net/blog/node-on-pi)
- Remove previous Nodejs: `sudo apt remove nodejs`
- Download unofficial package: `curl -o node-v20.3.1-linux-armv6l.tar.gz https://unofficial-builds.nodejs.org/download/release/v20.3.1/node-v20.3.1-linux-armv6l.tar.gz`
- Extract files: `tar -zxvf node-v20.3.1-linux-armv6l.tar.gz`
- Move the files over from the extracted directory: `sudo cp -r node-v20.3.1-linux-armv6l/* /usr/local/`
- In case you are greeted with the following error message:
```
cp: cannot create regular file '/usr/local/bin/node': Text file bus
```

You need to remove the node file first: `sudo rm /usr/local/bin/node`
- Restart the Raspberry Pi Zero W


## References
- [Install Arm GNU Toolchain on Ubuntu 22.04](https://lindevs.com/install-arm-gnu-toolchain-on-ubuntu)
- [Using Raspberry Pi for Embedded Systems Development](https://rawats.medium.com/using-raspberry-pi-for-embedded-systems-development-part-1-2d32c42acb5c)
- Flash stm32 with raspberry: [stm32duino-raspberrypi](https://github.com/koendv/stm32duino-raspberrypi)