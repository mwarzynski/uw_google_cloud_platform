#!/bin/bash

gcloud functions deploy gcf2 \
    --trigger-bucket=$BUCKET_IMAGES_SCALED \
    --service-account=service-account-gcf@gcp-lectures-project.iam.gserviceaccount.com \
    --set-env-vars \
        BUCKET_IMAGES=$BUCKET_IMAGES,BUCKET_IMAGES_SCALED=$BUCKET_IMAGES_SCALED,PROJECT_ID=$PROJECT_ID,TOPIC_NAME=$TOPIC_EMAILS_TO_SEND,GOOGLE_APPLICATION_CREDENTIALS=./service_account.json \
    --runtime python37
