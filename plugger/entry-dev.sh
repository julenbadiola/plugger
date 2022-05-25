#!/bin/bash
python manage.py makemigrations

python manage.py migrate
echo "" | python manage.py shell
cat <<EOF | python manage.py shell
from django.contrib.auth import get_user_model

User = get_user_model()  # get the currently active user model,

if not User.objects.filter(username='${ADMIN_USER}').exists():
    User.objects.create_superuser('${ADMIN_USER}', '${ADMIN_EMAIL}', '${ADMIN_PASSWORD}')

EOF

python manage.py runserver 0.0.0.0:5005