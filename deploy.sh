#!/bin/bash

export PROJECT_ID=$(gcloud config get-value project)

export SENDGRID_API_KEY="NO_SECRETS_IN_GIT_AS_EVERY_RESPONSIBLE_CITIZEN_WOULD_DO"

### CREATE

#gcloud services enable storage-component.googleapis.com
#gcloud services enable cloudapis.googleapis.com    
#gcloud services enable cloudfunctions.googleapis.com
#gcloud services enable pubsub.googleapis.com
#gcloud services enable vision.googleapis.com
gcloud services enable appengine.googleapis.com
gcloud services enable storage-api.googleapis.com
gcloud services enable logging.googleapis.com
gcloud services enable clouderrorreporting.googleapis.com
gcloud services enable iap.googleapis.com

# Creating a bucket for Cloud Functions
export BUCKET_GCF=$PROJECT_ID-gcf
export BUCKET_IMAGES=$PROJECT_ID-images
export BUCKET_IMAGES_SCALED=$PROJECT_ID-images-scaled

#gsutil mb gs://$BUCKET_GCF
#gsutil mb gs://$BUCKET_IMAGES
#gsutil mb gs://$BUCKET_IMAGES_SCALED

# Creating Pub/Sub
export TOPIC_IMAGE_WAS_SCALED=image-was-scaled
#gcloud pubsub topics create $TOPIC_IMAGE_WAS_SCALED

# Create Firebase Datastore
# https://console.cloud.google.com/firestore/welcome?project=$PROJECT_ID
# It's not possible to do so using `gcloud`.

# Deployment of Cloud Function
#(cd gcf_1; ./deploy.sh)
#(cd gcf_2; ./deploy.sh)
#(cd gcf_3; ./deploy.sh)

# # Deploy service 'app' to Cloud Run.
# (cd app/google_app_engine; ./deploy.sh)
# Setup IAP to require credentials.


### DELETE

# gcloud beta functions delete name
