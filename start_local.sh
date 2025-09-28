#!/bin/bash

# Activate virtual environment
source django_pro1/bin/activate

# Set Django settings to local
export DJANGO_SETTINGS_MODULE=geoApp.settings_local

# Change to project directory
cd geoApp

# Run migrations
python manage.py migrate

# Create superuser if it doesn't exist
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print('Superuser created: admin/admin')
else:
    print('Superuser already exists')
"

# Start development server
python manage.py runserver 0.0.0.0:8000
