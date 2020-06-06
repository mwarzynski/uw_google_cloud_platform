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

from mock import MagicMock
import pytest
import datastore

datastore.Client = MagicMock()


import main
from six import BytesIO

auth_headers = {"X-Goog-Authenticated-User-Email": "accounts.google.com:tester@google.com"}


@pytest.yield_fixture
def app(request):
    """This fixture provides a Flask app instance configured for testing.

    It also ensures the tests run within a request context, allowing
    any calls to flask.request, flask.current_app, etc. to work."""
    main.storage = MagicMock()
    main.datastore = MagicMock()
    app = main.app
    with app.test_request_context():
        yield app


def test_add(app):
    data = {'image': (BytesIO(b'test'), 'hello.jpg')}
    with app.test_client() as c:
        rv = c.post('/', data=data, headers=auth_headers, follow_redirects=True)
    assert rv.status == '200 OK'


def test_upload_bad_file(app):
    data = {
        'image': (BytesIO(b'<?php phpinfo(); ?>'),
                  '1337h4x0r.php')
    }
    with app.test_client() as c:
        rv = c.post('/', data=data, headers=auth_headers, follow_redirects=True)
    # check we weren't pwned
    assert rv.status == '400 BAD REQUEST'
