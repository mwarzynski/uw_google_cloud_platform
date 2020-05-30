# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from google.cloud import pubsub_v1

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(os.getenv('PROJECT_ID'), os.getenv('TOPIC_NAME'))


def gcf2(file_data, context):
    future = publisher.publish(topic_path, file_data['name'].encode("utf-8"))
    future.add_done_callback(get_callback)


def get_callback(f, data):
    def callback(f):
        try:
            print(f.result())
        except:  # noqa
            print("Please handle {} for {}.".format(f.exception(), data))
    return callback
