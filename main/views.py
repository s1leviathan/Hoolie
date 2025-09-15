from django.shortcuts import render

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

def health_status(request):
    """Pet health status page"""
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
    return render(request, 'main/health_status.html', context)

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
    
    context = {
        'pet_type': pet_type,
        'gender': gender,
        'birthdate': birthdate,
        'breed': breed,
        'name': name,
        'health_status': health_status,
        'conditions': conditions,
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
    
    context = {
        'pet_type': pet_type,
        'gender': gender,
        'birthdate': birthdate,
        'breed': breed,
        'name': name,
        'health_status': health_status,
        'conditions': conditions,
        'program': program,
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
            
            # Pricing (would be calculated based on the program and pets)
            annual_premium=calculate_total_premium(request.POST),
            
            # Status
            status='submitted'
        )
        
        # Return success response
        return JsonResponse({
            'success': True,
            'message': 'Η αίτησή σας υποβλήθηκε επιτυχώς!',
            'contract_number': application.contract_number,
            'redirect_url': f'/contact/?application_id={application.id}'
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
    """Final thank you page"""
    pet_type = request.GET.get('type', '')
    name = request.GET.get('name', '')
    email = request.GET.get('email', '')
    
    context = {
        'pet_type': pet_type,
        'name': name,
        'email': email,
    }
    
    return render(request, 'main/thank_you.html', context)