from django.core.management.base import BaseCommand
from shp.models import Claimant
import json
import os
from django.conf import settings
import glob

class Command(BaseCommand):
    help = 'Populate claimants data from JSON files'

    def add_arguments(self, parser):
        parser.add_argument('--village', type=str, help='Specific village name')
        parser.add_argument('--json-file', type=str, help='Path to specific JSON file')
        parser.add_argument('--load-all', action='store_true', help='Load all village JSON files')

    def handle(self, *args, **options):
        if options.get('load_all'):
            self.load_all_villages()
        elif options.get('json_file'):
            self.load_from_file(options['json_file'])
        elif options.get('village'):
            self.load_village(options['village'])
        else:
            # Default: load hardcoded Pimpalgaon data
            self.load_hardcoded_pimpalgaon()

    def load_all_villages(self):
        """Load all JSON files from the villages directory"""
        villages_dir = os.path.join(settings.BASE_DIR, 'data', 'villages')
        if not os.path.exists(villages_dir):
            self.stdout.write(self.style.ERROR(f'Villages directory not found: {villages_dir}'))
            return

        json_files = glob.glob(os.path.join(villages_dir, '*.json'))
        if not json_files:
            self.stdout.write(self.style.WARNING('No JSON files found in villages directory'))
            return

        total_loaded = 0
        for json_file in json_files:
            try:
                loaded_count = self.load_from_file(json_file)
                total_loaded += loaded_count
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error loading {json_file}: {e}'))

        self.stdout.write(self.style.SUCCESS(f'Successfully loaded {total_loaded} total claimants from {len(json_files)} villages'))

    def load_village(self, village_name):
        """Load specific village by name"""
        villages_dir = os.path.join(settings.BASE_DIR, 'data', 'villages')
        # Convert village name to filename format
        filename = village_name.lower().replace(' ', '_').replace('.', '_') + '.json'
        json_file = os.path.join(villages_dir, filename)
        
        if not os.path.exists(json_file):
            self.stdout.write(self.style.ERROR(f'JSON file not found for village: {json_file}'))
            return
        
        self.load_from_file(json_file)

    def load_from_file(self, json_file):
        """Load claimants data from a JSON file"""
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                claimants_data = json.load(f)
            
            return self.create_claimants(claimants_data, json_file)
        except json.JSONDecodeError as e:
            self.stdout.write(self.style.ERROR(f'Invalid JSON in {json_file}: {e}'))
            return 0
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error reading {json_file}: {e}'))
            return 0

    def load_hardcoded_pimpalgaon(self):
        claimants_data = {
            "document_details": {
                "title": "Information on forest dwellers and their 13-digit codes in reference to the titles distributed to eligible claimants",
                "village_name": "Pimpalgaon Khu",
                "taluka": "Sakri",
                "district": "Dhule"
            },
            "claimants": [
                {
                    "serial_number": 1,
                    "claimant_name": "Shama Soma Deshmukh",
                    "code_13_digit": "0203Pim01SSD0",
                    "claim_number": None,
                    "gat_number": "2-09",
                    "area": "3.09"
                },
                {
                    "serial_number": 2,
                    "claimant_name": "Suka Mila Gaikwad",
                    "code_13_digit": "0203Pim01SBG0",
                    "claim_number": None,
                    "gat_number": None,
                    "area": "2.47"
                },
                {
                    "serial_number": 3,
                    "claimant_name": "Sakharya Joga Malvi",
                    "code_13_digit": "0203Pim01SJM0",
                    "claim_number": "180",
                    "gat_number": None,
                    "area": "2.95"
                },
                {
                    "serial_number": 4,
                    "claimant_name": "Hatya Bherya Baris",
                    "code_13_digit": "0203Pim01HBB0",
                    "claim_number": "181",
                    "gat_number": None,
                    "area": "2.34"
                },
                {
                    "serial_number": 5,
                    "claimant_name": "Sonya Babula Desai",
                    "code_13_digit": "0203Pim01SDB0",
                    "claim_number": "182",
                    "gat_number": None,
                    "area": "1.46"
                },
                {
                    "serial_number": 6,
                    "claimant_name": "Lakadya Mukka Valvi",
                    "code_13_digit": "0203Pim01PLV0",
                    "claim_number": "183",
                    "gat_number": None,
                    "area": "1.78"
                },
                {
                    "serial_number": 7,
                    "claimant_name": "Appa Sonu Gaikwad",
                    "code_13_digit": "0203Pim01ASG0",
                    "claim_number": "184",
                    "gat_number": None,
                    "area": "1.42"
                },
                {
                    "serial_number": 8,
                    "claimant_name": "Beshya Kasha Gogurde",
                    "code_13_digit": "0203Pim01BKG0",
                    "claim_number": "185",
                    "gat_number": None,
                    "area": "1.58"
                },
                {
                    "serial_number": 9,
                    "claimant_name": "Pimpalgaon Gangaram Pawar",
                    "code_13_digit": "0203Pim01DGP0",
                    "claim_number": "186",
                    "gat_number": None,
                    "area": "3.03"
                },
                {
                    "serial_number": 10,
                    "claimant_name": "Pudya Mahadu Bhoye",
                    "code_13_digit": "0203Pim01PMB0",
                    "claim_number": "188",
                    "gat_number": None,
                    "area": "Illegible"
                },
                {
                    "serial_number": 11,
                    "claimant_name": "Jivlya Lakadya Valvi",
                    "code_13_digit": "0203Pim01JLV0",
                    "claim_number": "189",
                    "gat_number": None,
                    "area": "Illegible"
                },
                {
                    "serial_number": 12,
                    "claimant_name": "Baba Lala Desai",
                    "code_13_digit": "0203Pim01BLD0",
                    "claim_number": "190",
                    "gat_number": None,
                    "area": "0.72"
                },
                {
                    "serial_number": 13,
                    "claimant_name": "Sonya Dhedya Kuvar",
                    "code_13_digit": "0203Pim01SDK0",
                    "claim_number": "191",
                    "gat_number": None,
                    "area": "1.65"
                },
                {
                    "serial_number": 14,
                    "claimant_name": "Daga Kolsha Gaikwad",
                    "code_13_digit": "0203Pim01DKG0",
                    "claim_number": "192",
                    "gat_number": None,
                    "area": "0.59"
                },
                {
                    "serial_number": 15,
                    "claimant_name": "Baburao Dhedya Kakade",
                    "code_13_digit": "0203Pim01BDK1",
                    "claim_number": "193",
                    "gat_number": None,
                    "area": "1.50"
                },
                {
                    "serial_number": 16,
                    "claimant_name": "Nurjya Sonya Raut",
                    "code_13_digit": "0203Pim01NSR0",
                    "claim_number": "194",
                    "gat_number": None,
                    "area": "2.64"
                },
                {
                    "serial_number": 17,
                    "claimant_name": "Rivlya Lakadya Valvi",
                    "code_13_digit": "0203Pim01RLV0",
                    "claim_number": "195",
                    "gat_number": None,
                    "area": "1.17"
                },
                {
                    "serial_number": 18,
                    "claimant_name": "Rodya Babla Desai",
                    "code_13_digit": "0203Pim01RBD0",
                    "claim_number": "196",
                    "gat_number": None,
                    "area": "0.58"
                },
                {
                    "serial_number": 19,
                    "claimant_name": "Vichya Lakadya Valvi",
                    "code_13_digit": "0203Pim01VLV0",
                    "claim_number": "197",
                    "gat_number": None,
                    "area": "1.94"
                },
                {
                    "serial_number": 20,
                    "claimant_name": "Rajya Bhonya Kuvar",
                    "code_13_digit": "0203Pim01RBK0",
                    "claim_number": "198",
                    "gat_number": None,
                    "area": "2.32"
                },
                {
                    "serial_number": 21,
                    "claimant_name": "Raju Barku Chaure",
                    "code_13_digit": "0203Pim01RBC0",
                    "claim_number": "199",
                    "gat_number": None,
                    "area": "Illegible"
                },
                {
                    "serial_number": 22,
                    "claimant_name": "Gulbya Motiram Gaikwad",
                    "code_13_digit": "0203Pim01GMG0",
                    "claim_number": "200",
                    "gat_number": None,
                    "area": "Illegible"
                },
                {
                    "serial_number": 23,
                    "claimant_name": "Budha Dhedya Kuvar",
                    "code_13_digit": "0203Pim01BDK0",
                    "claim_number": "201",
                    "gat_number": None,
                    "area": "Illegible"
                },
                {
                    "serial_number": 24,
                    "claimant_name": "Revya Varsha Desai",
                    "code_13_digit": "0203Pim01RVD0",
                    "claim_number": "202",
                    "gat_number": None,
                    "area": "0.63"
                },
                {
                    "serial_number": 25,
                    "claimant_name": "Rajya Hanya Valvi",
                    "code_13_digit": "0203Pim01RHV0",
                    "claim_number": "203",
                    "gat_number": None,
                    "area": "1.42"
                },
                {
                    "serial_number": 26,
                    "claimant_name": "Baba Budha Kuvar",
                    "code_13_digit": "0203Pim01BBK0",
                    "claim_number": "204",
                    "gat_number": None,
                    "area": "1.22"
                },
                {
                    "serial_number": 27,
                    "claimant_name": "Murlidhar Ramdas Choudhary",
                    "code_13_digit": "0203Pim01MRC0",
                    "claim_number": "205",
                    "gat_number": None,
                    "area": "2.86"
                },
                {
                    "serial_number": 28,
                    "claimant_name": "Ganpat Ganya Chaure",
                    "code_13_digit": "0203Pim01GGC0",
                    "claim_number": "206",
                    "gat_number": None,
                    "area": "1.58"
                },
                {
                    "serial_number": 29,
                    "claimant_name": "Kubya Vakhadya Pavara",
                    "code_13_digit": "0203Pim01KVP0",
                    "claim_number": "207",
                    "gat_number": "207",
                    "area": "1.47"
                },
                {
                    "serial_number": 30,
                    "claimant_name": "Murlidhar Gangaram Pawar",
                    "code_13_digit": "0203Pim01MGP0",
                    "claim_number": "208",
                    "gat_number": None,
                    "area": "1.33"
                },
                {
                    "serial_number": 31,
                    "claimant_name": "Lotan Jatrya Desai",
                    "code_13_digit": "0203Pim01LJD0",
                    "claim_number": "209",
                    "gat_number": None,
                    "area": "2.10"
                },
                {
                    "serial_number": 32,
                    "claimant_name": "Banda Kharbu Sonawane",
                    "code_13_digit": "0203Pim01BKS0",
                    "claim_number": "210",
                    "gat_number": None,
                    "area": "0.25"
                },
                {
                    "serial_number": 33,
                    "claimant_name": "Munya Chila Chaure",
                    "code_13_digit": "0203Pim01MCC0",
                    "claim_number": "211",
                    "gat_number": None,
                    "area": "1.02"
                },
                {
                    "serial_number": 34,
                    "claimant_name": "Phulya Valya Raut",
                    "code_13_digit": "0203Pim01FVR0",
                    "claim_number": "212",
                    "gat_number": None,
                    "area": "0.55"
                },
                {
                    "serial_number": 35,
                    "claimant_name": "Sukanya Rajya Valvi",
                    "code_13_digit": "0203Pim01SRV0",
                    "claim_number": "213",
                    "gat_number": None,
                    "area": "0.41"
                }
            ]
        }

        
        self.create_claimants(claimants_data, "hardcoded")

    def create_claimants(self, claimants_data, source):
        """Create claimant records from data"""
        village_name = claimants_data['document_details']['village_name']
        
        # Clear existing data for this village
        existing_count = Claimant.objects.filter(village_name=village_name).count()
        Claimant.objects.filter(village_name=village_name).delete()
        
        if existing_count > 0:
            self.stdout.write(f'Cleared {existing_count} existing records for {village_name}')

        # Create new claimant records
        created_count = 0
        for claimant_data in claimants_data['claimants']:
            try:
                claimant = Claimant.objects.create(
                    serial_number=claimant_data['serial_number'],
                    claimant_name=claimant_data['claimant_name'],
                    code_13_digit=claimant_data['code_13_digit'],
                    claim_number=claimant_data.get('claim_number'),
                    gat_number=claimant_data.get('gat_number'),
                    area=str(claimant_data['area']),
                    village_name=claimants_data['document_details']['village_name'],
                    taluka=claimants_data['document_details'].get('taluka', ''),
                    district=claimants_data['document_details'].get('district', '')
                )
                created_count += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating claimant {claimant_data.get("serial_number", "unknown")}: {e}'))

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} claimant records for {village_name} from {source}')
        )
        return created_count
