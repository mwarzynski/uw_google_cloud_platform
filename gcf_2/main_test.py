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

from collections import UserDict
from mock import MagicMock, patch

import main


@patch('main.publisher')
@patch('main.vision_client')
@patch('main.datastore')
def test_image_processed_with_text(
    datastore,
    vision_client,
    publisher):
  # Define basic information which is provided as arguments.
  image_id = "123456789"
  image_name = f"{image_id}.jpg"
  # Define response from the Visual API client.
  visual_text_annotation = UserDict()
  visual_text_annotation.description = "Text visible in the image."
  visual_text_detection_response = UserDict()
  visual_text_detection_response.text_annotations = [visual_text_annotation]
  vision_client.text_detection = MagicMock(return_value=visual_text_detection_response)
  # Define Datastore implementation.
  datastore.get_image_by_id = MagicMock(return_value={"email": "tester@google.com", "filename": image_name})
  datastore.update_image_text = MagicMock()
  # Define Pub/Sub implementation.
  publisher.publish = MagicMock()

  main.gcf2({"name": image_name}, None)

  assert vision_client.text_detection.called is True
  assert datastore.update_image_text.called is True
  assert publisher.publish.called is True
  publish_args = publisher.publish.call_args.args
  assert publish_args[1] == b'{"recipient": "tester@google.com", "sender": "noreply@gcplecturesproject.com", "title": "123456789.jpg has been processed!", "html_content": "Image original: 123456789.jpg<br/>Image transformed: 123456789.jpg<br/><br/>Text visible in the image."}'


@patch('main.publisher')
@patch('main.vision_client')
@patch('main.datastore')
def test_image_processed_with_no_text(
    datastore,
    vision_client,
    publisher,
    capsys):
  # Define basic information which is provided as arguments.
  image_id = "123456789"
  image_name = f"{image_id}.jpg"
  # Define response from the Visual API client.
  visual_text_detection_response = UserDict()
  visual_text_detection_response.text_annotations = []
  vision_client.text_detection = MagicMock(return_value=visual_text_detection_response)
  # Define Datastore implementation.
  datastore.get_image_by_id = MagicMock()
  datastore.update_image_text = MagicMock()
  # Define Pub/Sub implementation.
  publisher.publish = MagicMock()

  main.gcf2({"name": image_name}, None)

  assert vision_client.text_detection.called is True
  assert datastore.update_image_text.called is False
  assert publisher.publish.called is False
  out, _ = capsys.readouterr()
  assert 'No annotations received from Visual API' in out
