#!/bin/bash

python manage.py migrate

source create-superuser.sh

gunicorn --config gunicorn-cfg.py core.wsgi