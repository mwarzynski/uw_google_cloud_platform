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

import logging
import hashlib
import datastore
import os
from flask import g, current_app, Flask, render_template
from flask import request
from google.cloud import error_reporting
import google.cloud.logging
import storage
import user
from werkzeug.exceptions import BadRequest

datastore_client = datastore.Client()


app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.urandom(24),
    MAX_CONTENT_LENGTH=8 * 1024 * 1024,
    ALLOWED_EXTENSIONS={'png', 'jpg', 'jpeg'}
)

app.debug = False
app.testing = False

# Configure logging
if not app.testing:
    logging.basicConfig(level=logging.INFO)
    client = google.cloud.logging.Client()
    # Attaches a Google Stackdriver logging handler to the root logger
    client.setup_logging(logging.INFO)
if app.testing:
    user.test_user = "tester@google.com"


def _check_extension(filename, allowed_extensions):
    file, ext = os.path.splitext(filename)
    if ext.replace('.', '') not in allowed_extensions:
        raise BadRequest(
            '{0} has an invalid name or extension'.format(filename))


@app.route('/', methods=['GET', 'POST'])
@user.authorize_by_headers
def main():
    if request.method == "GET":
        return render_template('form.html')
    # Parse form data.
    data = request.form.to_dict(flat=True)
    image = request.files.get('image')
    _check_extension(image.filename, current_app.config['ALLOWED_EXTENSIONS'])
    data['filename'] = image.filename
    _, file_extension = os.path.splitext(image.filename)
    data['email'] = g.username
    image_data = image.read()
    image_file_digest = str(hashlib.md5(image_data).hexdigest())
    data['file_digest'] = image_file_digest
    # Run this block of code in transaction.
    # If anything will go wrong, then it will rollback changes in Datastore (created entity).
    with datastore_client.transaction():
        f_image = datastore.Image(data['email'], data['filename'], image_file_digest)
        created = datastore_client.create(f_image)
        if not created:
            return render_template('form.html', message="Image already exists!")
        storage.upload_file(
            image_data,
            f_image.key() + file_extension,
            image.content_type
        )
    return render_template('form.html', message="Image added to processing queue.")


@app.route('/errors')
def errors():
    raise Exception('This is an intentional exception.')


# Add an error handler that reports exceptions to Stackdriver Error
# Reporting. Note that this error handler is only used when debug
# is False
@app.errorhandler(500)
def server_error(e):
    client = error_reporting.Client()
    client.report_exception(
        http_context=error_reporting.build_flask_context(request))
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


# This is only used when running locally. When running live, gunicorn runs
# the application.
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
