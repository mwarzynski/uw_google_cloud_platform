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
import json

from dataclasses import dataclass, asdict
from google.cloud import pubsub_v1
from google.cloud import vision
import datastore

BUCKET_NAME = os.getenv('BUCKET_IMAGES_SCALED')

vision_client = vision.ImageAnnotatorClient()
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(os.getenv('PROJECT_ID'), os.getenv('TOPIC_NAME'))


@dataclass
class Event:
    success: bool
    image_id: str
    image_text: str
    blob_name: str
    email: str
    error: str


def gcf2(file_data, context):
    event = Event(True, "", "", "", "", "")
    try:
        event.blob_name = file_data['name']
        event.image_id = event.blob_name.split(".")[0]
        image_entity = datastore.get_image_by_id(event.image_id)
        event.email = image_entity.get("email")

        blob_uri = f'gs://{BUCKET_NAME}/{event.blob_name}'
        print(f'Analyzing {event.blob_name}, ID={event.image_id}')

        image = vision.types.Image()
        image.source.image_uri = blob_uri
        response = vision_client.text_detection(image=image)

        annotations = response.text_annotations
        if len(annotations) > 0:
            event.image_text = annotations[0].description
        datastore.update_image_text(image_entity, event.image_text)
    except Exception as e:
        event.success = False
        event.error = str(e)
        print(e)
    message = json.dumps(asdict(event))
    publisher.publish(topic_path, message.encode("utf-8"))
