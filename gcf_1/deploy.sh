#!/bin/bash

gcloud functions deploy gcf1 \
    --trigger-bucket=$BUCKET_IMAGES \
    --service-account=service-account-gcf@gcp-lectures-project.iam.gserviceaccount.com \
    --set-env-vars \
        BUCKET_IMAGES_SCALED=$BUCKET_IMAGES_SCALED \
    --runtime python37

