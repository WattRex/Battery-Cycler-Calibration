################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (10.3-2021.10)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
$(SOURCE_PATH)/Sources/HAL/HAL_CAN/hal_can.c 

OBJS += \
./Sources/HAL/HAL_CAN/hal_can.o 

C_DEPS += \
./Sources/HAL/HAL_CAN/hal_can.d 


# Each subdirectory must supply rules for building sources it contributes
Sources/HAL/HAL_CAN/hal_can.o: $(SOURCE_PATH)/Sources/HAL/HAL_CAN/hal_can.c Sources/HAL/HAL_CAN/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -DUSE_HAL_DRIVER -DSTM32F334x8 -c -I"$(SOURCE_PATH)/Sources/HAL/HAL_ADC" -I"$(SOURCE_PATH)/Sources/HAL/HAL_CAN" -I"$(SOURCE_PATH)/Sources/HAL/HAL_GPIO" -I"$(SOURCE_PATH)/Sources/HAL/HAL_SYS" -I"$(SOURCE_PATH)/Sources/HAL/HAL_TMR" -I"$(SOURCE_PATH)/Sources/HAL/HAL_WDG" -I"$(SOURCE_PATH)/Sources/HAL/HAL_STS" -I"$(SOURCE_PATH)/Sources/HAL/HAL_PWM" -I"$(SOURCE_PATH)/Sources/MID/MID_PWR" -I"$(SOURCE_PATH)/Sources/MID/MID_DABS" -I"$(SOURCE_PATH)/Sources/MID/MID_COMM" -I"$(SOURCE_PATH)/Sources/MID/MID_REG" -I"$(SOURCE_PATH)/Sources/APP/APP_SALG" -I"$(SOURCE_PATH)/Sources/APP/APP_IFACE" -I"$(SOURCE_PATH)/Sources/EPC_CONF" -I"$(SOURCE_PATH)/Sources/EPC_ST" -I"$(SOURCE_PATH)/Sources/Test" -I"$(SOURCE_PATH)/Sources/Test/HAL" -I"$(SOURCE_PATH)/STM32/Core/Inc" -I"$(SOURCE_PATH)/STM32/Drivers/STM32F3xx_HAL_Driver/Inc" -I"$(SOURCE_PATH)/STM32/Drivers/CMSIS/Device/ST/STM32F3xx/Include" -I"$(SOURCE_PATH)/STM32/Drivers/STM32F3xx_HAL_Driver/Inc/Legacy" -I"$(SOURCE_PATH)/STM32/Drivers/CMSIS/Include" -Os -ffunction-sections -fdata-sections -Wall -fstack-usage -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-Sources-2f-HAL-2f-HAL_CAN

clean-Sources-2f-HAL-2f-HAL_CAN:
	-$(RM) ./Sources/HAL/HAL_CAN/hal_can.cyclo ./Sources/HAL/HAL_CAN/hal_can.d ./Sources/HAL/HAL_CAN/hal_can.o ./Sources/HAL/HAL_CAN/hal_can.su

.PHONY: clean-Sources-2f-HAL-2f-HAL_CAN

