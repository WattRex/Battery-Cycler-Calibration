################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (10.3-2021.10)
################################################################################

-include ../makefile.init

RM := rm -rf

# All of the sources participating in the build are defined here
-include sources.mk
-include Sources/Test/MID/subdir.mk
-include Sources/Test/HAL/subdir.mk
-include Sources/Test/subdir.mk
-include Sources/MID/MID_REG/subdir.mk
-include Sources/MID/MID_PWR/subdir.mk
-include Sources/MID/MID_DABS/subdir.mk
-include Sources/MID/MID_COMM/subdir.mk
-include Sources/HAL/HAL_WDG/subdir.mk
-include Sources/HAL/HAL_TMR/subdir.mk
-include Sources/HAL/HAL_SYS/subdir.mk
-include Sources/HAL/HAL_STS/subdir.mk
-include Sources/HAL/HAL_PWM/subdir.mk
-include Sources/HAL/HAL_GPIO/subdir.mk
-include Sources/HAL/HAL_CAN/subdir.mk
-include Sources/HAL/HAL_ADC/subdir.mk
-include Sources/EPC_ST/subdir.mk
-include Sources/EPC_CONF/subdir.mk
-include Sources/APP/APP_SALG/subdir.mk
-include Sources/APP/APP_IFACE/subdir.mk
-include Drivers/STM32F3xx_HAL_Driver/Src/subdir.mk
-include Core/Startup/subdir.mk
-include Core/Src/subdir.mk
-include objects.mk

ifneq ($(MAKECMDGOALS),clean)
ifneq ($(strip $(S_DEPS)),)
-include $(S_DEPS)
endif
ifneq ($(strip $(S_UPPER_DEPS)),)
-include $(S_UPPER_DEPS)
endif
ifneq ($(strip $(C_DEPS)),)
-include $(C_DEPS)
endif
endif

-include ../makefile.defs

OPTIONAL_TOOL_DEPS := \
$(wildcard ../makefile.defs) \
$(wildcard ../makefile.init) \
$(wildcard ../makefile.targets) \


BUILD_ARTIFACT_NAME := STM32
BUILD_ARTIFACT_EXTENSION := elf
BUILD_ARTIFACT_PREFIX :=
BUILD_ARTIFACT := $(BUILD_ARTIFACT_PREFIX)$(BUILD_ARTIFACT_NAME)$(if $(BUILD_ARTIFACT_EXTENSION),.$(BUILD_ARTIFACT_EXTENSION),)

# Add inputs and outputs from these tool invocations to the build variables 
EXECUTABLES += \
STM32.elf \

MAP_FILES += \
STM32.map \

SIZE_OUTPUT += \
default.size.stdout \

OBJDUMP_LIST += \
STM32.list \


# All Target
all: main-build
	@echo 'Build complete.'
	@echo $(SOURCE_PATH)

# Main-build Target
<<<<<<< Updated upstream
main-build: STM32.elf secondary-outputs
=======
main-build: STM32.elf secondary-outputs STM32.bin

STM32.bin: STM32.elf
	@echo 'Invoking: GNU Objcopy Utility'
	arm-none-eabi-objcopy -O binary STM32.elf STM32.bin
	@echo 'Generating binary: $@'
	@echo ' '
>>>>>>> Stashed changes

# Tool invocations
STM32.elf STM32.map: $(OBJS) $(USER_OBJS) $(SOURCE_PATH)/STM32/STM32F334R8TX_FLASH.ld makefile objects.list $(OPTIONAL_TOOL_DEPS)
	
	arm-none-eabi-gcc -o "STM32.elf" @"objects.list" $(USER_OBJS) $(LIBS) -mcpu=cortex-m4 \
	-T"$(SOURCE_PATH)/STM32/STM32F334R8TX_FLASH.ld" --specs=nosys.specs \
	-Wl,-Map="STM32.map" -Wl,--gc-sections -static --specs=nano.specs \
	-mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -Wl,--start-group -lc -lm -Wl,--end-group
	@echo 'Finished building target: $@'
<<<<<<< Updated upstream
	arm-none-eabi-objcopy -O binary STM32.elf STM32.bin
	@echo 'Generating binary'
	@echo ' '
=======
>>>>>>> Stashed changes

default.size.stdout: $(EXECUTABLES) makefile objects.list $(OPTIONAL_TOOL_DEPS)
	arm-none-eabi-size  $(EXECUTABLES)
	@echo 'Finished building: $@'
	@echo ' '

STM32.list: $(EXECUTABLES) makefile objects.list $(OPTIONAL_TOOL_DEPS)
	arm-none-eabi-objdump -h -S $(EXECUTABLES) > "STM32.list"
	@echo 'Finished building: $@'
	@echo ' '

# Other Targets
clean:
	-$(RM) STM32.elf STM32.list STM32.map default.size.stdout STM32.bin
	-@echo ' '

secondary-outputs: $(SIZE_OUTPUT) $(OBJDUMP_LIST)

fail-specified-linker-script-missing:
	@echo 'Error: Cannot find the specified linker script. Check the linker settings in the build configuration.'
	@exit 2

warn-no-linker-script-specified:
	@echo 'Warning: No linker script specified. Check the linker settings in the build configuration.'

.PHONY: all clean dependents main-build fail-specified-linker-script-missing warn-no-linker-script-specified

-include ../makefile.targets
