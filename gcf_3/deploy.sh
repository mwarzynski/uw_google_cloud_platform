#!/bin/bash

gcloud functions deploy gcf3 \
    --trigger-topic=$TOPIC_IMAGE_WAS_SCALED \
    --set-env-vars \
      BUCKET_IMAGES=$BUCKET_IMAGES,BUCKET_IMAGES_SCALED=$BUCKET_IMAGES_SCALED,SENDGRID_API_KEY=$SENDGRID_API_KEY \
    --runtime python37
