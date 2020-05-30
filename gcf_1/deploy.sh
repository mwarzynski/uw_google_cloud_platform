#!/bin/bash

gcloud functions deploy gcf1 \
    --trigger-bucket=$BUCKET_IMAGES \
    --set-env-vars \
        BUCKET_IMAGES_SCALED=$BUCKET_IMAGES_SCALED \
    --runtime python37

