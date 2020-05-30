#!/bin/bash

gcloud functions deploy gcf2 \
    --trigger-bucket=$BUCKET_IMAGES_SCALED \
    --set-env-vars \
        PROJECT_ID=$PROJECT_ID,TOPIC_NAME=$TOPIC_IMAGE_WAS_SCALED \
    --runtime python37
