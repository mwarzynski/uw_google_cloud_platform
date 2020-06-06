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
import uuid

from mock import MagicMock, patch

import main


@patch('main.tempfile')
@patch('main.os')
@patch('main.Image')
@patch('main.storage_client')
def test_scale_image(storage_client, image_mock, os_mock, tempfile_mock, capsys):
    bucket = 'images-bucket'
    filename = str(uuid.uuid4())
    scaled_bucket = 'images-scaled-bucket-' + str(uuid.uuid4())
    temp_file = "/tmp/file"

    tempfile_mock.mkstemp = MagicMock(return_value=(None, temp_file))
    os_mock.remove = MagicMock()
    os_mock.path = MagicMock()
    os_mock.path.basename = MagicMock(side_effect=(lambda x: x))

    os_mock.getenv = MagicMock(return_value=scaled_bucket)

    image_mock.return_value = image_mock
    image_mock.__enter__.return_value = image_mock

    data = {"bucket": bucket, "name": filename}

    blob = UserDict()
    blob.name = filename
    blob.bucket = UserDict()
    blob.download_to_filename = MagicMock()
    blob.upload_from_filename = MagicMock()

    bucket = UserDict()
    bucket.get_blob = MagicMock(return_value=blob)
    bucket.blob = MagicMock(return_value=blob)
    storage_client.bucket = MagicMock(return_value=bucket)

    main.gcf1(data, None)

    out, _ = capsys.readouterr()

    assert f'Image {filename} was downloaded to' in out
    assert f'Image {filename} was resized.' in out
    assert f'Scaled image uploaded to: gs://{scaled_bucket}/{filename}' in out
    assert os_mock.remove.called
    assert image_mock.transform.called
