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

from heat.common.i18n import _
from heat.engine import clients
from heat.engine import constraints
from heat.engine import properties
from heat.engine import resource
from heat.engine import support

from senlinclient.v1 import models

template_template = {
    "heat_template_version": "2015-04-30",
    "resources": {}
}

class ResourceGroup(resource.Resource):
    """Heat Template Resource for Monasca Notification.

    This plug-in requires python-monascaclient>=1.0.22. So to enable this
    plug-in, install this client library and restart the heat-engine.
    """

    support_status = support.SupportStatus(
        version='6.0.0',
        status=support.UNSUPPORTED)

    default_client_name = 'senlin'

    PROPERTIES = (
        COUNT, INDEX_VAR, RESOURCE_DEF, REMOVAL_POLICIES,
    ) = (
        'count', 'index_var', 'resource_def', 'removal_policies',
    )

    _RESOURCE_DEF_KEYS = (
        RESOURCE_DEF_TYPE, RESOURCE_DEF_PROPERTIES, RESOURCE_DEF_METADATA,
    ) = (
        'type', 'properties', 'metadata',
    )

    _REMOVAL_POLICIES_KEYS = (
        REMOVAL_RSRC_LIST,
    ) = (
        'resource_list',
    )

    _ROLLING_UPDATES_SCHEMA_KEYS = (
        MIN_IN_SERVICE, MAX_BATCH_SIZE, PAUSE_TIME,
    ) = (
        'min_in_service', 'max_batch_size', 'pause_time',
    )

    _BATCH_CREATE_SCHEMA_KEYS = (
        MAX_BATCH_SIZE, PAUSE_TIME,
    ) = (
        'max_batch_size', 'pause_time',
    )

    _UPDATE_POLICY_SCHEMA_KEYS = (
        ROLLING_UPDATE, BATCH_CREATE,
    ) = (
        'rolling_update', 'batch_create',
    )

    ATTRIBUTES = (
        REFS, ATTR_ATTRIBUTES,
    ) = (
        'refs', 'attributes',
    )

    properties_schema = {
        COUNT: properties.Schema(
            properties.Schema.INTEGER,
            _('The number of resources to create.'),
            default=1,
            constraints=[
                constraints.Range(min=0),
            ],
            update_allowed=True
        ),
        INDEX_VAR: properties.Schema(
            properties.Schema.STRING,
            _('A variable that this resource will use to replace with the '
              'current index of a given resource in the group. Can be used, '
              'for example, to customize the name property of grouped '
              'servers in order to differentiate them when listed with '
              'nova client.'),
            default="%index%",
            constraints=[
                constraints.Length(min=3)
            ],
            support_status=support.SupportStatus(version='2014.2')
        ),
        RESOURCE_DEF: properties.Schema(
            properties.Schema.MAP,
            _('Resource definition for the resources in the group. The value '
              'of this property is the definition of a resource just as if '
              'it had been declared in the template itself.'),
            schema={
                RESOURCE_DEF_TYPE: properties.Schema(
                    properties.Schema.STRING,
                    _('The type of the resources in the group'),
                    required=True
                ),
                RESOURCE_DEF_PROPERTIES: properties.Schema(
                    properties.Schema.MAP,
                    _('Property values for the resources in the group')
                ),
                RESOURCE_DEF_METADATA: properties.Schema(
                    properties.Schema.MAP,
                    _('Supplied metadata for the resources in the group'),
                    support_status=support.SupportStatus(version='5.0.0')
                ),

            },
            required=True,
            update_allowed=True
        ),
        REMOVAL_POLICIES: properties.Schema(
            properties.Schema.LIST,
            _('Policies for removal of resources on update'),
            schema=properties.Schema(
                properties.Schema.MAP,
                _('Policy to be processed when doing an update which '
                  'requires removal of specific resources.'),
                schema={
                    REMOVAL_RSRC_LIST: properties.Schema(
                        properties.Schema.LIST,
                        _("List of resources to be removed "
                          "when doing an update which requires removal of "
                          "specific resources. "
                          "The resource may be specified several ways: "
                          "(1) The resource name, as in the nested stack, "
                          "(2) The resource reference returned from "
                          "get_resource in a template, as available via "
                          "the 'refs' attribute "
                          "Note this is destructive on update when specified; "
                          "even if the count is not being reduced, and once "
                          "a resource name is removed, it's name is never "
                          "reused in subsequent updates"
                          ),
                        default=[]
                    ),
                },
            ),
            update_allowed=True,
            default=[],
            support_status=support.SupportStatus(version='2015.1')
        ),
    }

    def handle_create(self):
        profile_id = '111'
        params = {
            'name': self.physical_resource_name(),
            'profile_id': profile_id,
            'desired_capacity': self.properties[self.COUNT],
            'min_size': 0,
            'max_size': -1,
            'metadata': self.properties[self.METADATA],
        }

        cluster = self.client().create(models.Cluster, params)
        self.resource_id_set(cluster['id'])

    def handle_delete(self):
        if self.resource_id is not None:
            params = {
                'id': self.resource_id
            }
            try:
                cluster = self.client().delete(models.Cluster, params)
            except Exception as ex:
                self.client_plugin().ignore_not_found(ex)

        return self.resource_id

    def check_delete_complete(self, resource_id):
        if not resource_id:
            return True

        params = {
            'id': resource_id
        }
        try:
            cluster = self.client().get(models.Cluster, params)
        except Exception as ex:
            self.client_plugin().ignore_not_found(ex)
            return True

        return False


def resource_mapping():
    return {
        'OS::Senlin::ResourceGroup': ResourceGroup
    }


def available_resource_mapping():
    if not clients.has_client(ResourceGroup.default_client_name):
        return {}

    return resource_mapping()
