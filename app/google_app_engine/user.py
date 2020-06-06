from google.auth import jwt
import requests
import os
from flask import make_response, request, g
from functools import wraps

cloud_project_number = os.getenv("PROJECT_NUMBER")
cloud_project_id = os.getenv("PROJECT_ID")

test_user = None


def authorize_by_headers(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if test_user:
            g.username = test_user
        else:
            user_header = request.headers.get("X-Goog-Authenticated-User-Email")
            if user_header is None or len(user_header) == 0:
                return make_response("not authorized"), 401
            g.username = user_header.replace("accounts.google.com:", "")
        return f(*args, **kwargs)
    return decorated_function


def authorize_by_jwt(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if test_user:
            g.username = test_user
        else:
            auth_token = None
            for k, v in request.cookies.items():
                if "GCP_IAAP_AUTH_TOKEN_" in k:
                    auth_token = v
                    break
            if not auth_token:
                return make_response("not authorized"), 401
            _, username, err = validate_iap_jwt_from_app_engine(auth_token)
            if not username:
                return make_response("not authorized"), 401
            g.username = username
        return f(*args, **kwargs)
    return decorated_function


def validate_iap_jwt_from_app_engine(iap_jwt):
    """Validate a JWT passed to your App Engine app by Identity-Aware Proxy.

    Args:
      iap_jwt: The contents of the X-Goog-IAP-JWT-Assertion header.
      cloud_project_number: The project *number* for your Google Cloud project.
          This is returned by 'gcloud projects describe $PROJECT_ID', or
          in the Project Info card in Cloud Console.
      cloud_project_id: The project *ID* for your Google Cloud project.

    Returns:
      (user_id, user_email, error_str).
    """
    expected_audience = '/projects/{}/apps/{}'.format(
        cloud_project_number, cloud_project_id)
    return _validate_iap_jwt(iap_jwt, expected_audience)


def _validate_iap_jwt(iap_jwt, expected_audience):
    try:
        # Retrieve public key for token signature verification.
        key_id = jwt.decode_header(iap_jwt).get('kid')
        if not key_id:
            return (None, None, '**ERROR: no key ID**')
        key = _get_iap_key(key_id)

        # Verify token signature, expiry and audience.
        decoded_jwt = jwt.decode(iap_jwt, certs=key, audience=expected_audience)

        # Verify token issuer.
        if decoded_jwt.get('iss') != 'https://cloud.google.com/iap':
            return (None, None, '**ERROR: invalid issuer**')

        return (decoded_jwt['sub'], decoded_jwt['email'], '')
    except (ValueError, requests.exceptions.RequestException) as e:
        return (None, None, '**ERROR: JWT validation error {}**'.format(e))


def _get_iap_key(key_id):
    """Retrieves a public key from the list published by Identity-Aware Proxy,
    re-fetching the key file if necessary.
    """
    key_cache = _get_iap_key.key_cache
    key = key_cache.get(key_id)
    if not key:
        # Re-fetch the key file.
        resp = requests.get(
            'https://www.gstatic.com/iap/verify/public_key')
        if resp.status_code != 200:
            raise Exception(
                'Unable to fetch IAP keys: {} / {} / {}'.format(
                    resp.status_code, resp.headers, resp.text))
        key_cache = resp.json()
        _get_iap_key.key_cache = key_cache
        key = key_cache.get(key_id)
        if not key:
            raise Exception('Key {!r} not found'.format(key_id))
    return key


# Used to cache the Identity-Aware Proxy public keys.  This code only
# refetches the file when a JWT is signed with a key not present in
# this cache.
_get_iap_key.key_cache = {}
