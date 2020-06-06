# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import base64
import json
import os

import sendgrid

sg = sendgrid.SendGridAPIClient(api_key=os.getenv("SENDGRID_API_KEY"))


def gcf3(event, _):
    event_raw_data = base64.b64decode(event['data']).decode('utf-8')
    event = json.loads(event_raw_data)
    sg.send(sendgrid.Mail(
        from_email=event["sender"],
        to_emails=event["recipient"],
        subject=event["title"],
        html_content=event["html_content"]
    ))
