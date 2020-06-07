sed -u "s/_BUCKET_IMAGES/$BUCKET_IMAGES/g" app.yaml.template > app.yaml.tmp
sed -u "s/_PROJECT_ID/$PROJECT_ID/g" app.yaml.tmp > app.yaml.tmp2
sed -u "s/_PROJECT_NUMBER/$PROJECT_NUMBER/g" app.yaml.tmp2 > app.yaml

rm app.yaml.tmp
rm app.yaml.tmp2

gcloud app deploy -q
