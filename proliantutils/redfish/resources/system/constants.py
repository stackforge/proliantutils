# Copyright 2017 Hewlett Packard Enterprise Development LP
#
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

# Push power button action constants

PUSH_POWER_BUTTON_PRESS = 'press'
PUSH_POWER_BUTTON_PRESS_AND_HOLD = 'press and hold'

# BIOS Settings boot mode constants

BIOS_BOOT_MODE_LEGACY_BIOS = 'legacy bios'
BIOS_BOOT_MODE_UEFI = 'uefi'

# Persistent boot device for set

BOOT_SOURCE_TARGET_CD = 'Cd'
BOOT_SOURCE_TARGET_PXE = 'Pxe'
BOOT_SOURCE_TARGET_UEFI_TARGET = 'UefiTarget'
BOOT_SOURCE_TARGET_HDD = 'Hdd'

# System supported boot mode contants

SYSTEM_LEGACY_BIOS_ONLY = 0
SYSTEM_UEFI_ONLY = 3
SYSTEM_BIOS_AND_UEFI = 2
