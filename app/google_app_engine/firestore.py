# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START bookshelf_firestore_client_import]
import uuid
from dataclasses import dataclass, asdict

from google.cloud import datastore
# [END bookshelf_firestore_client_import]


@dataclass
class Image:
    email: str
    filename: str
    file_digest: str

    def key(self) -> str:
        return self.email + ":" + self.file_digest


def create(image: Image) -> bool:
    db = datastore.Client()
    key = db.key('images', image.key())
    # Check if image already exists
    image_exists = db.get(key)
    if image_exists:
        return False
    entity = datastore.Entity(key=key)
    entity.update(asdict(image))
    db.put(entity)
    return True
