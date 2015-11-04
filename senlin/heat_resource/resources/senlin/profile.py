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
from heat.common import template_format
from heat.engine import clients
from heat.engine import attributes
from heat.engine import properties
from heat.engine import resource
from heat.engine import support

from senlinclient.v1 import models


class SenlinProfile(resource.Resource):
    """Heat Template Resource for Monasca Notification.

    This plug-in requires python-monascaclient>=1.0.22. So to enable this
    plug-in, install this client library and restart the heat-engine.
    """

    support_status = support.SupportStatus(
        version='6.0.0')

    default_client_name = 'senlin'

    entity = 'profile'

    PROPERTIES = (
        NAME, SPEC, METADATA,
    ) = (
        'name', 'spec', 'metadata',
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
        SPEC: properties.Schema(
            properties.Schema.STRING,
            _('Type of the notification.'),
            required=True
        ),
        METADATA: properties.Schema(
            properties.Schema.MAP,
            _('Type of the notification.'),
            update_allowed=True,
            default={}
        )
    }

    attributes_schema = {
        ATTR_NAME: attributes.Schema(
            _("Cluster status."),
            type=attributes.Schema.STRING
        ),
        ATTR_TYPE: attributes.Schema(
            _("Cluster information."),
            type=attributes.Schema.STRING
        ),
        ATTR_METADATA: attributes.Schema(
            _("Cluster information."),
            type=attributes.Schema.MAP
        ),
        ATTR_ID: attributes.Schema(
            _("Cluster information."),
            type=attributes.Schema.STRING
        ),
        ATTR_SPEC: attributes.Schema(
            _("Cluster information."),
            type=attributes.Schema.MAP
        ),
    }

    def handle_create(self):
        spec = template_format.simple_parse(self.properties[self.SPEC])
        params = {
            'name': (self.properties[self.NAME] or
                     self.physical_resource_name()),
            'spec': spec,
            'metadata': self.properties[self.METADATA],
        }

        profile = self.client().create(models.Profile, params)
        self.resource_id_set(profile['id'])

    def handle_update(self, json_snippet=None,
                      tmpl_diff=None, prop_diff=None):
        if prop_diff:
            params = {
                'id': self.resource_id,
                'name': (prop_diff.get(self.NAME) or
                         self.properties[self.NAME] or
                         self.physical_resource_name()),
                'metadata': (prop_diff.get(self.METADATA) or
                             self.properties[self.METADATA])
            }
            self.client().update(models.Profile, params)

    def handle_delete(self):
        if self.resource_id is not None:
            params = {
                'id': self.resource_id
            }
            try:
                self.client().delete(models.Profile,
                                     params)
            except Exception as ex:
                self.client_plugin().ignore_not_found(ex)

    def _resolve_attribute(self, name):
        params = {
            'id': self.resource_id
        }
        profile = self.client().get(models.Profile, params)
        return getattr(profile, name, None)


def resource_mapping():
    return {
        'OS::Senlin::Profile': SenlinProfile
    }


def available_resource_mapping():
    if not clients.has_client(SenlinProfile.default_client_name):
        return {}

    return resource_mapping()
