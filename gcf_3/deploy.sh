#!/bin/bash

gcloud functions deploy gcf3 \
    --trigger-topic=$TOPIC_EMAILS_TO_SEND \
    --set-env-vars SENDGRID_API_KEY=$SENDGRID_API_KEY \
    --runtime python37
