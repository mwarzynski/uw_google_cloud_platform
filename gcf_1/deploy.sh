#!/bin/bash

gcloud functions deploy gcf1 \
    --trigger-bucket=${_BUCKET_IMAGES} \
    --set-env-vars \
        BUCKET_IMAGES_SCALED=${_BUCKET_IMAGES_SCALED} \
    --runtime python37

