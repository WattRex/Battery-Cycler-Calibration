################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (10.3-2021.10)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
$(SOURCE_PATH)/STM32/Core/Src/adc.c \
$(SOURCE_PATH)/STM32/Core/Src/can.c \
$(SOURCE_PATH)/STM32/Core/Src/dma.c \
$(SOURCE_PATH)/STM32/Core/Src/gpio.c \
$(SOURCE_PATH)/STM32/Core/Src/hrtim.c \
$(SOURCE_PATH)/STM32/Core/Src/i2c.c \
$(SOURCE_PATH)/STM32/Core/Src/iwdg.c \
$(SOURCE_PATH)/STM32/Core/Src/main.c \
$(SOURCE_PATH)/STM32/Core/Src/stm32f3xx_hal_msp.c \
$(SOURCE_PATH)/STM32/Core/Src/stm32f3xx_it.c \
$(SOURCE_PATH)/STM32/Core/Src/syscalls.c \
$(SOURCE_PATH)/STM32/Core/Src/sysmem.c \
$(SOURCE_PATH)/STM32/Core/Src/system_stm32f3xx.c \
$(SOURCE_PATH)/STM32/Core/Src/tim.c 

OBJS += \
./Core/Src/adc.o \
./Core/Src/can.o \
./Core/Src/dma.o \
./Core/Src/gpio.o \
./Core/Src/hrtim.o \
./Core/Src/i2c.o \
./Core/Src/iwdg.o \
./Core/Src/main.o \
./Core/Src/stm32f3xx_hal_msp.o \
./Core/Src/stm32f3xx_it.o \
./Core/Src/syscalls.o \
./Core/Src/sysmem.o \
./Core/Src/system_stm32f3xx.o \
./Core/Src/tim.o 

C_DEPS += \
./Core/Src/adc.d \
./Core/Src/can.d \
./Core/Src/dma.d \
./Core/Src/gpio.d \
./Core/Src/hrtim.d \
./Core/Src/i2c.d \
./Core/Src/iwdg.d \
./Core/Src/main.d \
./Core/Src/stm32f3xx_hal_msp.d \
./Core/Src/stm32f3xx_it.d \
./Core/Src/syscalls.d \
./Core/Src/sysmem.d \
./Core/Src/system_stm32f3xx.d \
./Core/Src/tim.d 


# Each subdirectory must supply rules for building sources it contributes
Core/Src/%.o Core/Src/%.su Core/Src/%.cyclo: $(SOURCE_PATH)/STM32/Core/Src/%.c Core/Src/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -DUSE_HAL_DRIVER -DSTM32F334x8 -c \
	-I"$(SOURCE_PATH)/Sources/HAL/HAL_ADC" \
	-I"$(SOURCE_PATH)/Sources/HAL/HAL_CAN" \
	-I"$(SOURCE_PATH)/Sources/HAL/HAL_GPIO" \
	-I"$(SOURCE_PATH)/Sources/HAL/HAL_SYS" \
	-I"$(SOURCE_PATH)/Sources/HAL/HAL_TMR" \
	-I"$(SOURCE_PATH)/Sources/HAL/HAL_WDG" \
	-I"$(SOURCE_PATH)/Sources/HAL/HAL_STS" \
	-I"$(SOURCE_PATH)/Sources/HAL/HAL_PWM" \
	-I"$(SOURCE_PATH)/Sources/MID/MID_PWR" \
	-I"$(SOURCE_PATH)/Sources/MID/MID_DABS" \
	-I"$(SOURCE_PATH)/Sources/MID/MID_COMM" \
	-I"$(SOURCE_PATH)/Sources/MID/MID_REG" \
	-I"$(SOURCE_PATH)/Sources/APP/APP_SALG" \
	-I"$(SOURCE_PATH)/Sources/APP/APP_IFACE" \
	-I"$(SOURCE_PATH)/Sources/EPC_CONF" \
	-I"$(SOURCE_PATH)/Sources/EPC_ST" \
	-I"$(SOURCE_PATH)/Sources/Test" \
	-I"$(SOURCE_PATH)/Sources/Test/HAL" \
	-I"$(SOURCE_PATH)/STM32/Core/Inc" \
	-I"$(SOURCE_PATH)/STM32/Drivers/STM32F3xx_HAL_Driver/Inc" \
	-I"$(SOURCE_PATH)/STM32/Drivers/CMSIS/Device/ST/STM32F3xx/Include" \
	-I"$(SOURCE_PATH)/STM32/Drivers/STM32F3xx_HAL_Driver/Inc/Legacy" \
	-I"$(SOURCE_PATH)/STM32/Drivers/CMSIS/Include" -Os -ffunction-sections \
	-fdata-sections -Wall -fstack-usage -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" \
	--specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-Core-2f-Src

clean-Core-2f-Src:
	-$(RM) ./Core/Src/adc.cyclo ./Core/Src/adc.d ./Core/Src/adc.o ./Core/Src/adc.su \
	 ./Core/Src/can.cyclo ./Core/Src/can.d ./Core/Src/can.o ./Core/Src/can.su \
	 ./Core/Src/dma.cyclo ./Core/Src/dma.d ./Core/Src/dma.o ./Core/Src/dma.su \
	 ./Core/Src/gpio.cyclo ./Core/Src/gpio.d ./Core/Src/gpio.o ./Core/Src/gpio.su \
	 ./Core/Src/hrtim.cyclo ./Core/Src/hrtim.d ./Core/Src/hrtim.o ./Core/Src/hrtim.su \
	 ./Core/Src/i2c.cyclo ./Core/Src/i2c.d ./Core/Src/i2c.o ./Core/Src/i2c.su \
	 ./Core/Src/iwdg.cyclo ./Core/Src/iwdg.d ./Core/Src/iwdg.o ./Core/Src/iwdg.su \
	 ./Core/Src/main.cyclo ./Core/Src/main.d ./Core/Src/main.o ./Core/Src/main.su \
	 ./Core/Src/stm32f3xx_hal_msp.cyclo ./Core/Src/stm32f3xx_hal_msp.d \
	 ./Core/Src/stm32f3xx_hal_msp.o ./Core/Src/stm32f3xx_hal_msp.su \
	 ./Core/Src/stm32f3xx_it.cyclo ./Core/Src/stm32f3xx_it.d ./Core/Src/stm32f3xx_it.o \
	 ./Core/Src/stm32f3xx_it.su ./Core/Src/syscalls.cyclo ./Core/Src/syscalls.d \
	 ./Core/Src/syscalls.o ./Core/Src/syscalls.su ./Core/Src/sysmem.cyclo \
	 ./Core/Src/sysmem.d ./Core/Src/sysmem.o ./Core/Src/sysmem.su \
	 ./Core/Src/system_stm32f3xx.cyclo ./Core/Src/system_stm32f3xx.d \
	 ./Core/Src/system_stm32f3xx.o ./Core/Src/system_stm32f3xx.su ./Core/Src/tim.cyclo \
	 ./Core/Src/tim.d ./Core/Src/tim.o ./Core/Src/tim.su

.PHONY: clean-Core-2f-Src

