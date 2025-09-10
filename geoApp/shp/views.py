from django.shortcuts import render
from django.http import JsonResponse
import json
import os
from django.conf import settings

def index(request):
    """Main dashboard view with map and claimant data"""
    # Load note data for the map
    from note.models import Note
    notes = Note.objects.all()
    
    context = {
        'note': notes
    }
    return render(request, 'index.html', context)

def get_claimants_data(request):
    """API endpoint to get claimants data for a specific village"""
    village_name = request.GET.get('village')
    
    if not village_name:
        return JsonResponse({'error': 'Village name is required'}, status=400)
    
    # Load village data from JSON file
    villages_dir = os.path.join(settings.BASE_DIR, 'data', 'villages')
    file_path = os.path.join(villages_dir, f'{village_name.lower().replace(" ", "_")}.json')
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            village_data = json.load(f)
        
        return JsonResponse(village_data)
    except FileNotFoundError:
        return JsonResponse({'error': 'Village data not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_available_villages(request):
    """API endpoint to get list of available villages"""
    villages_dir = os.path.join(settings.BASE_DIR, 'data', 'villages')
    villages = []
    
    if os.path.exists(villages_dir):
        for filename in os.listdir(villages_dir):
            if filename.endswith('.json'):
                try:
                    file_path = os.path.join(villages_dir, filename)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        village_data = json.load(f)
                        villages.append({
                            'name': village_data.get('document_details', {}).get('village_name', filename.replace('.json', '')),
                            'filename': filename.replace('.json', '')
                        })
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
                    continue
    
    return JsonResponse({'villages': villages})

def analytics(request):
    """Analytics page showcasing PM Yojanas"""
    return render(request, 'analytics.html')

def pm_kisan_details(request):
    """PM Kisan details page with FRA claimant eligibility analysis"""
    import json
    import os
    from django.conf import settings
    
    # Load all village data from JSON files
    villages_data = []
    total_claimants = 0
    eligible_claimants = 0
    priority_claimants = 0
    high_priority_claimants = 0
    
    villages_dir = os.path.join(settings.BASE_DIR, 'data', 'villages')
    
    if os.path.exists(villages_dir):
        for filename in os.listdir(villages_dir):
            if filename.endswith('.json'):
                file_path = os.path.join(villages_dir, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        village_data = json.load(f)
                        
                    # Process claimants for PM Kisan eligibility
                    processed_claimants = []
                    for claimant in village_data.get('claimants', []):
                        # Convert area to float for comparison
                        try:
                            area = float(claimant.get('area', 0))
                        except (ValueError, TypeError):
                            area = 0
                        
                        claimant['area'] = area
                        
                        # PM Kisan eligibility logic: area <= 2.0 hectares
                        is_eligible = area <= 2.0
                        is_priority = area <= 1.0  # Very small landholders get priority
                        is_high_priority = area <= 0.5  # Extremely small landholders get high priority
                        
                        claimant['eligible'] = is_eligible
                        claimant['priority'] = is_priority
                        claimant['high_priority'] = is_high_priority
                        
                        if is_eligible:
                            eligible_claimants += 1
                        if is_priority:
                            priority_claimants += 1
                        if is_high_priority:
                            high_priority_claimants += 1
                        
                        total_claimants += 1
                        processed_claimants.append(claimant)
                    
                    village_data['claimants'] = processed_claimants
                    villages_data.append(village_data)
                    
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
                    continue
    
    context = {
        'villages_data': villages_data,
        'total_claimants': total_claimants,
        'eligible_claimants': eligible_claimants,
        'priority_claimants': priority_claimants,
        'high_priority_claimants': high_priority_claimants,
    }
    
    return render(request, 'pm_kisan_details.html', context)

def mgnrega_details(request):
    """MGNREGA details page with FRA claimant eligibility analysis"""
    import json
    import os
    from django.conf import settings
    
    # Load all village data from JSON files
    villages_data = []
    total_claimants = 0
    eligible_claimants = 0
    priority_claimants = 0
    high_priority_claimants = 0
    
    villages_dir = os.path.join(settings.BASE_DIR, 'data', 'villages')
    
    if os.path.exists(villages_dir):
        for filename in os.listdir(villages_dir):
            if filename.endswith('.json'):
                file_path = os.path.join(villages_dir, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        village_data = json.load(f)
                        
                    # Process claimants for MGNREGA eligibility
                    processed_claimants = []
                    for claimant in village_data.get('claimants', []):
                        # Convert area to float for comparison
                        try:
                            area = float(claimant.get('area', 0))
                        except (ValueError, TypeError):
                            area = 0
                        
                        claimant['area'] = area
                        
                        # MGNREGA eligibility logic: all rural residents are eligible
                        # Priority based on economic status and community background
                        is_eligible = True  # All rural residents are eligible
                        is_priority = False
                        is_high_priority = False
                        
                        # Priority criteria
                        if area <= 2.0:  # Small landholders
                            is_priority = True
                        
                        # High priority criteria
                        name_lower = claimant.get('claimant_name', '').lower()
                        
                        # SC/ST communities get high priority
                        sc_st_indicators = ['chaudhari', 'gavali', 'malche', 'pawar', 'ahire', 'gaikwad', 'sonvane', 'gangurde', 'badhir', 'bhoye', 'deshmukh']
                        if any(indicator in name_lower for indicator in sc_st_indicators):
                            is_high_priority = True
                        
                        # Women get high priority
                        women_indicators = ['bai', 'ya', 'i']
                        if any(name_lower.endswith(indicator) for indicator in women_indicators):
                            is_high_priority = True
                        
                        claimant['eligible'] = is_eligible
                        claimant['priority'] = is_priority
                        claimant['high_priority'] = is_high_priority
                        
                        if is_eligible:
                            eligible_claimants += 1
                        if is_priority:
                            priority_claimants += 1
                        if is_high_priority:
                            high_priority_claimants += 1
                        
                        total_claimants += 1
                        processed_claimants.append(claimant)
                    
                    village_data['claimants'] = processed_claimants
                    villages_data.append(village_data)
                    
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
                    continue
    
    context = {
        'villages_data': villages_data,
        'total_claimants': total_claimants,
        'eligible_claimants': eligible_claimants,
        'priority_claimants': priority_claimants,
        'high_priority_claimants': high_priority_claimants,
    }
    
    return render(request, 'mgnrega_details.html', context)

def pm_jai_jeevan_details(request):
    """PM Jai Jeevan Yojana details page with FRA claimant eligibility analysis"""
    import json
    import os
    from django.conf import settings
    
    # Load all village data from JSON files
    villages_data = []
    total_claimants = 0
    eligible_claimants = 0
    priority_claimants = 0
    high_priority_claimants = 0
    
    villages_dir = os.path.join(settings.BASE_DIR, 'data', 'villages')
    
    if os.path.exists(villages_dir):
        for filename in os.listdir(villages_dir):
            if filename.endswith('.json'):
                file_path = os.path.join(villages_dir, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        village_data = json.load(f)
                        
                    # Process claimants for PM Jai Jeevan eligibility
                    processed_claimants = []
                    for claimant in village_data.get('claimants', []):
                        # Convert area to float for comparison
                        try:
                            area = float(claimant.get('area', 0))
                        except (ValueError, TypeError):
                            area = 0
                        
                        claimant['area'] = area
                        
                        # PM Jai Jeevan eligibility logic: all rural residents are eligible
                        # Priority based on water quality issues and economic status
                        is_eligible = True  # All rural residents are eligible
                        is_priority = False
                        is_high_priority = False
                        
                        # Priority criteria - small landholders
                        if area <= 2.0:  # Small landholders
                            is_priority = True
                        
                        # High priority criteria
                        name_lower = claimant.get('claimant_name', '').lower()
                        
                        # SC/ST communities get high priority
                        sc_st_indicators = ['chaudhari', 'gavali', 'malche', 'pawar', 'ahire', 'gaikwad', 'sonvane', 'gangurde', 'badhir', 'bhoye', 'deshmukh']
                        if any(indicator in name_lower for indicator in sc_st_indicators):
                            is_high_priority = True
                        
                        # Women get high priority
                        women_indicators = ['bai', 'ya', 'i']
                        if any(name_lower.endswith(indicator) for indicator in women_indicators):
                            is_high_priority = True
                        
                        # Very small landholders get high priority
                        if area <= 1.0:
                            is_high_priority = True
                        
                        # Areas with no gat number (likely water quality issues) get high priority
                        if not claimant.get('gat_number') or claimant.get('gat_number') == 'null':
                            is_high_priority = True
                        
                        claimant['eligible'] = is_eligible
                        claimant['priority'] = is_priority
                        claimant['high_priority'] = is_high_priority
                        
                        if is_eligible:
                            eligible_claimants += 1
                        if is_priority:
                            priority_claimants += 1
                        if is_high_priority:
                            high_priority_claimants += 1
                        
                        total_claimants += 1
                        processed_claimants.append(claimant)
                    
                    village_data['claimants'] = processed_claimants
                    villages_data.append(village_data)
                    
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
                    continue
    
    context = {
        'villages_data': villages_data,
        'total_claimants': total_claimants,
        'eligible_claimants': eligible_claimants,
        'priority_claimants': priority_claimants,
        'high_priority_claimants': high_priority_claimants,
    }
    
    return render(request, 'pm_jai_jeevan_details.html', context)

def pm_ayushman_details(request):
    """PM Ayushman Bharat details page with FRA claimant eligibility analysis"""
    import json
    import os
    from django.conf import settings
    
    # Load all village data from JSON files
    villages_data = []
    total_claimants = 0
    eligible_claimants = 0
    priority_claimants = 0
    high_priority_claimants = 0
    
    villages_dir = os.path.join(settings.BASE_DIR, 'data', 'villages')
    
    if os.path.exists(villages_dir):
        for filename in os.listdir(villages_dir):
            if filename.endswith('.json'):
                file_path = os.path.join(villages_dir, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        village_data = json.load(f)
                        
                    # Process claimants for PM Ayushman Bharat eligibility
                    processed_claimants = []
                    for claimant in village_data.get('claimants', []):
                        # Convert area to float for comparison
                        try:
                            area = float(claimant.get('area', 0))
                        except (ValueError, TypeError):
                            area = 0
                        
                        claimant['area'] = area
                        
                        # PM Ayushman Bharat eligibility logic: all rural residents are eligible
                        # Priority based on economic status and family size
                        is_eligible = True  # All rural residents are eligible
                        is_priority = False
                        is_high_priority = False
                        
                        # Priority criteria - small landholders
                        if area <= 2.0:  # Small landholders
                            is_priority = True
                        
                        # High priority criteria
                        name_lower = claimant.get('claimant_name', '').lower()
                        
                        # SC/ST communities get high priority
                        sc_st_indicators = ['chaudhari', 'gavali', 'malche', 'pawar', 'ahire', 'gaikwad', 'sonvane', 'gangurde', 'badhir', 'bhoye', 'deshmukh']
                        if any(indicator in name_lower for indicator in sc_st_indicators):
                            is_high_priority = True
                        
                        # Women get high priority
                        women_indicators = ['bai', 'ya', 'i']
                        if any(name_lower.endswith(indicator) for indicator in women_indicators):
                            is_high_priority = True
                        
                        # Very small landholders get high priority
                        if area <= 1.0:
                            is_high_priority = True
                        
                        # Areas with no claim number (likely need healthcare) get high priority
                        if not claimant.get('claim_number') or claimant.get('claim_number') == 'null':
                            is_high_priority = True
                        
                        # Estimate family size based on area and community
                        estimated_family_size = 4  # Default
                        if area <= 1.0:
                            estimated_family_size = 6  # Larger families in smaller landholdings
                        elif area <= 2.0:
                            estimated_family_size = 5
                        
                        # SC/ST communities tend to have larger families
                        if any(indicator in name_lower for indicator in sc_st_indicators):
                            estimated_family_size += 1
                        
                        claimant['eligible'] = is_eligible
                        claimant['priority'] = is_priority
                        claimant['high_priority'] = is_high_priority
                        claimant['estimated_family_size'] = estimated_family_size
                        
                        if is_eligible:
                            eligible_claimants += 1
                        if is_priority:
                            priority_claimants += 1
                        if is_high_priority:
                            high_priority_claimants += 1
                        
                        total_claimants += 1
                        processed_claimants.append(claimant)
                    
                    village_data['claimants'] = processed_claimants
                    villages_data.append(village_data)
                    
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
                    continue
    
    context = {
        'villages_data': villages_data,
        'total_claimants': total_claimants,
        'eligible_claimants': eligible_claimants,
        'priority_claimants': priority_claimants,
        'high_priority_claimants': high_priority_claimants,
    }
    
    return render(request, 'pm_ayushman_details.html', context)

def pm_kaushal_details(request):
    """PM Kaushal Vikas details page with FRA claimant eligibility analysis"""
    import json
    import os
    from django.conf import settings
    
    # Load all village data from JSON files
    villages_data = []
    total_claimants = 0
    eligible_claimants = 0
    priority_claimants = 0
    high_priority_claimants = 0
    
    villages_dir = os.path.join(settings.BASE_DIR, 'data', 'villages')
    
    if os.path.exists(villages_dir):
        for filename in os.listdir(villages_dir):
            if filename.endswith('.json'):
                file_path = os.path.join(villages_dir, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        village_data = json.load(f)
                        
                    # Process claimants for PM Kaushal Vikas eligibility
                    processed_claimants = []
                    for claimant in village_data.get('claimants', []):
                        # Convert area to float for comparison
                        try:
                            area = float(claimant.get('area', 0))
                        except (ValueError, TypeError):
                            area = 0
                        
                        claimant['area'] = area
                        
                        # Estimate age based on serial number
                        serial_number = claimant.get('serial_number', '1')
                        try:
                            serial_num = int(serial_number)
                            # Estimate age: younger serial numbers = older people
                            # Assuming serial numbers 1-50 are older (40-60), 51-100 are middle-aged (25-40), 101+ are younger (18-35)
                            if serial_num <= 50:
                                estimated_age = 50 - (serial_num * 0.4)  # 30-50 years
                            elif serial_num <= 100:
                                estimated_age = 40 - ((serial_num - 50) * 0.3)  # 25-40 years
                            else:
                                estimated_age = 35 - ((serial_num - 100) * 0.2)  # 18-35 years
                            
                            estimated_age = max(18, min(65, int(estimated_age)))
                        except (ValueError, TypeError):
                            estimated_age = 35  # Default age
                        
                        claimant['estimated_age'] = estimated_age
                        
                        # PM Kaushal Vikas eligibility logic: age 15-45 years
                        is_eligible = 15 <= estimated_age <= 45
                        is_priority = False
                        is_high_priority = False
                        
                        # Priority criteria - small landholders
                        if area <= 2.0 and is_eligible:  # Small landholders
                            is_priority = True
                        
                        # High priority criteria
                        name_lower = claimant.get('claimant_name', '').lower()
                        
                        # SC/ST communities get high priority
                        sc_st_indicators = ['chaudhari', 'gavali', 'malche', 'pawar', 'ahire', 'gaikwad', 'sonvane', 'gangurde', 'badhir', 'bhoye', 'deshmukh']
                        if any(indicator in name_lower for indicator in sc_st_indicators) and is_eligible:
                            is_high_priority = True
                        
                        # Women get high priority
                        women_indicators = ['bai', 'ya', 'i']
                        if any(name_lower.endswith(indicator) for indicator in women_indicators) and is_eligible:
                            is_high_priority = True
                        
                        # Very small landholders get high priority
                        if area <= 1.0 and is_eligible:
                            is_high_priority = True
                        
                        # Young adults (18-30) get high priority
                        if 18 <= estimated_age <= 30 and is_eligible:
                            is_high_priority = True
                        
                        claimant['eligible'] = is_eligible
                        claimant['priority'] = is_priority
                        claimant['high_priority'] = is_high_priority
                        
                        if is_eligible:
                            eligible_claimants += 1
                        if is_priority:
                            priority_claimants += 1
                        if is_high_priority:
                            high_priority_claimants += 1
                        
                        total_claimants += 1
                        processed_claimants.append(claimant)
                    
                    village_data['claimants'] = processed_claimants
                    villages_data.append(village_data)
                    
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
                    continue
    
    context = {
        'villages_data': villages_data,
        'total_claimants': total_claimants,
        'eligible_claimants': eligible_claimants,
        'priority_claimants': priority_claimants,
        'high_priority_claimants': high_priority_claimants,
    }
    
    return render(request, 'pm_kaushal_details.html', context)

def digital_india_details(request):
    """Digital India details page with FRA claimant eligibility analysis"""
    import json
    import os
    from django.conf import settings
    
    # Load all village data from JSON files
    villages_data = []
    total_claimants = 0
    eligible_claimants = 0
    priority_claimants = 0
    high_priority_claimants = 0
    
    villages_dir = os.path.join(settings.BASE_DIR, 'data', 'villages')
    
    if os.path.exists(villages_dir):
        for filename in os.listdir(villages_dir):
            if filename.endswith('.json'):
                file_path = os.path.join(villages_dir, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        village_data = json.load(f)
                        
                    # Process claimants for Digital India eligibility
                    processed_claimants = []
                    for claimant in village_data.get('claimants', []):
                        # Convert area to float for comparison
                        try:
                            area = float(claimant.get('area', 0))
                        except (ValueError, TypeError):
                            area = 0
                        
                        claimant['area'] = area
                        
                        # Digital India eligibility logic:
                        # 1. Universal access - all citizens are eligible
                        # 2. Priority given to rural areas (all FRA claimants are rural)
                        # 3. High priority for SC/ST communities
                        # 4. High priority for women
                        # 5. High priority for economically weaker sections
                        # 6. Digital readiness assessment based on landholding and community
                        
                        is_eligible = True  # Universal access for all citizens
                        is_priority = False
                        is_high_priority = False
                        
                        # Digital readiness assessment
                        digital_readiness = "Basic"
                        
                        # Priority criteria - rural areas get priority
                        if area <= 2.0:  # Small landholders
                            is_priority = True
                            digital_readiness = "Medium"
                        
                        # High priority criteria
                        name_lower = claimant.get('claimant_name', '').lower()
                        
                        # SC/ST communities get high priority for digital inclusion
                        sc_st_indicators = ['chaudhari', 'gavali', 'malche', 'pawar', 'ahire', 'gaikwad', 'sonvane', 'gangurde', 'badhir', 'bhoye', 'deshmukh']
                        if any(indicator in name_lower for indicator in sc_st_indicators):
                            is_high_priority = True
                            digital_readiness = "High"
                        
                        # Women get high priority for digital empowerment
                        women_indicators = ['bai', 'ya', 'i']
                        if any(name_lower.endswith(indicator) for indicator in women_indicators):
                            is_high_priority = True
                            if digital_readiness == "Basic":
                                digital_readiness = "Medium"
                        
                        # Very small landholders get high priority
                        if area <= 1.0:
                            is_high_priority = True
                            digital_readiness = "High"
                        
                        # Areas with no claim number (likely need digital services) get high priority
                        if not claimant.get('claim_number') or claimant.get('claim_number') == 'null':
                            is_high_priority = True
                            digital_readiness = "High"
                        
                        # Areas with no gat number (likely need digital documentation) get high priority
                        if not claimant.get('gat_number') or claimant.get('gat_number') == 'null':
                            is_high_priority = True
                            if digital_readiness == "Basic":
                                digital_readiness = "Medium"
                        
                        # Digital readiness levels
                        if digital_readiness == "Basic":
                            digital_readiness = "Basic - Needs Digital Literacy"
                        elif digital_readiness == "Medium":
                            digital_readiness = "Medium - Ready for Digital Services"
                        elif digital_readiness == "High":
                            digital_readiness = "High - Priority for Digital Inclusion"
                        
                        claimant['eligible'] = is_eligible
                        claimant['priority'] = is_priority
                        claimant['high_priority'] = is_high_priority
                        claimant['digital_readiness'] = digital_readiness
                        
                        if is_eligible:
                            eligible_claimants += 1
                        if is_priority:
                            priority_claimants += 1
                        if is_high_priority:
                            high_priority_claimants += 1
                        
                        total_claimants += 1
                        processed_claimants.append(claimant)
                    
                    village_data['claimants'] = processed_claimants
                    villages_data.append(village_data)
                    
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
                    continue
    
    context = {
        'villages_data': villages_data,
        'total_claimants': total_claimants,
        'eligible_claimants': eligible_claimants,
        'priority_claimants': priority_claimants,
        'high_priority_claimants': high_priority_claimants,
    }
    
    return render(request, 'digital_india_details.html', context)

def startup_india_details(request):
    """Startup India details page with FRA claimant entrepreneurship potential analysis"""
    import json
    import os
    from django.conf import settings
    
    # Load all village data from JSON files
    villages_data = []
    total_claimants = 0
    eligible_claimants = 0
    priority_claimants = 0
    high_priority_claimants = 0
    
    villages_dir = os.path.join(settings.BASE_DIR, 'data', 'villages')
    
    if os.path.exists(villages_dir):
        for filename in os.listdir(villages_dir):
            if filename.endswith('.json'):
                file_path = os.path.join(villages_dir, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        village_data = json.load(f)
                        
                    # Process claimants for Startup India entrepreneurship potential
                    processed_claimants = []
                    for claimant in village_data.get('claimants', []):
                        # Convert area to float for comparison
                        try:
                            area = float(claimant.get('area', 0))
                        except (ValueError, TypeError):
                            area = 0
                        
                        claimant['area'] = area
                        
                        # Estimate age based on serial number (similar to PM Kaushal logic)
                        serial_number = claimant.get('serial_number', '1')
                        try:
                            serial_num = int(serial_number)
                            # Estimate age: younger serial numbers = older people
                            # Assuming serial numbers 1-50 are older (40-60), 51-100 are middle-aged (25-40), 101+ are younger (18-35)
                            if serial_num <= 50:
                                estimated_age = 50 - (serial_num * 0.4)  # 30-50 years
                            elif serial_num <= 100:
                                estimated_age = 40 - ((serial_num - 50) * 0.3)  # 25-40 years
                            else:
                                estimated_age = 35 - ((serial_num - 100) * 0.2)  # 18-35 years
                            
                            estimated_age = max(18, min(65, int(estimated_age)))
                        except (ValueError, TypeError):
                            estimated_age = 35  # Default age
                        
                        claimant['estimated_age'] = estimated_age
                        
                        # Startup India eligibility logic:
                        # 1. Age factor: 18-45 years have higher startup potential
                        # 2. Land resources: Can be leveraged for agri-tech startups
                        # 3. Community background: SC/ST get priority for startup support
                        # 4. Gender inclusion: Women get special startup incentives
                        # 5. Economic need: Small landholders have higher motivation
                        
                        is_eligible = 18 <= estimated_age <= 45  # Age criteria for startup potential
                        is_priority = False
                        is_high_priority = False
                        
                        # Startup potential assessment
                        startup_potential = "Limited"
                        age_group = "Senior"
                        startup_phase = "Mature"
                        
                        if 18 <= estimated_age <= 30:
                            age_group = "Young Adult"
                            startup_phase = "Early Stage"
                        elif 31 <= estimated_age <= 40:
                            age_group = "Adult"
                            startup_phase = "Growth Stage"
                        elif 41 <= estimated_age <= 45:
                            age_group = "Experienced"
                            startup_phase = "Expansion Stage"
                        
                        # Priority criteria - small landholders have higher motivation
                        if area <= 2.0 and is_eligible:  # Small landholders
                            is_priority = True
                            startup_potential = "Good"
                        
                        # High priority criteria
                        name_lower = claimant.get('claimant_name', '').lower()
                        
                        # SC/ST communities get high priority for startup support
                        sc_st_indicators = ['chaudhari', 'gavali', 'malche', 'pawar', 'ahire', 'gaikwad', 'sonvane', 'gangurde', 'badhir', 'bhoye', 'deshmukh']
                        if any(indicator in name_lower for indicator in sc_st_indicators) and is_eligible:
                            is_high_priority = True
                            startup_potential = "Excellent"
                        
                        # Women get high priority for startup incentives
                        women_indicators = ['bai', 'ya', 'i']
                        if any(name_lower.endswith(indicator) for indicator in women_indicators) and is_eligible:
                            is_high_priority = True
                            if startup_potential == "Limited":
                                startup_potential = "Good"
                        
                        # Very small landholders get high priority (higher motivation)
                        if area <= 1.0 and is_eligible:
                            is_high_priority = True
                            startup_potential = "Excellent"
                        
                        # Young adults (18-30) get high priority
                        if 18 <= estimated_age <= 30 and is_eligible:
                            is_high_priority = True
                            startup_potential = "Excellent"
                        
                        # Areas with no claim number (likely need economic opportunities) get high priority
                        if (not claimant.get('claim_number') or claimant.get('claim_number') == 'null') and is_eligible:
                            is_high_priority = True
                            startup_potential = "Excellent"
                        
                        # Startup potential levels
                        if startup_potential == "Limited":
                            startup_potential = "Limited - Focus on Traditional Skills"
                        elif startup_potential == "Good":
                            startup_potential = "Good - Agri-Tech & Rural Business Potential"
                        elif startup_potential == "Excellent":
                            startup_potential = "Excellent - High Startup Potential"
                        
                        claimant['eligible'] = is_eligible
                        claimant['priority'] = is_priority
                        claimant['high_priority'] = is_high_priority
                        claimant['startup_potential'] = startup_potential
                        claimant['age_group'] = age_group
                        claimant['startup_phase'] = startup_phase
                        
                        if is_eligible:
                            eligible_claimants += 1
                        if is_priority:
                            priority_claimants += 1
                        if is_high_priority:
                            high_priority_claimants += 1
                        
                        total_claimants += 1
                        processed_claimants.append(claimant)
                    
                    village_data['claimants'] = processed_claimants
                    villages_data.append(village_data)
                    
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
                    continue
    
    context = {
        'villages_data': villages_data,
        'total_claimants': total_claimants,
        'eligible_claimants': eligible_claimants,
        'priority_claimants': priority_claimants,
        'high_priority_claimants': high_priority_claimants,
    }
    
    return render(request, 'startup_india_details.html', context)

def about(request):
    """About page for FRA Atlas"""
    return render(request, 'about.html')