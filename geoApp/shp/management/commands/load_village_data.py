import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from shp.models import Claimant


class Command(BaseCommand):
    help = 'Load village data from JSON files into the Claimant model'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force reload data even if it already exists',
        )

    def handle(self, *args, **options):
        self.stdout.write('Loading village data from JSON files...')
        
        # Path to the villages data directory
        villages_dir = os.path.join(settings.BASE_DIR, 'data', 'villages')
        
        if not os.path.exists(villages_dir):
            self.stdout.write(
                self.style.ERROR(f'Villages directory not found: {villages_dir}')
            )
            return
        
        total_loaded = 0
        total_skipped = 0
        
        # Process each JSON file in the villages directory
        for filename in os.listdir(villages_dir):
            if not filename.endswith('.json'):
                continue
                
            file_path = os.path.join(villages_dir, filename)
            self.stdout.write(f'Processing {filename}...')
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Extract village information
                doc_details = data.get('document_details', {})
                village_name = doc_details.get('village_name', 'Unknown')
                taluka = doc_details.get('taluka', 'Unknown')
                district = doc_details.get('district', 'Unknown')
                
                # Process claimants
                claimants = data.get('claimants', [])
                village_loaded = 0
                village_skipped = 0
                
                for claimant_data in claimants:
                    # Handle area field - convert to string if it's a number
                    area = claimant_data.get('area', '0')
                    if isinstance(area, (int, float)):
                        area = str(area)
                    
                    # Use get_or_create to avoid duplicates
                    claimant, created = Claimant.objects.get_or_create(
                        serial_number=claimant_data.get('serial_number'),
                        village_name=village_name,
                        defaults={
                            'claimant_name': claimant_data.get('claimant_name', ''),
                            'code_13_digit': claimant_data.get('code_13_digit', ''),
                            'claim_number': claimant_data.get('claim_number', ''),
                            'gat_number': claimant_data.get('gat_number', ''),
                            'area': area,
                            'taluka': taluka,
                            'district': district,
                        }
                    )
                    
                    if created:
                        village_loaded += 1
                        total_loaded += 1
                    else:
                        village_skipped += 1
                        total_skipped += 1
                
                self.stdout.write(
                    f'  {village_name}: {village_loaded} loaded, {village_skipped} skipped'
                )
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error processing {filename}: {e}')
                )
                continue
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Data loading completed! Total: {total_loaded} loaded, {total_skipped} skipped'
            )
        )
        
        # Show summary of loaded data
        total_claimants = Claimant.objects.count()
        villages = Claimant.objects.values('village_name').distinct().count()
        districts = Claimant.objects.values('district').distinct().count()
        
        self.stdout.write(f'Database now contains:')
        self.stdout.write(f'  - {total_claimants} claimants')
        self.stdout.write(f'  - {villages} villages')
        self.stdout.write(f'  - {districts} districts')
