################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (10.3-2021.10)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
$(SOURCE_PATH)/Sources/Test/HAL/hal_adc_test.c \
$(SOURCE_PATH)/Sources/Test/HAL/hal_can_test.c \
$(SOURCE_PATH)/Sources/Test/HAL/hal_gpio_test.c \
$(SOURCE_PATH)/Sources/Test/HAL/hal_pwm_test.c \
$(SOURCE_PATH)/Sources/Test/HAL/hal_sts_test.c \
$(SOURCE_PATH)/Sources/Test/HAL/hal_tmr_test.c \
$(SOURCE_PATH)/Sources/Test/HAL/hal_wdg_test.c 

OBJS += \
./Sources/Test/HAL/hal_adc_test.o \
./Sources/Test/HAL/hal_can_test.o \
./Sources/Test/HAL/hal_gpio_test.o \
./Sources/Test/HAL/hal_pwm_test.o \
./Sources/Test/HAL/hal_sts_test.o \
./Sources/Test/HAL/hal_tmr_test.o \
./Sources/Test/HAL/hal_wdg_test.o 

C_DEPS += \
./Sources/Test/HAL/hal_adc_test.d \
./Sources/Test/HAL/hal_can_test.d \
./Sources/Test/HAL/hal_gpio_test.d \
./Sources/Test/HAL/hal_pwm_test.d \
./Sources/Test/HAL/hal_sts_test.d \
./Sources/Test/HAL/hal_tmr_test.d \
./Sources/Test/HAL/hal_wdg_test.d 


# Each subdirectory must supply rules for building sources it contributes
Sources/Test/HAL/hal_adc_test.o: $(SOURCE_PATH)/Sources/Test/HAL/hal_adc_test.c Sources/Test/HAL/subdir.mk

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

Sources/Test/HAL/hal_can_test.o: $(SOURCE_PATH)/Sources/Test/HAL/hal_can_test.c Sources/Test/HAL/subdir.mk
	
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

Sources/Test/HAL/hal_gpio_test.o: $(SOURCE_PATH)/Sources/Test/HAL/hal_gpio_test.c Sources/Test/HAL/subdir.mk
	
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

Sources/Test/HAL/hal_pwm_test.o: $(SOURCE_PATH)/Sources/Test/HAL/hal_pwm_test.c Sources/Test/HAL/subdir.mk
	
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

Sources/Test/HAL/hal_sts_test.o: $(SOURCE_PATH)/Sources/Test/HAL/hal_sts_test.c Sources/Test/HAL/subdir.mk

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

Sources/Test/HAL/hal_tmr_test.o: $(SOURCE_PATH)/Sources/Test/HAL/hal_tmr_test.c Sources/Test/HAL/subdir.mk
	
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

Sources/Test/HAL/hal_wdg_test.o: $(SOURCE_PATH)/Sources/Test/HAL/hal_wdg_test.c Sources/Test/HAL/subdir.mk

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

clean: clean-Sources-2f-Test-2f-HAL

clean-Sources-2f-Test-2f-HAL:
	-$(RM) ./Sources/Test/HAL/hal_adc_test.cyclo ./Sources/Test/HAL/hal_adc_test.d \
	./Sources/Test/HAL/hal_adc_test.o ./Sources/Test/HAL/hal_adc_test.su \
	./Sources/Test/HAL/hal_can_test.cyclo ./Sources/Test/HAL/hal_can_test.d \
	./Sources/Test/HAL/hal_can_test.o ./Sources/Test/HAL/hal_can_test.su \
	./Sources/Test/HAL/hal_gpio_test.cyclo ./Sources/Test/HAL/hal_gpio_test.d \
	./Sources/Test/HAL/hal_gpio_test.o ./Sources/Test/HAL/hal_gpio_test.su \
	./Sources/Test/HAL/hal_pwm_test.cyclo ./Sources/Test/HAL/hal_pwm_test.d \
	./Sources/Test/HAL/hal_pwm_test.o ./Sources/Test/HAL/hal_pwm_test.su \
	./Sources/Test/HAL/hal_sts_test.cyclo ./Sources/Test/HAL/hal_sts_test.d \
	./Sources/Test/HAL/hal_sts_test.o ./Sources/Test/HAL/hal_sts_test.su \
	./Sources/Test/HAL/hal_tmr_test.cyclo ./Sources/Test/HAL/hal_tmr_test.d \
	./Sources/Test/HAL/hal_tmr_test.o ./Sources/Test/HAL/hal_tmr_test.su \
	./Sources/Test/HAL/hal_wdg_test.cyclo ./Sources/Test/HAL/hal_wdg_test.d \
	./Sources/Test/HAL/hal_wdg_test.o ./Sources/Test/HAL/hal_wdg_test.su

.PHONY: clean-Sources-2f-Test-2f-HAL

