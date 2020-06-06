#!/bin/bash

gcloud functions deploy gcf2 \
    --trigger-bucket=$BUCKET_IMAGES_SCALED \
    --set-env-vars \
        BUCKET_IMAGES_SCALED=$BUCKET_IMAGES_SCALED,PROJECT_ID=$PROJECT_ID,TOPIC_NAME=$TOPIC_EMAILS_TO_SEND \
    --runtime python37
