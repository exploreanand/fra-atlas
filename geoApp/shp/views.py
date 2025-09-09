from django.shortcuts import render
from django.http import JsonResponse
from .models import Shp, Claimant
from tiff.models import Tiff
from note.models import Note

# Create your views here.
def index(request):
    shp = Shp.objects.all()
    tiff = Tiff.objects.all()
    return render(request, 'index.html', {'shp': shp, 'tiff': tiff, 'note': note})

def note(request):
    if(request.method == 'POST'):
        note_heading = request.POST.get('note-heading')
        note = request.POST.get('note')
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')
        print(note_heading, note, lat, lng, 'email username')
        return render(request, 'index.html')
    return render(request, 'index.html')

def get_claimants_data(request):
    """Return claimants data for highlighting features"""
    village = request.GET.get('village', 'Pimpalgaon Khu')
    claimants = Claimant.objects.filter(village_name=village)
    
    data = {
        'village_name': village,
        'serial_numbers': list(claimants.values_list('serial_number', flat=True)),
        'claimants': list(claimants.values(
            'serial_number', 'claimant_name', 'code_13_digit', 
            'claim_number', 'gat_number', 'area'
        ))
    }
    return JsonResponse(data)

def get_available_villages(request):
    """Return list of all available villages"""
    villages = Claimant.objects.values(
        'village_name', 'taluka', 'district'
    ).distinct().order_by('village_name')
    
    return JsonResponse({
        'villages': list(villages)
    })