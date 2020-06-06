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


import os
import tempfile

from google.cloud import storage
from wand.image import Image

storage_client = storage.Client()


def gcf1(data, _):
    file_name = data['name']
    bucket_name = data['bucket']
    return __scale_image(bucket_name, file_name)


def __scale_image(bucket_name: str, file_name: str):
    blob = storage_client.bucket(bucket_name).get_blob(file_name)
    file_name = blob.name
    _, temp_local_filename = tempfile.mkstemp()

    # Download file from bucket.
    blob.download_to_filename(temp_local_filename)
    print(f'Image {file_name} was downloaded to {temp_local_filename}.')

    # Scale the image using ImageMagick.
    with Image(filename=temp_local_filename) as image:
        image.transform(resize='640x480>')
        image.save(filename=temp_local_filename)
    print(f'Image {file_name} was resized.')

    # Upload result to a second bucket, to avoid re-triggering the function.
    scaled_bucket_name = os.getenv('BUCKET_IMAGES_SCALED')
    scaled_bucket = storage_client.bucket(scaled_bucket_name)
    new_blob = scaled_bucket.blob(file_name)
    new_blob.upload_from_filename(temp_local_filename)
    print(f'Scaled image uploaded to: gs://{scaled_bucket_name}/{file_name}')

    # Delete the temporary file.
    os.remove(temp_local_filename)
