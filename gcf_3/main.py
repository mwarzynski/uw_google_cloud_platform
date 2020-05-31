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
import base64

from google.cloud import vision

BUCKET_NAME = os.getenv('BUCKET_IMAGES_SCALED')

vision_client = vision.ImageAnnotatorClient()


def gcf3(event, context):
    """Background Cloud Function to be triggered by Pub/Sub.
    Args:
         event (dict):  The dictionary with data specific to this type of
         event. The `data` field contains the PubsubMessage message. The
         `attributes` field will contain custom attributes if there are any.
         context (google.cloud.functions.Context): The Cloud Functions event
         metadata. The `event_id` field contains the Pub/Sub message ID. The
         `timestamp` field contains the publish time.
    """
    try:
        file_name = base64.b64decode(event['data']).decode('utf-8')

        blob_uri = f'gs://{BUCKET_NAME}/{file_name}'
        print(f'Analyzing {file_name}.')
        image = vision.types.Image()
        image.source.image_uri = blob_uri
        response = vision_client.text_detection(image=image)

        texts = response.text_annotations
        for text in texts:
            vertices = ','.join([f"({v.x},{v.y})" for v in text.bounding_poly.vertices])
            print(f"description={text.description}, bounds={vertices}")
        if response.error.message:
            raise Exception(f"{response.error.message}; https://cloud.google.com/apis/design/errors")
    except Exception as e:
        print(e)
