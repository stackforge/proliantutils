# Copyright 2015 Hewlett-Packard Development Company, L.P.
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
"""Test Class for Common Operations."""

import unittest

from proliantutils.ilo import operations


class IloOperationsTestCase(unittest.TestCase):

    def setUp(self):
        super(IloOperationsTestCase, self).setUp()
        self.operations_object = operations.IloOperations()

    def test__okay(self):
        self.operations_object.host = '1.2.3.4'
        self.assertEqual('[iLO 1.2.3.4] foo',
                         self.operations_object._('foo'))

    def test__no_host(self):
        self.assertEqual('foo',
                         self.operations_object._('foo'))
