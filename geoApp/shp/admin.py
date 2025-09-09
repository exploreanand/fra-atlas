from django.contrib import admin
from .models import Shp, Claimant

# Register your models here.
admin.site.register(Shp)

@admin.register(Claimant)
class ClaimantAdmin(admin.ModelAdmin):
    list_display = ['serial_number', 'claimant_name', 'code_13_digit', 'claim_number', 'area', 'village_name']
    list_filter = ['village_name', 'taluka', 'district']
    search_fields = ['claimant_name', 'code_13_digit', 'claim_number']
    ordering = ['serial_number']