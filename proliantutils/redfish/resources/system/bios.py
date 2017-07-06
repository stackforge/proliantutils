# Copyright 2017 Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import sushy
from sushy.resources import base

from proliantutils import exception
from proliantutils import log
from proliantutils.redfish.resources.system import mappings
from proliantutils.redfish import utils

LOG = log.get_logger(__name__)

BOOT_SOURCE_TARGET_TO_PARTIAL_STRING_MAP = {
    sushy.BOOT_SOURCE_TARGET_CD: ('HPE Virtual CD-ROM',),
    sushy.BOOT_SOURCE_TARGET_PXE: ('NIC', 'PXE'),
    sushy.BOOT_SOURCE_TARGET_UEFI_TARGET: ('ISCSI',),
    sushy.BOOT_SOURCE_TARGET_HDD: ('Logical Drive', 'HDD', 'Storage', 'LogVol')
}


class BIOSSettings(base.ResourceBase):

    boot_mode = base.MappedField(["Attributes", "BootMode"],
                                 mappings.GET_BIOS_BOOT_MODE_MAP)
    _pending_settings = None
    _boot_settings = None

    @property
    def pending_settings(self):
        """Property to provide reference to bios_pending_settings instance

        It is calculated once when the first time it is queried. On refresh,
        this property gets reset.
        """
        if self._pending_settings is None:
            self._pending_settings = BIOSPendingSettings(
                self._conn, utils.get_subresource_path_by(
                    self, ["@Redfish.Settings", "SettingsObject"]))

        return self._pending_settings

    @property
    def boot_settings(self):
        """Property to provide reference to bios boot instance

        It is calculated once when the first time it is queried. On refresh,
        this property gets reset.
        """
        if self._boot_settings is None:
            self._boot_settings = BIOSBootSettings(
                self._conn,
                utils.get_subresource_path_by(
                    self, ["Oem", "Hpe", "Links", "Boot"]))

        return self._boot_settings


class BIOSPendingSettings(base.ResourceBase):

    boot_mode = base.MappedField(["Attributes", "BootMode"],
                                 mappings.GET_BIOS_BOOT_MODE_MAP)


class BIOSBootSettings(base.ResourceBase):

    boot_sources = base.Field("BootSources", adapter=list)
    persistent_boot_config_order = base.Field("PersistentBootConfigOrder",
                                              adapter=list)

    def get_persistent_boot_device(self):
        """Get current persistent boot device set for the host

        :returns: persistent boot device for the system
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        boot_string = None
        preferred_boot_device = self.persistent_boot_config_order[0]
        try:
            for boot_source in self.boot_sources:
                if (preferred_boot_device ==
                        boot_source["StructuredBootString"]):
                    boot_string = boot_source["BootString"]
                    break
        except KeyError as e:
            msg = ('Get persistent boot device failed with key error. '
                   'Error %(error)s') % {'error': str(e)}
            LOG.debug(msg)
            raise exception.IloCommandNotSupportedError(msg)

        is_present_in_boot_string = (
            lambda match_sub_strings: any(
                [sub_string in boot_string
                 for sub_string in match_sub_strings]))

        for key, value in BOOT_SOURCE_TARGET_TO_PARTIAL_STRING_MAP.items():
            if is_present_in_boot_string(value):
                return key
        return sushy.BOOT_SOURCE_TARGET_NONE
