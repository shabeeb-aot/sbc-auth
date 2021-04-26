# Copyright © 2019 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests to verify the Activity Log API end-point.

Test-Suite to ensure that the /Activity Log endpoint is working as expected.
"""

from auth_api import status as http_status
from auth_api.schemas import utils as schema_utils
from auth_api.utils.enums import ActivityAction
from tests.utilities.factory_scenarios import TestJwtClaims
from tests.utilities.factory_utils import (factory_auth_header,
                                           factory_user_model, factory_activity_log_model, factory_org_model)


def test_fetch_log_no_content_no_org(client, jwt, session):  # pylint:disable=unused-argument
    """Assert that the none can be fetched."""
    headers = factory_auth_header(jwt=jwt, claims=TestJwtClaims.staff_role)
    rv = client.get('/api/v1/orgs/1/activity-logs', headers=headers, content_type='application/json')
    assert rv.status_code == http_status.HTTP_200_OK


def test_fetch_activity_log(client, jwt, session):  # pylint:disable=unused-argument
    """Assert that the activity log can be fetched."""
    user = factory_user_model()
    org = factory_org_model()

    factory_activity_log_model(
        actor=user.id,
        action=ActivityAction.GENERATED_PASSCODE.value
    )
    factory_activity_log_model(
        actor=user.id,
        action=ActivityAction.CREATE_AFFILIATION.value,
        org_id=org.id
    )
    factory_activity_log_model(
        actor=user.id,
        action=ActivityAction.REMOVE_AFFILIATION.value,
        org_id=org.id
    )

    headers = factory_auth_header(jwt=jwt, claims=TestJwtClaims.staff_role)
    rv = client.get(f'/api/v1/orgs/{org.id}/activity-logs',
                    headers=headers, content_type='application/json')
    activity_logs = rv.json
    assert len(activity_logs.get('activityLogs')) == 2
    assert schema_utils.validate(activity_logs, 'paged_response')[0]
    assert rv.status_code == http_status.HTTP_200_OK

    rv = client.get(f'/api/v1/orgs/{org.id}/activity-logs?action={ActivityAction.REMOVE_AFFILIATION.value}',
                    headers=headers, content_type='application/json')
    assert len(rv.json.get('activityLogs')) == 1