#!/bin/bash

python manage.py makemigrations
python manage.py migrate

source create-superuser.sh

python manage.py runserver 0.0.0.0:5005