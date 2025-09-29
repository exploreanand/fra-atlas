"""
URL configuration for geoApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from shp.views import index, get_claimants_data, get_available_villages, analytics, pm_kisan_details, mgnrega_details, pm_jai_jeevan_details, pm_ayushman_details, pm_kaushal_details, digital_india_details, startup_india_details
from note.views import note

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health', lambda request: HttpResponse('ok'), name='health'),
    path('',index, name='index' ),
    path('note/', note, name='note'),
    path('analytics/', analytics, name='analytics'),
    path('pm-kisan-details/', pm_kisan_details, name='pm_kisan_details'),
    path('mgnrega-details/', mgnrega_details, name='mgnrega_details'),
    path('pm-jai-jeevan-details/', pm_jai_jeevan_details, name='pm_jai_jeevan_details'),
    path('pm-ayushman-details/', pm_ayushman_details, name='pm_ayushman_details'),
    path('pm-kaushal-details/', pm_kaushal_details, name='pm_kaushal_details'),
    path('digital-india-details/', digital_india_details, name='digital_india_details'),
    path('startup-india-details/', startup_india_details, name='startup_india_details'),
    path('api/claimants/', get_claimants_data, name='get_claimants_data'),
    path('api/villages/', get_available_villages, name='get_available_villages')
]
