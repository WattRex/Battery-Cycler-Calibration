################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (10.3-2021.10)
################################################################################

ELF_SRCS := 
OBJ_SRCS := 
S_SRCS := 
C_SRCS := 
S_UPPER_SRCS := 
O_SRCS := 
CYCLO_FILES := 
SIZE_OUTPUT := 
OBJDUMP_LIST := 
SU_FILES := 
EXECUTABLES := 
OBJS := 
MAP_FILES := 
S_DEPS := 
S_UPPER_DEPS := 
C_DEPS := 

# Every subdirectory with source files must be described here
SUBDIRS := \
Core/Src \
Core/Startup \
Drivers/STM32F3xx_HAL_Driver/Src \
Sources/APP/APP_IFACE \
Sources/APP/APP_SALG \
Sources/EPC_CONF \
Sources/EPC_ST \
Sources/HAL/HAL_ADC \
Sources/HAL/HAL_CAN \
Sources/HAL/HAL_GPIO \
Sources/HAL/HAL_PWM \
Sources/HAL/HAL_STS \
Sources/HAL/HAL_SYS \
Sources/HAL/HAL_TMR \
Sources/HAL/HAL_WDG \
Sources/MID/MID_COMM \
Sources/MID/MID_DABS \
Sources/MID/MID_PWR \
Sources/MID/MID_REG \
Sources/Test/HAL \
Sources/Test/MID \
Sources/Test

mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
ws_path = $(patsubst %/build/, %/firmware,$(dir $(mkfile_path)))
SOURCE_PATH := $(strip $(ws_path))
