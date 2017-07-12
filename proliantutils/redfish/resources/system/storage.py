# Copyright 2017 Hewlett Packard Enterprise Development LP
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

import logging

from sushy.resources import base

LOG = logging.getLogger(__name__)


class HealthStatusField(base.CompositeField):
    health = base.Field('Health')
    state = base.Field('State')


class Storage(base.ResourceBase):

    identity = base.Field('Id', required=True)
    """The Storage identity string"""

    name = base.Field('Name')
    """The name of the resource or array element"""

    description = base.Field('Description')
    """Description"""

    storage_controllers = base.Field('StorageControllers')
    """The set of storage controllers"""

    drives = base.Field('Drives')
    """The set of drives attached to the storage controllers"""

    volumes = base.Field('Volumes')
    """The set of volumes produced by the storage controllers."""

    status = HealthStatusField('Status')

    def __init__(self, connector, identity, redfish_version=None):
        """A class representing a Storage

        :param connector: A Connector instance
        :param identity: The identity of the Storage resource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(Storage, self).__init__(connector, identity,
                                      redfish_version)


class StorageCollection(base.ResourceCollectionBase):

    @property
    def _resource_type(self):
        return Storage

    def __init__(self, connector, path, redfish_version=None):
        """A class representing a StorageCollection

        :param connector: A Connector instance
        :param path: The canonical path to the Storage
            collection resource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(StorageCollection, self).__init__(connector, path,
                                                redfish_version)
