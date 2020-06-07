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

import traceback
from dataclasses import dataclass, asdict
from google.cloud import pubsub_v1
from google.cloud import vision
import datastore
import storage

BUCKET_NAME = os.getenv('BUCKET_IMAGES_SCALED')

vision_client = vision.ImageAnnotatorClient()
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(os.getenv('PROJECT_ID'), os.getenv('TOPIC_NAME'))


@dataclass
class Message:
    recipient: str
    sender: str
    title: str
    html_content: str


def gcf2(file_data, _):
    try:
        # Evaluate the URI of the blob.
        blob_name = file_data['name']
        blob_uri = f'gs://{BUCKET_NAME}/{blob_name}'

        # Use Visual API to get the Image Text.
        image = vision.types.Image()
        image.source.image_uri = blob_uri
        response = vision_client.text_detection(image=image)
        annotations = response.text_annotations
        if len(annotations) == 0:
            # If there is no text from Visual API, abort.
            print(f"Text from '{blob_uri}' could not be evaluated. No annotations received from Visual API.")
            return
        image_text = annotations[0].description

        # Update image_text in Datastore.
        # Also, fetch the email for the recipient.
        image_id = blob_name.split(".")[0]
        with datastore.transaction():
            image_entity = datastore.get_image_by_id(image_id)
            datastore.update_image_text(image_entity, image_text)

        # Sign URLs to Cloud Storage.
        uri_image, uri_image_transformed = storage.generate_signed_urls(blob_name)

        # Send message to topic.
        message = _prepare_message(
            image_entity.get("email"),
            image_entity.get("filename"),
            uri_image,
            uri_image_transformed,
            image_text
        )
        message = json.dumps(asdict(message))
        publisher.publish(topic_path, message.encode("utf-8"))
    except Exception as e:
        print(e)
        traceback.print_exc()


def _prepare_message(recipient: str, filename: str, image_original: str, image_transformed: str, image_text: str) -> Message:
    html_content = f"Image original: {image_original}<br/>Image transformed: {image_transformed}<br/><br/>{image_text}"
    return Message(
        recipient,
        "noreply@gcplecturesproject.com",
        f"{filename} has been processed!",
        html_content
    )
