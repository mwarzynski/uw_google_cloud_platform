#!/bin/bash

# Test Cloud Functions.
(cd gcf_1; source venv/bin/activate; pytest main_test.py)
(cd gcf_2; source venv/bin/activate; pytest main_test.py)
(cd gcf_3; source venv/bin/activate; pytest main_test.py)

# Test App Engine service,
(cd app/google_app_engine; source venv/bin/activate; pytest main_test.py)


