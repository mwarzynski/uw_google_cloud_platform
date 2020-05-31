#!/bin/bash

export PROJECT_ID=$(gcloud config get-value project)

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
# gcloud builds submit --tag gcr.io/${PROJECT_ID}/app
# gcloud run deploy --image gcr.io/${PROJECT_ID}/app --platform managed




### DELETE

# gcloud beta functions delete name
