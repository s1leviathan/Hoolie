from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, FileResponse, Http404
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage

def index(request):
    """Main introduction page with beautiful animations"""
    return render(request, 'main/index.html')

def select_pet(request):
    """Pet selection page"""
    return render(request, 'main/select_pet.html')

def pet_gender(request):
    """Pet gender selection page"""
    pet_type = request.GET.get('type', 'pet')
    context = {
        'pet_type': pet_type
    }
    return render(request, 'main/pet_gender.html', context)

def pet_birthdate(request):
    """Pet birth date selection page"""
    pet_type = request.GET.get('type', 'pet')
    gender = request.GET.get('gender', '')
    context = {
        'pet_type': pet_type,
        'gender': gender
    }
    return render(request, 'main/pet_birthdate.html', context)

def pet_breed(request):
    """Dog breed selection page"""
    pet_type = request.GET.get('type', 'pet')
    gender = request.GET.get('gender', '')
    birthdate = request.GET.get('birthdate', '')
    
    # Common dog breeds for dropdown
    dog_breeds = [
        'Λαμπραντόρ', 'Γκόλντεν Ρετρίβερ', 'Γερμανικός Ποιμενικός', 'Μπουλντόγκ',
        'Πούντλ', 'Μπίγκλ', 'Ρότβαϊλερ', 'Γιόρκσαϊρ Τέριερ', 'Ντάξχουντ',
        'Σιμπέριαν Χάσκι', 'Πομερανιάν', 'Σιτσού', 'Μπόξερ', 'Τσιουάουα',
        'Μαλτέζ', 'Κοκέρ Σπάνιελ', 'Μπορντέρ Κόλι', 'Φρέντς Μπουλντόγκ',
        'Αυστραλιανός Ποιμενικός', 'Μπασέτ Χάουντ'
    ]
    
    context = {
        'pet_type': pet_type,
        'gender': gender,
        'birthdate': birthdate,
        'breeds': dog_breeds
    }
    return render(request, 'main/pet_breed.html', context)

def cat_breed(request):
    """Cat breed selection page"""
    pet_type = request.GET.get('type', 'pet')
    gender = request.GET.get('gender', '')
    birthdate = request.GET.get('birthdate', '')
    
    # Common cat breeds for dropdown  
    cat_breeds = [
        'Περσική', 'Μέιν Κουν', 'Σιαμέζα', 'Ραγκντόλ', 'Βρετανική Κοντότριχη',
        'Αμπισίνια', 'Ρωσική Μπλε', 'Σκωτσέζικη Πτυχωτή', 'Σφίγκα',
        'Βεγγαλική', 'Μάνξ', 'Νορβηγική Δασική', 'Τούρκικη Αγκυρα',
        'Αμερικανική Κοντότριχη', 'Εξωτική Κοντότριχη', 'Ορμιέντλ',
        'Σομαλί', 'Τονκινέζα', 'Μπομπέι', 'Κορνίς Ρεξ'
    ]
    
    context = {
        'pet_type': pet_type,
        'gender': gender,
        'birthdate': birthdate,
        'breeds': cat_breeds
    }
    return render(request, 'main/cat_breed.html', context)

def pet_name(request):
    """Pet name input page"""
    pet_type = request.GET.get('type', 'pet')
    gender = request.GET.get('gender', '')
    birthdate = request.GET.get('birthdate', '')
    breed = request.GET.get('breed', '')
    
    context = {
        'pet_type': pet_type,
        'gender': gender,
        'birthdate': birthdate,
        'breed': breed
    }
    return render(request, 'main/pet_name.html', context)

def pet_documents(request):
    """Pet documents upload page"""
    pet_type = request.GET.get('type', 'pet')
    gender = request.GET.get('gender', '')
    birthdate = request.GET.get('birthdate', '')
    breed = request.GET.get('breed', '')
    name = request.GET.get('name', '')
    
    context = {
        'pet_type': pet_type,
        'gender': gender,
        'birthdate': birthdate,
        'breed': breed,
        'name': name
    }
    return render(request, 'main/pet_documents.html', context)

@csrf_exempt
@require_http_methods(["POST"])
def upload_pet_document(request):
    """API endpoint to handle pet document uploads"""
    from .models import PetDocument
    import json
    
    try:
        if 'file' not in request.FILES:
            return JsonResponse({
                'success': False,
                'error': 'Δεν βρέθηκε αρχείο'
            }, status=400)
        
        uploaded_file = request.FILES['file']
        pet_name = request.POST.get('pet_name', '')
        pet_type = request.POST.get('pet_type', '')
        
        # Validate file size (10MB max)
        max_size = 10 * 1024 * 1024  # 10MB
        if uploaded_file.size > max_size:
            return JsonResponse({
                'success': False,
                'error': f'Το αρχείο υπερβαίνει το όριο 10MB'
            }, status=400)
        
        # Validate file type
        allowed_types = [
            'application/pdf',
            'image/jpeg',
            'image/jpg',
            'image/png',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        ]
        if uploaded_file.content_type not in allowed_types:
            return JsonResponse({
                'success': False,
                'error': f'Ο τύπος αρχείου δεν είναι αποδεκτός'
            }, status=400)
        
        # Save document to S3/local storage
        document = PetDocument.objects.create(
            file=uploaded_file,
            original_filename=uploaded_file.name,
            file_size=uploaded_file.size,
            file_type=uploaded_file.content_type,
            pet_name=pet_name,
            pet_type=pet_type
        )
        
        return JsonResponse({
            'success': True,
            'document_id': document.id,
            'filename': document.original_filename,
            'file_url': document.get_file_url(),
            'message': 'Το αρχείο ανέβηκε επιτυχώς'
        })
        
    except Exception as e:
        import logging
        import traceback
        logger = logging.getLogger(__name__)
        logger.error(f"Error uploading pet document: {str(e)}")
        logger.error(traceback.format_exc())
        return JsonResponse({
            'success': False,
            'error': f'Σφάλμα κατά το ανέβασμα: {str(e)}'
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def upload_pet_photo(request):
    """API endpoint to handle pet photo uploads (minimum 5 required)"""
    from .models import PetPhoto
    import json
    
    try:
        if 'file' not in request.FILES:
            return JsonResponse({
                'success': False,
                'error': 'Δεν βρέθηκε αρχείο'
            }, status=400)
        
        uploaded_file = request.FILES['file']
        pet_name = request.POST.get('pet_name', '')
        pet_type = request.POST.get('pet_type', '')
        
        # Validate file size (10MB max)
        max_size = 10 * 1024 * 1024  # 10MB
        if uploaded_file.size > max_size:
            return JsonResponse({
                'success': False,
                'error': f'Το αρχείο υπερβαίνει το όριο 10MB'
            }, status=400)
        
        # Validate file type - only images for photos
        allowed_types = [
            'image/jpeg',
            'image/jpg',
            'image/png',
            'image/webp'
        ]
        if uploaded_file.content_type not in allowed_types:
            return JsonResponse({
                'success': False,
                'error': f'Ο τύπος αρχείου δεν είναι αποδεκτός. Μόνο εικόνες (JPG, PNG, WEBP)'
            }, status=400)
        
        # Save photo to S3/local storage
        photo = PetPhoto.objects.create(
            file=uploaded_file,
            original_filename=uploaded_file.name,
            file_size=uploaded_file.size,
            file_type=uploaded_file.content_type,
            pet_name=pet_name,
            pet_type=pet_type
        )
        
        return JsonResponse({
            'success': True,
            'photo_id': photo.id,
            'filename': photo.original_filename,
            'file_url': photo.get_file_url(),
            'message': 'Η φωτογραφία ανέβηκε επιτυχώς'
        })
        
    except Exception as e:
        import logging
        import traceback
        logger = logging.getLogger(__name__)
        logger.error(f"Error uploading pet photo: {str(e)}")
        logger.error(traceback.format_exc())
        return JsonResponse({
            'success': False,
            'error': f'Σφάλμα κατά το ανέβασμα: {str(e)}'
        }, status=500)

def health_status(request):
    """Pet health status page - NOW REPLACED WITH QUESTIONNAIRE"""
    # Handle form submission (questionnaire) - store data in session for later submission
    # The application will be submitted later from contact_info page
    if request.method == 'POST':
        # Store all questionnaire data in session for later use
        request.session['questionnaire_data'] = dict(request.POST)
        request.session['questionnaire_submitted'] = True
        
        from django.http import JsonResponse
        return JsonResponse({
            'success': True,
            'message': 'Το ερωτηματολόγιο συμπληρώθηκε επιτυχώς!'
        })
    
    # GET request - show questionnaire form (different for dogs and cats)
    pet_type = request.GET.get('type', 'pet')
    gender = request.GET.get('gender', '')
    birthdate = request.GET.get('birthdate', '')
    breed = request.GET.get('breed', '')
    name = request.GET.get('name', '')
    health_status = request.GET.get('health_status', '')
    conditions = request.GET.get('health_conditions', '')
    program = request.GET.get('program', '')
    
    context = {
        'pet_type': pet_type,
        'gender': gender,
        'birthdate': birthdate,
        'breed': breed,
        'name': name,
        'health_status': health_status,
        'health_conditions': conditions,
        'program': program
    }
    
    # Render different questionnaire template based on pet type
    if pet_type == 'dog':
        return render(request, 'main/questionnaire_dog.html', context)
    elif pet_type == 'cat':
        return render(request, 'main/questionnaire_cat.html', context)
    else:
        return render(request, 'main/questionnaire_dog.html', context)  # Default to dog

def dog_health_conditions(request):
    """Dog health conditions selection page"""
    pet_type = request.GET.get('type', 'pet')
    gender = request.GET.get('gender', '')
    birthdate = request.GET.get('birthdate', '')
    breed = request.GET.get('breed', '')
    name = request.GET.get('name', '')
    
    # Common dog health conditions
    dog_conditions = [
        'Δυσπλασία ισχίου', 'Δυσπλασία αγκώνα', 'Καταρράκτης', 'Γλαύκωμα',
        'Καρδιακές παθήσεις', 'Επιληψία', 'Αλλεργίες δέρματος', 'Οστεοαρθρίτιδα',
        'Διαβήτης', 'Παχυσαρκία', 'Προβλήματα θυρεοειδούς', 'Νεφρικές παθήσεις',
        'Ηπατικές παθήσεις', 'Αναπνευστικά προβλήματα', 'Γαστρεντερικές διαταραχές',
        'Όγκοι/Καρκίνος', 'Τραυματισμοί από ατυχήματα', 'Χειρουργικές επεμβάσεις'
    ]
    
    context = {
        'pet_type': pet_type,
        'gender': gender,
        'birthdate': birthdate,
        'breed': breed,
        'name': name,
        'conditions': dog_conditions
    }
    return render(request, 'main/dog_health_conditions.html', context)

def cat_health_conditions(request):
    """Cat health conditions selection page"""
    pet_type = request.GET.get('type', 'pet')
    gender = request.GET.get('gender', '')
    birthdate = request.GET.get('birthdate', '')
    breed = request.GET.get('breed', '')
    name = request.GET.get('name', '')
    
    # Common cat health conditions
    cat_conditions = [
        'Χρόνια νεφρική ανεπάρκεια', 'Υπερθυρεοειδισμός', 'Διαβήτης', 'Καρδιακές παθήσεις',
        'Ουρολιθίαση', 'Κυστίτιδα', 'Αλλεργίες δέρματος', 'Οδοντικά προβλήματα',
        'Αναπνευστικές λοιμώξεις', 'Γαστρεντερικές διαταραχές', 'Παχυσαρκία',
        'Οφθαλμικά προβλήματα', 'Όγκοι/Καρκίνος', 'Ιογενείς λοιμώξεις (FIV, FeLV)',
        'Παρασιτώσεις', 'Τραυματισμοί από πτώσεις', 'Χειρουργικές επεμβάσεις'
    ]
    
    context = {
        'pet_type': pet_type,
        'gender': gender,
        'birthdate': birthdate,
        'breed': breed,
        'name': name,
        'conditions': cat_conditions
    }
    return render(request, 'main/cat_health_conditions.html', context)

def insurance_choice(request):
    """Insurance choice page - get insured now or contact later"""
    pet_type = request.GET.get('type', '')
    gender = request.GET.get('gender', '')
    birthdate = request.GET.get('birthdate', '')
    breed = request.GET.get('breed', '')
    name = request.GET.get('name', '')
    health_status = request.GET.get('health_status', '')
    
    context = {
        'pet_type': pet_type,
        'gender': gender,
        'birthdate': birthdate,
        'breed': breed,
        'name': name,
        'health_status': health_status,
    }
    
    return render(request, 'main/insurance_choice.html', context)

def review_info(request):
    """Review page showing all entered information"""
    pet_type = request.GET.get('type', '')
    gender = request.GET.get('gender', '')
    birthdate = request.GET.get('birthdate', '')
    breed = request.GET.get('breed', '')
    name = request.GET.get('name', '')
    health_status = request.GET.get('health_status', '')
    conditions = request.GET.get('conditions', '')
    
    context = {
        'pet_type': pet_type,
        'gender': gender,
        'birthdate': birthdate,
        'breed': breed,
        'name': name,
        'health_status': health_status,
        'conditions': conditions,
    }
    
    return render(request, 'main/review_info.html', context)

def insurance_programs(request):
    """Insurance programs selection page"""
    pet_type = request.GET.get('type', '')
    gender = request.GET.get('gender', '')
    birthdate = request.GET.get('birthdate', '')
    breed = request.GET.get('breed', '')
    name = request.GET.get('name', '')
    health_status = request.GET.get('health_status', '')
    conditions = request.GET.get('conditions', '')
    is_healthy = request.GET.get('is_healthy', '')  # Get is_healthy from questionnaire
    
    context = {
        'pet_type': pet_type,
        'gender': gender,
        'birthdate': birthdate,
        'breed': breed,
        'name': name,
        'health_status': health_status,
        'conditions': conditions,
        'is_healthy': is_healthy,  # Pass to template
    }
    
    return render(request, 'main/insurance_programs.html', context)

def non_covered(request):
    """Non-covered conditions transparency page"""
    pet_type = request.GET.get('type', '')
    gender = request.GET.get('gender', '')
    birthdate = request.GET.get('birthdate', '')
    breed = request.GET.get('breed', '')
    name = request.GET.get('name', '')
    health_status = request.GET.get('health_status', '')
    conditions = request.GET.get('conditions', '')
    program = request.GET.get('program', '')
    is_healthy = request.GET.get('is_healthy', '')  # Get is_healthy from questionnaire
    
    context = {
        'pet_type': pet_type,
        'gender': gender,
        'birthdate': birthdate,
        'breed': breed,
        'name': name,
        'health_status': health_status,
        'conditions': conditions,
        'program': program,
        'is_healthy': is_healthy,  # Pass to template for auto-routing
    }
    
    return render(request, 'main/non_covered.html', context)

def user_data(request):
    """User data collection page with pricing calculation"""
    from .models import InsuranceApplication
    from datetime import datetime
    
    pet_type = request.GET.get('type', '')
    gender = request.GET.get('gender', '')
    birthdate = request.GET.get('birthdate', '')
    breed = request.GET.get('breed', '')
    name = request.GET.get('name', '')
    health_status = request.GET.get('health_status', '')
    conditions = request.GET.get('conditions', '')
    program = request.GET.get('program', '')
    
    # Second pet data (if exists)
    second_pet_type = request.GET.get('second_pet_type', '')
    second_pet_gender = request.GET.get('second_pet_gender', '')
    second_pet_birthdate = request.GET.get('second_pet_birthdate', '')
    second_pet_breed = request.GET.get('second_pet_breed', '')
    second_pet_name = request.GET.get('second_pet_name', '')
    second_pet_health_status = request.GET.get('second_pet_health_status', '')
    second_pet_conditions = request.GET.get('second_pet_conditions', '')
    second_pet_program = request.GET.get('second_pet_program', '')
    
    # User data (for pre-filling form)
    user_full_name = request.GET.get('fullName', '')
    user_afm = request.GET.get('afm', '')
    user_phone = request.GET.get('phone', '')
    user_address = request.GET.get('address', '')
    user_postal_code = request.GET.get('postalCode', '')
    user_email = request.GET.get('email', '')
    user_microchip = request.GET.get('microchip', '')
    
    # Check for second pet health issue message
    second_pet_health_issue = request.GET.get('second_pet_health_issue', '') == 'true'
    
    # Pricing tables - using EXACT values from original table
    DOG_PRICING = {
        'silver': {
            '10': {'final': 166.75, 'six_month': 87.54, 'three_month': 45.86, 'second_pet': 300.15, 'second_pet_6m': 157.58, 'second_pet_3m': 82.54},
            '11-20': {'final': 207.20, 'six_month': 108.78, 'three_month': 56.98, 'second_pet': 372.96, 'second_pet_6m': 195.80, 'second_pet_3m': 102.56},
            '21-40': {'final': 234.14, 'six_month': 122.92, 'three_month': 64.39, 'second_pet': 421.45, 'second_pet_6m': 221.26, 'second_pet_3m': 115.90},
            '>40': {'final': 254.36, 'six_month': 133.54, 'three_month': 69.95, 'second_pet': 457.84, 'second_pet_6m': 240.37, 'second_pet_3m': 125.91}
        },
        'gold': {
            '10': {'final': 234.14, 'six_month': 122.92, 'three_month': 64.39, 'second_pet': 421.45, 'second_pet_6m': 221.26, 'second_pet_3m': 115.90},
            '11-20': {'final': 261.09, 'six_month': 137.07, 'three_month': 71.80, 'second_pet': 469.96, 'second_pet_6m': 246.73, 'second_pet_3m': 129.24},
            '21-40': {'final': 288.05, 'six_month': 151.23, 'three_month': 79.21, 'second_pet': 518.50, 'second_pet_6m': 272.21, 'second_pet_3m': 142.59},
            '>40': {'final': 308.26, 'six_month': 161.84, 'three_month': 84.77, 'second_pet': 554.88, 'second_pet_6m': 291.31, 'second_pet_3m': 152.59}
        },
        'platinum': {
            '10': {'final': 368.92, 'six_month': 193.69, 'three_month': 101.45, 'second_pet': 664.06, 'second_pet_6m': 348.63, 'second_pet_3m': 182.62},
            '11-20': {'final': 389.15, 'six_month': 204.30, 'three_month': 107.02, 'second_pet': 700.47, 'second_pet_6m': 367.75, 'second_pet_3m': 192.63},
            '21-40': {'final': 409.36, 'six_month': 214.91, 'three_month': 112.57, 'second_pet': 736.85, 'second_pet_6m': 386.85, 'second_pet_3m': 202.63},
            '>40': {'final': 436.32, 'six_month': 229.07, 'three_month': 119.99, 'second_pet': 785.38, 'second_pet_6m': 412.33, 'second_pet_3m': 215.98}
        }
    }
    
    CAT_PRICING = {
        'silver': {
            '10': {'final': 113.81, 'six_month': 59.75, 'three_month': 31.30, 'second_pet': 204.85, 'second_pet_6m': 107.55, 'second_pet_3m': 56.33},
            '11-20': {'final': 141.02, 'six_month': 74.03, 'three_month': 38.78, 'second_pet': 253.83, 'second_pet_6m': 133.26, 'second_pet_3m': 69.80}
        },
        'gold': {
            '10': {'final': 168.22, 'six_month': 88.32, 'three_month': 46.26, 'second_pet': 302.80, 'second_pet_6m': 158.97, 'second_pet_3m': 83.27},
            '11-20': {'final': 188.61, 'six_month': 99.02, 'three_month': 51.87, 'second_pet': 339.50, 'second_pet_6m': 178.24, 'second_pet_3m': 93.36}
        },
        'platinum': {
            '10': {'final': 277.02, 'six_month': 145.44, 'three_month': 76.18, 'second_pet': 498.64, 'second_pet_6m': 261.79, 'second_pet_3m': 137.13},
            '11-20': {'final': 311.02, 'six_month': 163.28, 'three_month': 85.53, 'second_pet': 559.83, 'second_pet_6m': 293.91, 'second_pet_3m': 153.95}
        }
    }
    
    # Extract weight from breed string (e.g., "Λαμπραντόρ (έως 10 κιλά)")
    weight_category = None
    if breed:
        if 'έως 10 κιλά' in breed:
            weight_category = '10'
        elif '11-20 κιλά' in breed:
            weight_category = '11-20'
        elif '21-40 κιλά' in breed:
            weight_category = '21-40'
        elif '>40 κιλά' in breed:
            weight_category = '>40'
    
    # Calculate pricing
    pricing_data = None
    if pet_type and program and weight_category:
        if pet_type == 'dog' and program in DOG_PRICING and weight_category in DOG_PRICING[program]:
            pricing_data = DOG_PRICING[program][weight_category]
        elif pet_type == 'cat' and program in CAT_PRICING and weight_category in CAT_PRICING[program]:
            pricing_data = CAT_PRICING[program][weight_category]
    
    # Calculate second pet pricing if exists
    second_pet_pricing_data = None
    second_pet_weight_category = None
    if second_pet_breed:
        if 'έως 10 κιλά' in second_pet_breed:
            second_pet_weight_category = '10'
        elif '11-20 κιλά' in second_pet_breed:
            second_pet_weight_category = '11-20'
        elif '21-40 κιλά' in second_pet_breed:
            second_pet_weight_category = '21-40'
        elif '>40 κιλά' in second_pet_breed:
            second_pet_weight_category = '>40'
        
        if second_pet_type and second_pet_program and second_pet_weight_category:
            if second_pet_type == 'dog' and second_pet_program in DOG_PRICING and second_pet_weight_category in DOG_PRICING[second_pet_program]:
                second_pet_pricing_data = DOG_PRICING[second_pet_program][second_pet_weight_category]
            elif second_pet_type == 'cat' and second_pet_program in CAT_PRICING and second_pet_weight_category in CAT_PRICING[second_pet_program]:
                second_pet_pricing_data = CAT_PRICING[second_pet_program][second_pet_weight_category]

    context = {
        'pet_type': pet_type,
        'gender': gender,
        'birthdate': birthdate,
        'breed': breed,
        'name': name,
        'health_status': health_status,
        'conditions': conditions,
        'program': program,
        'weight_category': weight_category,
        'pricing_data': pricing_data,
        
        # Second pet data
        'second_pet_type': second_pet_type,
        'second_pet_gender': second_pet_gender,
        'second_pet_birthdate': second_pet_birthdate,
        'second_pet_breed': second_pet_breed,
        'second_pet_name': second_pet_name,
        'second_pet_health_status': second_pet_health_status,
        'second_pet_conditions': second_pet_conditions,
        'second_pet_program': second_pet_program,
        'second_pet_weight_category': second_pet_weight_category,
        'second_pet_pricing_data': second_pet_pricing_data,
        
        # User data for pre-filling
        'user_full_name': user_full_name,
        'user_afm': user_afm,
        'user_phone': user_phone,
        'user_address': user_address,
        'user_postal_code': user_postal_code,
        'user_email': user_email,
        'user_microchip': user_microchip,
        
        # Messages
        'second_pet_health_issue': second_pet_health_issue,
    }
    
    # Handle form submission
    if request.method == 'POST':
        return handle_application_submission(request)
    
    # Render old user_data template (keep for now, but questionnaire is at health-status)
    return render(request, 'main/user_data.html', context)

def handle_application_submission(request):
    """Handle insurance application form submission"""
    from .models import InsuranceApplication
    from datetime import datetime
    from django.http import JsonResponse
    
    try:
        # Parse birthdate
        pet_birthdate = None
        if request.POST.get('birthdate'):
            try:
                pet_birthdate = datetime.strptime(request.POST.get('birthdate'), '%Y-%m-%d').date()
            except ValueError:
                pass
        
        # Parse second pet birthdate
        second_pet_birthdate = None
        if request.POST.get('secondPetBirthdate'):
            try:
                second_pet_birthdate = datetime.strptime(request.POST.get('secondPetBirthdate'), '%Y-%m-%d').date()
            except ValueError:
                pass
        
        # Calculate base premium
        base_premium = calculate_total_premium(request.POST)
        
        # Check for affiliate code and apply discount
        affiliate_code_str = request.POST.get('affiliateCode', '').strip().upper()
        discount_applied = 0
        affiliate_code_obj = None
        
        if affiliate_code_str:
            from .models import AmbassadorCode
            try:
                affiliate_code_obj = AmbassadorCode.objects.get(code=affiliate_code_str)
                if affiliate_code_obj.is_valid():
                    # Apply discount
                    final_amount, discount = affiliate_code_obj.apply_discount(float(base_premium))
                    discount_applied = discount
                    base_premium = final_amount
                    # Increment usage counter
                    affiliate_code_obj.increment_usage()
            except AmbassadorCode.DoesNotExist:
                pass  # Code not found, proceed without discount
        
        # Create application
        application = InsuranceApplication.objects.create(
            # User information
            full_name=request.POST.get('fullName', ''),
            afm=request.POST.get('afm', ''),
            phone=request.POST.get('phone', ''),
            address=request.POST.get('address', ''),
            postal_code=request.POST.get('postalCode', ''),
            email=request.POST.get('email', ''),
            
            # Pet information
            pet_name=request.POST.get('name', ''),
            pet_type=request.POST.get('type', ''),
            pet_gender=request.POST.get('gender', ''),
            pet_breed=request.POST.get('breed', ''),
            pet_birthdate=pet_birthdate,
            pet_weight_category=extract_weight_from_breed(request.POST.get('breed', '')),
            microchip_number=request.POST.get('microchip', ''),
            
            # Second pet information
            has_second_pet=bool(request.POST.get('secondPetName')),
            second_pet_name=request.POST.get('secondPetName', ''),
            second_pet_type=request.POST.get('secondPetType', ''),
            second_pet_gender=request.POST.get('secondPetGender', ''),
            second_pet_breed=request.POST.get('secondPetBreed', ''),
            second_pet_birthdate=second_pet_birthdate,
            second_pet_weight_category=request.POST.get('secondPetWeight', ''),
            
            # Insurance details
            program=request.POST.get('program', ''),
            health_status=request.POST.get('health_status', ''),
            health_conditions=request.POST.get('conditions', ''),
            second_pet_health_status=request.POST.get('secondPetHealth', ''),
            
            # Pricing (with discount applied if code was used)
            annual_premium=base_premium,
            affiliate_code=affiliate_code_str if affiliate_code_str else None,
            discount_applied=discount_applied,
            
            # Status
            status='submitted'
        )
        
        # Create and save questionnaire
        # Get questionnaire data from session (stored when questionnaire was submitted) or from POST
        try:
            from .models import Questionnaire
            from datetime import datetime
            
            # Get questionnaire data from session or POST
            questionnaire_data = {}
            if 'questionnaire_data' in request.session:
                # Get from session (stored when questionnaire was submitted)
                session_data = request.session['questionnaire_data']
                # Convert QueryDict-like structure to regular dict
                for key, value in session_data.items():
                    if isinstance(value, list) and len(value) > 0:
                        questionnaire_data[key] = value[0]  # Get first value from list
                    else:
                        questionnaire_data[key] = value
            else:
                # Fallback to POST data (for backwards compatibility)
                # Django QueryDict needs special handling
                for key in request.POST.keys():
                    values = request.POST.getlist(key)
                    if len(values) == 1:
                        questionnaire_data[key] = values[0]
                    else:
                        questionnaire_data[key] = values
            
            # Helper function to safely get boolean value
            def get_bool(key, default=False):
                val = questionnaire_data.get(key, '')
                if isinstance(val, list):
                    val = val[0] if val else ''
                return val == 'true' or val is True
            
            # Helper function to safely get string value
            def get_str(key, default=''):
                val = questionnaire_data.get(key, default)
                if isinstance(val, list):
                    val = val[0] if val else default
                return str(val) if val else default
            
            # Parse desired start date
            desired_start_date = None
            start_date_str = get_str('desired_start_date')
            if start_date_str:
                try:
                    desired_start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                except ValueError:
                    pass
            
            # Determine if it's a dog or cat to handle leishmaniasis question
            pet_type_val = request.POST.get('type', '') or get_str('type', '')
            is_dog = pet_type_val == 'dog'
            
            # Handle breed_type (purebred/mixed/crossbreed)
            breed_type = get_str('breed_type', '')
            is_purebred = breed_type == 'purebred'
            is_mixed = breed_type == 'mixed'
            is_crossbreed = breed_type == 'crossbreed'
            
            # Check if questionnaire already exists for this application
            questionnaire, created = Questionnaire.objects.get_or_create(
                application=application,
                defaults={
                    # Section 1.1
                    'has_other_insured_pet': get_bool('has_other_insured_pet'),
                    'has_been_denied_insurance': get_bool('has_been_denied_insurance'),
                    'has_special_terms_imposed': get_bool('has_special_terms_imposed'),
                    # Section 2
                    'pet_colors': get_str('pet_colors'),
                    'pet_weight': get_str('pet_weight'),
                    'is_purebred': is_purebred,
                    'is_mixed': is_mixed,
                    'is_crossbreed': is_crossbreed,
                    'pet_breed_or_crossbreed': get_str('pet_breed_or_crossbreed'),
                    # Section 2.1 (Dog specific)
                    'special_breed_5_percent': get_bool('special_breed_5_percent') if is_dog else False,
                    'special_breed_20_percent': get_bool('special_breed_20_percent') if is_dog else False,
                    # Section 2.2
                    'is_healthy': get_bool('is_healthy'),
                    'is_healthy_details': get_str('is_healthy_details'),
                    'has_injury_illness_3_years': get_bool('has_injury_illness_3_years'),
                    'has_injury_illness_details': get_str('has_injury_illness_3_years_details'),
                    'has_surgical_procedure': get_bool('has_surgical_procedure'),
                    'has_surgical_procedure_details': get_str('has_surgical_procedure_details'),
                    'has_examination_findings': get_bool('has_examination_findings'),
                    'has_examination_findings_details': get_str('has_examination_findings_details'),
                    'is_sterilized': get_bool('is_sterilized'),
                    # Leishmaniasis vaccination only for dogs (cats don't have this question)
                    'is_vaccinated_leishmaniasis': get_bool('is_vaccinated_leishmaniasis') if is_dog else False,
                    'follows_vaccination_program': get_bool('follows_vaccination_program'),
                    'follows_vaccination_program_details': get_str('follows_vaccination_program_details'),
                    'has_hereditary_disease': get_bool('has_hereditary_disease'),
                    'has_hereditary_disease_details': get_str('has_hereditary_disease_details'),
                    # Section 3
                    'program': get_str('program') or request.POST.get('program', ''),
                    'additional_poisoning_coverage': get_bool('additional_poisoning_coverage'),
                    'additional_blood_checkup': get_bool('additional_blood_checkup'),
                    # Section 4
                    'desired_start_date': desired_start_date,
                    # Section 5
                    'payment_method': get_str('payment_method'),
                    'payment_frequency': get_str('payment_frequency'),
                    # Section 6
                    'consent_terms_conditions': get_bool('consent_terms_conditions'),
                    'consent_info_document': get_bool('consent_info_document'),
                    'consent_email_notifications': get_bool('consent_email_notifications'),
                    'consent_marketing': get_bool('consent_marketing'),
                    'consent_data_processing': get_bool('consent_data_processing'),
                    'consent_pet_gov_platform': get_bool('consent_pet_gov_platform'),
                }
            )
            
            # If questionnaire already existed, update it
            if not created:
                questionnaire.has_other_insured_pet = get_bool('has_other_insured_pet')
                questionnaire.has_been_denied_insurance = get_bool('has_been_denied_insurance')
                questionnaire.has_special_terms_imposed = get_bool('has_special_terms_imposed')
                questionnaire.pet_colors = get_str('pet_colors')
                questionnaire.pet_weight = get_str('pet_weight')
                questionnaire.is_purebred = is_purebred
                questionnaire.is_mixed = is_mixed
                questionnaire.is_crossbreed = is_crossbreed
                questionnaire.pet_breed_or_crossbreed = get_str('pet_breed_or_crossbreed')
                questionnaire.special_breed_5_percent = get_bool('special_breed_5_percent') if is_dog else False
                questionnaire.special_breed_20_percent = get_bool('special_breed_20_percent') if is_dog else False
                questionnaire.is_healthy = get_bool('is_healthy')
                questionnaire.is_healthy_details = get_str('is_healthy_details')
                questionnaire.has_injury_illness_3_years = get_bool('has_injury_illness_3_years')
                questionnaire.has_injury_illness_details = get_str('has_injury_illness_3_years_details')
                questionnaire.has_surgical_procedure = get_bool('has_surgical_procedure')
                questionnaire.has_surgical_procedure_details = get_str('has_surgical_procedure_details')
                questionnaire.has_examination_findings = get_bool('has_examination_findings')
                questionnaire.has_examination_findings_details = get_str('has_examination_findings_details')
                questionnaire.is_sterilized = get_bool('is_sterilized')
                questionnaire.is_vaccinated_leishmaniasis = get_bool('is_vaccinated_leishmaniasis') if is_dog else False
                questionnaire.follows_vaccination_program = get_bool('follows_vaccination_program')
                questionnaire.follows_vaccination_program_details = get_str('follows_vaccination_program_details')
                questionnaire.has_hereditary_disease = get_bool('has_hereditary_disease')
                questionnaire.has_hereditary_disease_details = get_str('has_hereditary_disease_details')
                questionnaire.program = get_str('program') or request.POST.get('program', '')
                questionnaire.additional_poisoning_coverage = get_bool('additional_poisoning_coverage')
                questionnaire.additional_blood_checkup = get_bool('additional_blood_checkup')
                questionnaire.desired_start_date = desired_start_date
                questionnaire.payment_method = get_str('payment_method')
                questionnaire.payment_frequency = get_str('payment_frequency')
                questionnaire.consent_terms_conditions = get_bool('consent_terms_conditions')
                questionnaire.consent_info_document = get_bool('consent_info_document')
                questionnaire.consent_email_notifications = get_bool('consent_email_notifications')
                questionnaire.consent_marketing = get_bool('consent_marketing')
                questionnaire.consent_data_processing = get_bool('consent_data_processing')
                questionnaire.consent_pet_gov_platform = get_bool('consent_pet_gov_platform')
                questionnaire.save()
            
            # Clear questionnaire data from session after successful save
            if 'questionnaire_data' in request.session:
                del request.session['questionnaire_data']
                if 'questionnaire_submitted' in request.session:
                    del request.session['questionnaire_submitted']
            
            import logging
            logger = logging.getLogger(__name__)
            logger.info(f"Questionnaire {'created' if created else 'updated'} successfully for application {application.id} (Questionnaire ID: {questionnaire.id})")
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"CRITICAL: Error creating/updating questionnaire for application {application.id}: {e}")
            import traceback
            logger.error(traceback.format_exc())
            # Re-raise the exception so we know questionnaires are failing
            raise
        
        # Link uploaded documents to this application
        try:
            from .models import PetDocument
            pet_name = request.POST.get('name', '')
            pet_type = request.POST.get('type', '')
            
            # Find documents uploaded for this pet (before application was created)
            PetDocument.objects.filter(
                application__isnull=True,
                pet_name=pet_name,
                pet_type=pet_type
            ).update(application=application)
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Could not link documents to application {application.id}: {e}")
        
        # Link uploaded photos to this application
        try:
            from .models import PetPhoto
            pet_name = request.POST.get('name', '')
            pet_type = request.POST.get('type', '')
            
            # Find photos uploaded for this pet (before application was created)
            PetPhoto.objects.filter(
                application__isnull=True,
                pet_name=pet_name,
                pet_type=pet_type
            ).update(application=application)
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Could not link photos to application {application.id}: {e}")
        
        # Generate and store contract PDF (contains all application data for admin access)
        try:
            from .utils import generate_contract_pdf
            pdf_paths = generate_contract_pdf(application)
            if pdf_paths:
                # Store the first PDF (or the only one) - this contains all application data
                application.contract_pdf_path = pdf_paths[0] if isinstance(pdf_paths, list) else pdf_paths
                application.contract_generated = True
                application.save()
        except Exception as e:
            # Log error but don't fail the submission
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error generating PDF for application {application.id}: {e}")
        
        # Send notification emails
        try:
            from .email_utils import send_application_notification_emails
            send_application_notification_emails(application)
        except Exception as e:
            # Log error but don't fail the submission
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error sending emails for application {application.id}: {e}")
        
        # Redirect to thank you page for all applications
        # Get is_healthy from questionnaire for passing through URL
        is_healthy_value = request.POST.get('is_healthy', '')
        
        return JsonResponse({
            'success': True,
            'message': 'Η αίτησή σας υποβλήθηκε επιτυχώς!',
            'application_number': application.application_number,
            'application_id': application.id,
            'redirect_url': f'/thank-you/?application_id={application.id}',
            'is_healthy': is_healthy_value  # Pass is_healthy for potential use in other flows
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Σφάλμα κατά την υποβολή: {str(e)}'
        })

def extract_weight_from_breed(breed):
    """Extract weight category from breed string"""
    if not breed:
        return ''
    
    if 'έως 10 κιλά' in breed:
        return '10'
    elif '11-20 κιλά' in breed:
        return '11-20'
    elif '21-40 κιλά' in breed:
        return '21-40'
    elif '>40 κιλά' in breed:
        return '>40'
    
    return ''

def calculate_total_premium(post_data):
    """Calculate total premium based on submitted data"""
    # This would use the same pricing logic as in the frontend
    # For now, return a placeholder
    return 389.15

def application_processing(request):
    """Application processing page for pets with health issues"""
    application_id = request.GET.get('application_id')
    
    try:
        from .models import InsuranceApplication
        application = InsuranceApplication.objects.get(id=application_id)
        
        context = {
            'application': application,
            'application_number': application.application_number or f'HPI{10000 + application.id}',
            'pet_name': application.pet_name,
            'has_second_pet': application.has_second_pet,
            'second_pet_name': application.second_pet_name if application.has_second_pet else None
        }
        
        return render(request, 'main/application_processing.html', context)
    except InsuranceApplication.DoesNotExist:
        return render(request, 'main/application_processing.html', {
            'error': 'Η αίτηση δεν βρέθηκε'
        })

def contact_info(request):
    """Contact information collection page"""
    pet_type = request.GET.get('type', '')
    gender = request.GET.get('gender', '')
    birthdate = request.GET.get('birthdate', '')
    breed = request.GET.get('breed', '')
    name = request.GET.get('name', '')
    health_status = request.GET.get('health_status', '')
    conditions = request.GET.get('conditions', '')
    
    context = {
        'pet_type': pet_type,
        'gender': gender,
        'birthdate': birthdate,
        'breed': breed,
        'name': name,
        'health_status': health_status,
        'conditions': conditions,
    }
    
    return render(request, 'main/contact_info.html', context)

def thank_you(request):
    """Final thank you page with application details"""
    application_id = request.GET.get('application_id')
    application = None
    
    if application_id:
        try:
            from .models import InsuranceApplication
            application = InsuranceApplication.objects.get(id=application_id)
        except InsuranceApplication.DoesNotExist:
            pass
    
    context = {
        'application': application,
        'application_number': application.application_number if application else None,
        'pet_name': application.pet_name if application else '',
        'pet_type': application.pet_type if application else '',
        'email': application.email if application else '',
        'full_name': application.full_name if application else '',
    }
    
    return render(request, 'main/thank_you.html', context)


@csrf_exempt
@require_http_methods(["POST"])
def validate_affiliate_code(request):
    """API endpoint to validate affiliate/ambassador/partner codes"""
    from .models import AmbassadorCode
    import json
    
    try:
        data = json.loads(request.body)
        code = data.get('code', '').strip().upper()
        
        if not code:
            return JsonResponse({
                'success': False,
                'error': 'Παρακαλώ εισάγετε έναν κωδικό.'
            }, status=400)
        
        # Find the code
        try:
            ambassador_code = AmbassadorCode.objects.get(code=code)
        except AmbassadorCode.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Ο κωδικός δεν βρέθηκε. Παρακαλώ ελέγξτε τον κωδικό και δοκιμάστε ξανά.'
            }, status=404)
        
        # Validate the code
        if not ambassador_code.is_valid():
            if not ambassador_code.is_active:
                error_msg = 'Ο κωδικός δεν είναι ενεργός.'
            elif ambassador_code.max_uses and ambassador_code.current_uses >= ambassador_code.max_uses:
                error_msg = 'Ο κωδικός έχει εξαντληθεί.'
            else:
                error_msg = 'Ο κωδικός δεν είναι έγκυρος για αυτή την περίοδο.'
            
            return JsonResponse({
                'success': False,
                'error': error_msg
            }, status=400)
        
        # Return success with code details
        discount_info = {}
        if ambassador_code.discount_percentage > 0:
            discount_info['type'] = 'percentage'
            discount_info['value'] = float(ambassador_code.discount_percentage)
            discount_info['description'] = f'{ambassador_code.discount_percentage}% έκπτωση'
        elif ambassador_code.discount_amount > 0:
            discount_info['type'] = 'fixed'
            discount_info['value'] = float(ambassador_code.discount_amount)
            discount_info['description'] = f'{ambassador_code.discount_amount}€ έκπτωση'
        
        if ambassador_code.max_discount:
            discount_info['max_discount'] = float(ambassador_code.max_discount)
        
        return JsonResponse({
            'success': True,
            'code': ambassador_code.code,
            'code_type': ambassador_code.get_code_type_display(),
            'name': ambassador_code.name,
            'description': ambassador_code.description,
            'discount': discount_info,
            'message': f'✓ Κωδικός "{ambassador_code.code}" εφαρμόστηκε επιτυχώς!'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Μη έγκυρο αίτημα.'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Σφάλμα: {str(e)}'
        }, status=500)

def serve_file(request, file_type, file_id):
    """Serve files from S3 or local storage through Django"""
    try:
        if file_type == 'photo':
            from .models import PetPhoto
            file_obj = get_object_or_404(PetPhoto, id=file_id)
        elif file_type == 'document':
            from .models import PetDocument
            file_obj = get_object_or_404(PetDocument, id=file_id)
        else:
            raise Http404("Invalid file type")
        
        if not file_obj.file:
            raise Http404("File not found")
        
        # Check if file exists in storage
        if not default_storage.exists(file_obj.file.name):
            raise Http404("File not found in storage")
        
        # Open and serve the file
        file = default_storage.open(file_obj.file.name, 'rb')
        response = FileResponse(file, content_type=file_obj.file_type)
        response['Content-Disposition'] = f'inline; filename="{file_obj.original_filename}"'
        return response
        
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error serving file {file_type}/{file_id}: {str(e)}")
        raise Http404("File not found")