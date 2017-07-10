# Copyright 2017 Hewlett Packard Enterprise Development LP
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

import json

import mock
import testtools

from proliantutils import exception
from proliantutils.redfish.resources.system import pcidevice


class HPEPCIDeviceTestCase(testtools.TestCase):

    def setUp(self):
        super(HPEPCIDeviceTestCase, self).setUp()
        self.conn = mock.Mock()
        pci_file = 'proliantutils/tests/redfish/json_samples/pci_device.json'
        with open(pci_file, 'r') as f:
            pci_json = json.loads(f.read()
        self.conn.get.return_value.json.return_value = pci_json['pci_device1']

        pci_path = "/redfish/v1/Systems/1/PCIDevices/1"
        self.sys_pci = pcidevice.PciDevice(
            self.conn, pci_path, redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.sys_eth._parse_attributes()
        self.assertEqual('1.0.2', self.sys_pci.redfish_version)
        self.assertEqual('1', self.sys_pci.identity)
        self.assertEqual('Network Controller', self.sys_pci.name)


class PciDeviceCollectionTestCase(base.TestCase):

    def setUp(self):
        super(PciDeviceCollectionTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('sushy/tests/unit/json_samples/'
                  'pci_device_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        self.sys_pci_col = pcidevice.PciDeviceCollection(
            self.conn, '/redfish/v1/Systems/1/PCIDevices',
            redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.sys_pci_col._parse_attributes()
        self.assertEqual('1.0.2', self.sys_pci_col.redfish_version)
        self.assertEqual('PciDevices', self.sys_pci_col.name)
        pci_path = '/redfish/v1/Systems/1/PCIDevices/1'
        self.assertEqual(pci_path, self.sys_pci_col.members_identities)

    @mock.patch.object(pcidevice, 'PciDevice', autospec=True)
    def test_get_member(self, mock_pci):
        self.sys_eth_col.get_member(
            '/redfish/v1/Systems/1/PCIDevices/1')
        mock_pci.assert_called_once_with(
            self.sys_pci_col._conn,
            ('/redfish/v1/Systems/1/PCIDevices/1'),
            redfish_version=self.sys_pci_col.redfish_version)

    @mock.patch.object(pcidevice, 'PciDevice', autospec=True)
    def test_get_members(self, mock_pci):
        members = self.sys_pci_col.get_members()
        path_list = ["/redfish/v1/Systems/1/PCIDevices/1",
                     "/redfish/v1/Systems/1/PCIDevices/2",
                     "/redfish/v1/Systems/1/PCIDevices/6"]
        calls = [
            mock.call(self.sys_pci_col._conn, path_list[1],
                      redfish_version=self.sys_pci_col.redfish_version),
        ]
        mock_pci.assert_has_calls(calls)
        self.assertIsInstance(members, list)
        self.assertEqual(3, len(members))
