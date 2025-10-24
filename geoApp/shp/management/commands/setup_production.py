from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import connection
from django.core.management import call_command
import os


class Command(BaseCommand):
    help = 'Setup production environment'

    def handle(self, *args, **options):
        self.stdout.write('Setting up production environment...')
        
        # Create superuser if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password=os.getenv('ADMIN_PASSWORD', 'admin123')
            )
            self.stdout.write(
                self.style.SUCCESS('Superuser created: admin')
            )
        else:
            self.stdout.write('Superuser already exists')
        
        # Enable PostGIS extension
        with connection.cursor() as cursor:
            try:
                cursor.execute("CREATE EXTENSION IF NOT EXISTS postgis;")
                cursor.execute("CREATE EXTENSION IF NOT EXISTS postgis_topology;")
                self.stdout.write(
                    self.style.SUCCESS('PostGIS extensions enabled')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f'PostGIS setup warning: {e}')
                )
        
        # Load village data
        try:
            self.stdout.write('Loading village data...')
            call_command('load_village_data')
            self.stdout.write(
                self.style.SUCCESS('Village data loaded successfully')
            )
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'Village data loading warning: {e}')
            )
        
        self.stdout.write(
            self.style.SUCCESS('Production setup completed!')
        )
