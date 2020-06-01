from google.cloud import datastore

db = datastore.Client()


def get_image_by_id(key_id: str):
    key = db.key('images', key_id)
    return db.get(key)


def update_image_text(image, image_text: str):
    image.update({"image_text": image_text})
    db.put(image)
