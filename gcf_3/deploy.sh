#!/bin/bash

gcloud functions deploy gcf3 \
    --trigger-topic=$TOPIC_IMAGE_WAS_SCALED \
    --set-env-vars \
        BUCKET_IMAGES_SCALED=$BUCKET_IMAGES_SCALED \
    --runtime python37
