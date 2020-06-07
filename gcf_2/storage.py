from google.cloud import storage
import datetime
import os

bucket_images = os.getenv("BUCKET_IMAGES")
bucket_images_scaled = os.getenv("BUCKET_IMAGES_SCALED")


storage_client = storage.Client()


def generate_signed_urls(blob_name: str) -> (str, str):
  image = generate_download_signed_url_v4(bucket_images, blob_name)
  image_scaled = generate_download_signed_url_v4(bucket_images_scaled, blob_name)
  return image, image_scaled


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
        expiration=datetime.timedelta(hours=1),
        method="GET",
    )
    return url
