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

from mock import MagicMock, patch

import base64
import main

event_bytes = b'''
{
  "recipient": "tester@google.com",
  "sender": "noreply@gcplecturesproject.com",
  "title": "Extraordinary title!",
  "html_content": "MESSAGE AS HTML"
}
'''


@patch('main.sg')
def test_mail_sent_properly(
    sendgrid):
  # Define input data.
  event = base64.b64encode(event_bytes)
  # Define mail sender implementation.
  sendgrid.send = MagicMock()

  main.gcf3({"data": event}, None)

  assert sendgrid.send.called is True
  args = sendgrid.send.call_args.args[0]
  assert args.from_email.email == "noreply@gcplecturesproject.com"
  assert args.personalizations[0].tos[0]['email'] == "tester@google.com"
  assert args.subject.subject == 'Extraordinary title!'
  assert args.contents[0].content == 'MESSAGE AS HTML'
