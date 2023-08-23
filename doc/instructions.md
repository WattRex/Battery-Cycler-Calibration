# CALIBRATION AND FLASH GUIDE
This app consists of a station to flash and calibrate differents EPCs.
From the code folder, the program to run is ```./manager/manager.py```

## About the calibration station
We need the following elements:
- A power supply to establish the voltage and current. Minimun ranges:
    -   0.5V - 14V.
    -   -1.5A - 1.5A.
- Two multimeters to measure the voltage and current. Minimun ranges:
    -   0.5V - 14V.
    -   -1.5A - 1.5A.
- A raspberry pi to run the program and communicate with the devices.
- The EPC to calibrate.
- External battery.

All these elements must be connected via USB to the raspberry pi.

To get started, download the entire project folder to the raspberry and run ```pip3 install -r requirements.txt``` command to install all the necessary python packages.


## About the app
In the principal menu there are seven options:
    
    1. Flash original program.
    2. Configure device.
    3. Calibrate device.
    4. Flash with calibration data.
    5. Guided mode.
    6. Flash other EPC.
    7. Exit.


### 1. Flash original program.
This option reset the EPC with the last release.


### 2. Configure device.
The second option is used to indicate the serial number, software version, CAN ID and hardware version of the EPC.
To indicate the hardware version, the following questions must be answered:

    1. Does the EPC have a fan?
        - No
        - Yes
    2. What type of connector does the EPC have?
        - 18650
        - Banana
    3. What type of temperature sensor in anode does the EPC have?
        - No anode.
        - Ring NTC.
        - Plastic NTC.
    4. What type of temperature sensor in body does the EPC have?
        - No STS.
        - STS Sens.
    5. What type of temperature sensor in ambient does the EPC have?
        - No sensor.
        - Plastic NTC.


### 3. Calibrate device.
In the epc you have to perform three types of calibration:

    1. Voltage high side.
    2. Voltage low side.
    3. Current.

Each time it is calibrated, a .csv file will be created with the data obtained from the source, the multimeter and the epc device inside the board folder. If there is already previous data, you will have to confirm if you want to overwrite the data.
If a device configuration does not exist, it will be executed before starting the calibration.

#### 3.1 Voltage high side.
Calibrate the high side voltage.
- Minimun high side voltage: 5V.
- Maximun high side voltage: 14V.

Before starting the calibration, the station must be wired as follows:
¿¿¿¿????

#### 3.2. Voltage low side.
Calibrate the low side voltage.
- Minimun low side voltage: 0.5V.
- Maximun low side voltage: 5V.

Before starting the calibration, the station must be wired as follows:
¿¿¿¿????

#### 3.3. Current.
Calibrate the low side current.
- Minimun low side current: -1.5A.
- Maximun low side current: 1.5A.

Before starting the calibration, the station must be wired as follows:
¿¿¿¿????
(Connect external battery)

### 4. Flash with calibration data.
Flash the EPC with new calibration.
Before executing this option, the device must be configured and all calibrations performed. If they have not yet been carried out, the program will indicate it and guide you to carry out the remaining steps prior to new calibration.


### 5. Guided mode.
It is used to change the mode to guided. The program indicates the steps that must be followed.


### 6. Flash other EPC.
The program is reset to configure a new EPC


### 7. Exit.
Close the program.


## Used technologies
* [Source] (https://elektroautomatik.com/shop/en/products/programmable-dc-laboratory-power-supplies/dc-laboratory-power-supplies/series-ps-2000b-br-100-up-to-332-w/724/power-supply-2x0..84v/0..5a)

* [Multimeters] (https://www.bkprecision.com/products/vids/2831E?)

* [Raspberry Pi] (https://www.raspberrypi.com/products/raspberry-pi-zero/)