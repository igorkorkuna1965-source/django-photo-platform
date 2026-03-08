#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
python manage.py create_remote_superuser
gunicorn mysite.wsgi:application --bind 0.0.0.0:$PORT