#!/bin/bash

gcloud functions deploy gcf3 \
    --trigger-topic=$TOPIC_EMAILS_TO_SEND \
    --service-account=service-account-gcf@gcp-lectures-project.iam.gserviceaccount.com \
    --set-env-vars SENDGRID_API_KEY=$SENDGRID_API_KEY \
    --runtime python37
