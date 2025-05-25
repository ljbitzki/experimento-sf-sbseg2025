#!/bin/bash
# Start redis
service redis-server start

# Collect static files
echo "Inicializando Celery"
celery -A net2d worker --loglevel=INFO &

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python manage.py makemigrations

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Run Django
echo "Starting Django"
python manage.py runserver 0:8000