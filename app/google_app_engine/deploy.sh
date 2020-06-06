sed -u "s/{{BUCKET_IMAGES}}/$BUCKET_IMAGES/g" app.yaml.template > app.yaml

gcloud app deploy
