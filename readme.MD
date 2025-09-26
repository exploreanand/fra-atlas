To start django_pro1 venv:
source "/Users/mymac/Coding Main/GEO Main/DJANGO/django_pro1/bin/activate"

To start PostgreSQL
bash 'pgadmin-server' into the terminal, its a shortcut an (alias)
username: admin
password: 123456


To start geoserver
bash - conda activate geoserver_env
bash - geoserver ~/geoserver-data
username : admin
password : geoserver

To start Django Server
bash - python manage.py runserver

Django Admin Login:
username: admin
password: admin

To make requirement.txt
pip freeze > requirements.txt

You can add unlimited villages by simply:
Adding JSON files to data/villages/
Running python manage.py populate_claimants --load-all
Uploading corresponding shapefiles
The system will automatically handle everything else!