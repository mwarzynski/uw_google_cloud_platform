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
import datetime

from google.cloud import storage
import sendgrid

bucket_images = os.getenv("BUCKET_IMAGES")
bucket_images_scaled = os.getenv("BUCKET_IMAGES_SCALED")

sendgrid_api_key = os.getenv("SENDGRID_API_KEY")
sg = sendgrid.SendGridAPIClient(api_key=sendgrid_api_key)

storage_client = storage.Client()


def generate_download_signed_url_v4(bucket_name, blob_name):
    """Generates a v4 signed URL for downloading a blob.

    Note that this method requires a service account key file. You can not use
    this if you are using Application Default Credentials from Google Compute
    Engine or from the Google Cloud SDK.
    """

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    url = blob.generate_signed_url(
        version="v4",
        expiration=datetime.timedelta(minutes=15),
        method="GET",
    )
    return url


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
        event_raw_data = base64.b64decode(event['data']).decode('utf-8')
        event = json.loads(event_raw_data)

        blob_name = event['blob_name']

        # image_original = generate_download_signed_url_v4(bucket_images, blob_name)
        # image_transformed = generate_download_signed_url_v4(bucket_images_scaled, blob_name)
        image_original = blob_name
        image_transformed = blob_name
        image_text = event['image_text']

        message = sendgrid.Mail(
            from_email="noreply@mimuwgcpproject.pl",
            to_emails=event['email'],
            subject="Image has been processed!",
            html_content=f"Image original: {image_original}\nImage transformed: {image_transformed}\n\n{image_text}"
        )
        sg.send(message)
    except Exception as e:
        print(e)
