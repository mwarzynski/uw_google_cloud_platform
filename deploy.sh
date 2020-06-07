#!/bin/bash

export PROJECT_ID=$(gcloud config get-value project)

export SENDGRID_API_KEY="NO_SECRETS_IN_GIT_AS_EVERY_RESPONSIBLE_CITIZEN_WOULD_DO"

### CREATE

#gcloud services enable storage-component.googleapis.com
#gcloud services enable cloudapis.googleapis.com    
#gcloud services enable cloudfunctions.googleapis.com
#gcloud services enable pubsub.googleapis.com
#gcloud services enable vision.googleapis.com
#gcloud services enable appengine.googleapis.com
#gcloud services enable storage-api.googleapis.com
#gcloud services enable logging.googleapis.com
#gcloud services enable clouderrorreporting.googleapis.com
#gcloud services enable iap.googleapis.com
#gcloud services enable sourcerepo.googleapis.com
#gcloud services enable cloudbuild.googleapis.com
#gcloud services enable cloudkms.googleapis.com

#gcloud kms keyrings create mykeyring --location=global
#gcloud kms keys create images --purpose=encryption --location=global --keyring=mykeyring

# Create repositories.
#gcloud source repos create gcf1
#gcloud source repos create gcf2
#gcloud source repos create gcf3
#gcloud source repos create app

# Creating a bucket for Cloud Functions
export BUCKET_GCF=$PROJECT_ID-gcf
export BUCKET_IMAGES=$PROJECT_ID-images
export BUCKET_IMAGES_SCALED=$PROJECT_ID-images-scaled

# gsutil mb gs://$BUCKET_GCF
# gsutil mb gs://$BUCKET_IMAGES
# gsutil mb gs://$BUCKET_IMAGES_SCALED

# Creating Pub/Sub
export TOPIC_EMAILS_TO_SEND=emails-to-send
# gcloud pubsub topics create $TOPIC_EMAILS_TO_SEND

# Create Firebase Datastore
# https://console.cloud.google.com/firestore/welcome?project=$PROJECT_ID
# It's not possible to do so using `gcloud`.

# Deployment of Cloud Function
# (cd gcf_1; ./deploy.sh)
# (cd gcf_2; ./deploy.sh)
# (cd gcf_3; ./deploy.sh)

# Deploy service 'app' to Cloud Run.
#(cd app/google_app_engine; ./deploy.sh)

# Setup IAP to require credentials.


### DELETE

# gcloud beta functions delete name
