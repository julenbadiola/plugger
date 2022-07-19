#!/bin/bash

cat <<EOF | python manage.py shell
from django.contrib.auth import get_user_model

User = get_user_model()  # get the currently active user model,

if not User.objects.filter(username='${ADMIN_USER}').exists():
    print("Creating superuser")
    User.objects.create_superuser('${ADMIN_USER}', '${ADMIN_EMAIL}', '${ADMIN_PASSWORD}')
else:
    print("Superuser already created")
EOF