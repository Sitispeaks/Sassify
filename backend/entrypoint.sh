#!/bin/sh

python manage.py makemigrations --no-input
python manage.py migrate --no-input
python manage.py collectstatic --no-input

gunicorn --workers 4 --threads 4 backend.wsgi:application --bind 0.0.0.0:8000


# docker-compose run --rm  web python /app/backend/manage.py search_index --rebuild