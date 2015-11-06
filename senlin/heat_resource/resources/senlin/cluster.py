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

from heat.common import exception
from heat.common.i18n import _
from heat.engine import clients
from heat.engine import constraints
from heat.engine import properties
from heat.engine import resource
from heat.engine import support

from senlinclient.v1 import models


class SenlinCluster(resource.Resource):
    """Heat Template Resource for Monasca Notification.

    This plug-in requires python-monascaclient>=1.0.22. So to enable this
    plug-in, install this client library and restart the heat-engine.
    """

    support_status = support.SupportStatus(
        version='6.0.0')

    default_client_name = 'senlin'

    entity = 'cluster'

    PROPERTIES = (
        NAME, PROFILE, DESIRED_CAPACITY, MIN_SIZE, MAX_SIZE,
        METADATA, TIMEOUT
    ) = (
        'name', 'profile', 'desired_capacity', 'min_size',
        'max_size', 'metadata', 'timeout'
    )

    ATTRIBUTES = (
        ATTR_NAME, ATTR_TYPE, ATTR_METADATA, ATTR_ID, ATTR_SPEC,
    ) = (
        "name", "type", 'metadata', 'id', 'spec',
    )

    properties_schema = {
        NAME: properties.Schema(
            properties.Schema.STRING,
            _('Name of the notification. By default, physical resource name '
              'is used.'),
            update_allowed=True
        ),
        PROFILE: properties.Schema(
            properties.Schema.STRING,
            _('Type of the notification.'),
            required=True,
            update_allowed=True,
            constraints=[
                constraints.CustomConstraint('senlin.profile')
            ]
        ),
        DESIRED_CAPACITY: properties.Schema(
            properties.Schema.INTEGER,
            _('Type of the notification.'),
            update_allowed=True,
            default=0
        ),
        MIN_SIZE: properties.Schema(
            properties.Schema.INTEGER,
            _('Type of the notification.'),
            update_allowed=True,
            default=0,
            constraints=[
                constraints.Range(min=0)
            ]
        ),
        MAX_SIZE: properties.Schema(
            properties.Schema.INTEGER,
            _('Type of the notification.'),
            update_allowed=True,
            default=-1,
            constraints=[
                constraints.Range(min=-1)
            ]
        ),
        METADATA: properties.Schema(
            properties.Schema.MAP,
            _('Type of the notification.'),
            update_allowed=True,
            default={}
        ),
        TIMEOUT: properties.Schema(
            properties.Schema.INTEGER,
            _('Type of the notification.'),
            update_allowed=True,
            # default=3600
        ),
    }

    def _get_cluster_status(self, cluster_id):
        params = {
            'id': cluster_id
        }
        cluster = self.client().get(models.Cluster, params)
        return cluster['status']

    def handle_create(self):
        params = {
            'name': (self.properties[self.NAME] or
                     self.physical_resource_name()),
            'profile_id': self.properties[self.PROFILE],
            'desired_capacity': self.properties[self.DESIRED_CAPACITY],
            'min_size': self.properties[self.MIN_SIZE],
            'max_size': self.properties[self.MAX_SIZE],
            'metadata': self.properties[self.METADATA],
            'timeout': self.properties[self.TIMEOUT]
        }
        cluster = self.client().create(models.Cluster, params)
        self.resource_id_set(cluster['id'])
        return cluster['id']

    def check_create_complete(self, resource_id):
        status = self._get_cluster_status(resource_id)
        if status == 'ACTIVE':
            return True
        return False

    def handle_delete(self):
        if self.resource_id is not None:
            params = {
                'id': self.resource_id
            }
            try:
                self.client().delete(models.Cluster, params)
            except Exception as ex:
                self.client_plugin().ignore_not_found(ex)

        return self.resource_id

    def handle_update(self, json_snippet=None,
                      tmpl_diff=None, prop_diff=None):
        if prop_diff:
            if any(p in prop_diff for p in [self.NAME, self.PROFILE,
                                            self.METADATA, self.TIMEOUT]):
                params = {
                    'id': self.resource_id,
                    'name': (prop_diff.get(self.NAME) or
                             self.properties[self.NAME] or
                             self.physical_resource_name()),
                    'profile_id': (prop_diff.get(self.PROFILE) or
                                   self.properties[self.PROFILE]),
                    'metadata': (prop_diff.get(self.METADATA) or
                                 self.properties[self.METADATA]),
                    'timeout': (prop_diff.get(self.TIMEOUT) or
                                self.properties[self.TIMEOUT])
                }
                self.client().update(models.Cluster, params)
            if any(p in prop_diff for p in [self.DESIRED_CAPACITY,
                                            self.MIN_SIZE, self.MAX_SIZE]):
                action_args = {
                    'min_size': (prop_diff.get(self.MIN_SIZE) or
                                 self.properties[self.MIN_SIZE]),
                    'max_size': (prop_diff.get(self.MAX_SIZE) or
                                 self.properties[self.MAX_SIZE]),
                    'adjustment_type': 'EXACT_CAPACITY',
                    'number': (prop_diff.get(self.DISIRED_CAPACITY) or
                               self.properties[self.DISIRED_CAPACITY]),
                }
                params = {
                    'id': self.resource_id,
                    'action': 'resize',
                    'action_args': action_args
                }
                self.client().action(models.Cluster, params)

    def check_update_complete(self, resource_id):
        status = self._get_cluster_status(resource_id)
        if status == 'ACTIVE':
            return True
        return False

    def check_delete_complete(self, resource_id):
        if not resource_id:
            return True

        params = {
            'id': resource_id
        }
        try:
            self.client().get(models.Cluster, params)
        except Exception as ex:
            self.client_plugin().ignore_not_found(ex)
            return True

        return False

    def validate(self):
        # check validity of group size
        min_size = self.properties[self.MIN_SIZE]
        max_size = self.properties[self.MAX_SIZE]

        if max_size < min_size:
            msg = _("MinSize can not be greater than MaxSize")
            raise exception.StackValidationFailed(message=msg)

        if self.properties[self.DESIRED_CAPACITY] is not None:
            desired_capacity = self.properties[self.DESIRED_CAPACITY]
            if desired_capacity < min_size or desired_capacity > max_size:
                msg = _("DesiredCapacity must be between MinSize and MaxSize")
                raise exception.StackValidationFailed(message=msg)


def resource_mapping():
    return {
        'OS::Senlin::Cluster': SenlinCluster
    }


def available_resource_mapping():
    if not clients.has_client(SenlinCluster.default_client_name):
        return {}

    return resource_mapping()
