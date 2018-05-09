#!/bin/bash

# Enables the PWM ports of the BeableBone.

echo cape-universaln > /sys/devices/bone_capemgr.*/slots
config-pin P8.19 pwm
config-pin P8.13 pwm
config-pin P9.16 pwm
config-pin P9.14 pwm
