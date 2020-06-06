# Copyright 2019 Google LLC
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

from __future__ import absolute_import

import os

from flask import current_app
from google.cloud import storage
import six


def upload_file(file_stream, filename, content_type):
    """
    Uploads a file to a given Cloud Storage bucket and returns the public url
    to the new object.
    """
    bucketname = os.getenv('GOOGLE_STORAGE_BUCKET')

    # [START bookshelf_cloud_storage_client]
    client = storage.Client()
    bucket = client.bucket(bucketname)
    blob = bucket.blob(filename)

    blob.upload_from_string(
        file_stream,
        content_type=content_type)

    url = blob.public_url
    # [END bookshelf_cloud_storage_client]

    if isinstance(url, six.binary_type):
        url = url.decode('utf-8')

    return url
