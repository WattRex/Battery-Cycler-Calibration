################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (10.3-2021.10)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
S_SRCS += \
$(SOURCE_PATH)/STM32/Core/Startup/startup_stm32f334r8tx.s 

OBJS += \
./Core/Startup/startup_stm32f334r8tx.o 

S_DEPS += \
./Core/Startup/startup_stm32f334r8tx.d 


# Each subdirectory must supply rules for building sources it contributes
Core/Startup/%.o: $(SOURCE_PATH)/STM32/Core/Startup/%.s Core/Startup/subdir.mk
	arm-none-eabi-gcc -mcpu=cortex-m4 -c \
	-I"$(SOURCE_PATH)/Sources/HAL/HAL_ADC" \
	-I"$(SOURCE_PATH)/Sources/HAL/HAL_CAN" \
	-I"$(SOURCE_PATH)/Sources/HAL/HAL_GPIO" \
	-I"$(SOURCE_PATH)/Sources/HAL/HAL_SYS" \
	-I"$(SOURCE_PATH)/Sources/HAL/HAL_TMR" \
	-I"$(SOURCE_PATH)/Sources/HAL/HAL_WDG" \
	-I"$(SOURCE_PATH)/Sources/EPC_CONF" \
	-I"$(SOURCE_PATH)/Sources/HAL/HAL_PWM" \
	-I"$(SOURCE_PATH)/Sources/MID/MID_PWR" \
	-I"$(SOURCE_PATH)/Sources/MID/MID_DABS" \
	-I"$(SOURCE_PATH)/Sources/MID/MID_COMM" \
	-I"$(SOURCE_PATH)/Sources/APP/APP_SALG" \
	-I"$(SOURCE_PATH)/Sources/APP/APP_IFACE" \
	-I"$(SOURCE_PATH)/Sources/Test" \
	-I"$(SOURCE_PATH)/Sources/Test/HAL" \
	-I"$(SOURCE_PATH)/Sources/EPC_ST" \
	-I"$(SOURCE_PATH)/Sources/HAL/HAL_STS" \
	-I"$(SOURCE_PATH)/Sources/MID/MID_REG" -x assembler-with-cpp -MMD -MP -MF"$(@:%.o=%.d)" \
	-MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@" "$<"

clean: clean-Core-2f-Startup

clean-Core-2f-Startup:
	-$(RM) ./Core/Startup/startup_stm32f334r8tx.d ./Core/Startup/startup_stm32f334r8tx.o

.PHONY: clean-Core-2f-Startup

