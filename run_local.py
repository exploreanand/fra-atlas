#!/usr/bin/env python
"""
Local development server runner.
This script runs the Django development server with local settings.
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

if __name__ == "__main__":
    # Set Django settings module to local settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geoApp.settings_local')
    
    # Add the project directory to Python path
    project_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, project_dir)
    
    # Setup Django
    django.setup()
    
    # Run the development server
    execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8000'])
