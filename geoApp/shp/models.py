from django.db import models
import datetime
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import geopandas as gpd
import os
import glob
import zipfile
from sqlalchemy import *
# This fiona import is good practice to have when working with geopandas
import fiona
from geo.Geoserver import Geoserver
from pg.pg import Pg

####################################################################################
# Geoserver parameters and conn_str
####################################################################################
# initializing the library
db = Pg(dbname='geoapp', user='postgres',
        password='123456', host='localhost', port='5432')
geo = Geoserver('http://127.0.0.1:8080/geoserver',
                username='admin', password='geoserver')
# Database connection string (postgresql://${database_user}:${databse_password}@${database_host}:${database_port}/${database_name}
conn_str = 'postgresql://postgres:123456@localhost:5432/geoapp'


######################################################################################
# Shp model
######################################################################################
# The shapefile model
class Shp(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000, blank=True)
    file = models.FileField(upload_to= '%Y/%m/%d')
    uploaded_date = models.DateField(default=datetime.date.today, blank=True)

    def __str__(self):
        return self.name


# Django post save signal
@receiver(post_save, sender=Shp)
def public_data(sender, instance, created, **kwargs):
    file = instance.file.path
    file_format = os.path.basename(file).split('.')[-1]
    file_name = os.path.basename(file).split('.')[0]
    file_path = os.path.dirname(file)
    name = instance.name

    # extract zipfile
    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall(file_path)

    os.remove(file)  # remove zip file

    shp = glob.glob(r'{}/**/*.shp'.format(file_path),
                    recursive=True)  # to get shp
    try:
        req_shp = shp[0]
        # This line is correct and works perfectly with modern geopandas
        gdf = gpd.read_file(req_shp)  # make geodataframe
        engine = create_engine(conn_str)
        gdf.to_postgis(
            con=engine,
            schema='data',
            name=name,
            if_exists="replace")

        # --- CODE IMPROVEMENT ---
        # This logic is improved to delete all associated shapefile files
        # (e.g., .shp, .shx, .dbf, .prj), not just the .shp file.
        file_path_no_ext = os.path.splitext(req_shp)[0]
        for f in glob.glob(f"{file_path_no_ext}.*"):
            os.remove(f)

    except Exception as e:
        # Improved cleanup for error cases as well
        shp_files = glob.glob(r'{}/**/*.shp'.format(file_path), recursive=True)
        for shp_file in shp_files:
            file_path_no_ext = os.path.splitext(shp_file)[0]
            for f in glob.glob(f"{file_path_no_ext}.*"):
                os.remove(f)

        instance.delete()
        print("There is problem during shp upload: ", e)

    # publish shp to the geoserver using geoserver-rest
    geo.create_featurestore(store_name='geoApp', workspace='geoapp', db='geoapp',
                            host='localhost', pg_user='postgres', pg_password='123456', schema='data')
    geo.publish_featurestore(
        workspace='geoapp', store_name='geoApp', pg_table=name)

    # For styling of layer
    geo.create_outline_featurestyle('geoApp_shp', workspace='geoapp')

    geo.publish_style(
        layer_name=name, style_name='geoApp_shp', workspace='geoapp')



# Django post delete signal for both DB and GeoServer
@receiver(post_delete, sender=Shp)
def delete_table(sender, instance, **kwargs):
    db.delete_table(instance.name, schema='data')
    geo.delete_layer(instance.name, 'geoapp')