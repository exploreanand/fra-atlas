# Multi-Village JSON Data Management System

This directory contains the scalable solution for managing JSON data from multiple villages for dynamic highlighting in the GIS application.

## Directory Structure

```
geoApp/data/
├── villages/
│   ├── pimpalgaon_khu.json
│   ├── sample_village.json
│   └── [additional_village_files].json
└── README.md (this file)
```

## JSON File Format

Each village JSON file should follow this standardized format:

```json
{
  "document_details": {
    "title": "Information on forest dwellers and their 13-digit codes...",
    "village_name": "Village Name Here",
    "taluka": "Taluka Name",
    "district": "District Name"
  },
  "claimants": [
    {
      "serial_number": 1,
      "claimant_name": "Claimant Full Name",
      "code_13_digit": "Unique 13-digit code",
      "claim_number": "Claim number or null",
      "gat_number": "Gat number or null",
      "area": "Area in hectares or 'Illegible'"
    }
    // ... more claimants
  ]
}
```

## File Naming Convention

- Use lowercase letters
- Replace spaces with underscores
- Use `.json` extension
- Example: `"New Village Name"` → `new_village_name.json`

## Management Commands

### Load All Villages
```bash
python manage.py populate_claimants --load-all
```

### Load Specific Village
```bash
python manage.py populate_claimants --village="Village Name"
```

### Load from Specific File
```bash
python manage.py populate_claimants --json-file="/path/to/village.json"
```

### Load Default (Pimpalgaon - backward compatibility)
```bash
python manage.py populate_claimants
```

## API Endpoints

### Get Claimants Data
```
GET /api/claimants/?village=Village%20Name
```
Returns claimants data for highlighting features where `patta_id` matches `serial_number`.

### Get Available Villages
```
GET /api/villages/
```
Returns list of all available villages with their taluka and district information.

## Frontend Integration

The system automatically:
1. Loads available villages from the API
2. Updates location dropdowns dynamically
3. Fetches claimants data when village is selected
4. Highlights shapefile features where `patta_id` matches `serial_number`

## Adding New Villages

1. **Create JSON file**: Add your village data in the `villages/` directory following the naming convention
2. **Load data**: Run `python manage.py populate_claimants --load-all` or load the specific village
3. **Verify**: The village will automatically appear in the frontend dropdown

## Highlighting Logic

- Shapefile features with `patta_id` attribute matching any `serial_number` from the selected village will be highlighted in red
- The highlighting updates dynamically when switching between villages
- Serial number dropdown shows all claimants for the selected village

## Troubleshooting

### Common Issues

1. **Village not appearing in dropdown**:
   - Check if JSON file is properly formatted
   - Ensure the file is in the correct directory
   - Run `python manage.py populate_claimants --load-all`

2. **Highlighting not working**:
   - Verify shapefile has `patta_id` attribute
   - Check if `serial_number` values match `patta_id` values
   - Ensure village data is loaded in database

3. **JSON parsing errors**:
   - Validate JSON syntax using online JSON validators
   - Check for proper encoding (UTF-8)
   - Ensure all required fields are present

### Validation Commands

```bash
# Check if villages are loaded
python manage.py shell
>>> from shp.models import Claimant
>>> Claimant.objects.values('village_name').distinct()

# Check specific village data
>>> Claimant.objects.filter(village_name="Village Name").count()
```

## Data Backup

Before adding new data or making changes:
```bash
# Backup current database
python manage.py dumpdata shp.Claimant > claimants_backup.json

# Restore if needed
python manage.py loaddata claimants_backup.json
```

## Performance Notes

- The system can handle multiple villages efficiently
- Village data is cached in the frontend
- API calls are made only when switching villages
- Database queries are optimized with proper indexing

## Security Considerations

- JSON files should be properly validated before loading
- Only authorized users should have access to management commands
- Consider implementing file upload restrictions in production

---

For technical support or questions about this system, please refer to the main project documentation or contact the development team.
