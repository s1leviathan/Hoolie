from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, FileResponse, Http404, HttpResponse
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

def pet_breed(request):
    """Dog breed selection page"""
    pet_type = request.GET.get('type', 'dog')
    gender = request.GET.get('gender', '')
    
    # Common dog breeds for dropdown (20 breeds)
    dog_breeds = [
        'Λαμπραντόρ', 'Γκόλντεν Ρετρίβερ', 'Γερμανικός Ποιμενικός', 'Μπουλντόγκ',
        'Πούντλ', 'Μπίγκλ', 'Ρότβαϊλερ', 'Γιόρκσαϊρ Τέριερ',
        'Ντάξχουντ', 'Σιμπέριαν Χάσκι', 'Πομερανιάν', 'Σιτσού',
        'Μπόξερ', 'Τσιουάουα', 'Μαλτέζ', 'Κοκέρ Σπάνιελ',
        'Μπορντέρ Κόλι', 'Φρέντς Μπουλντόγκ', 'Αυστραλιανός Ποιμενικός', 'Μπασέτ Χάουντ'
    ]
    
    context = {
        'pet_type': pet_type,
        'gender': gender,
        'breeds': dog_breeds
    }
    return render(request, 'main/pet_breed.html', context)

def cat_breed(request):
    """Cat breed selection page"""
    pet_type = request.GET.get('type', 'cat')
    gender = request.GET.get('gender', '')
    
    # Common cat breeds for dropdown (20 breeds)
    cat_breeds = [
        'Περσική', 'Μέιν Κουν', 'Σιαμέζα', 'Ραγκντόλ',
        'Βρετανική Κοντότριχη', 'Αμπισίνια', 'Ρωσική Μπλε', 'Σκωτσέζικη Πτυχωτή',
        'Σφίγκα', 'Βεγγαλική', 'Μάνξ', 'Νορβηγική Δασική',
        'Τούρκικη Αγκυρα', 'Αμερικανική Κοντότριχη', 'Εξωτική Κοντότριχη', 'Ορμιέντλ',
        'Σομαλί', 'Τονκινέζα', 'Μπομπέι', 'Κορνίς Ρεξ'
    ]
    
    context = {
        'pet_type': pet_type,
        'gender': gender,
        'breeds': cat_breeds
    }
    return render(request, 'main/cat_breed.html', context)

def pet_name(request):
    """Pet name input page"""
    pet_type = request.GET.get('type', '')
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

def cat_name(request):
    """Cat name input page"""
    pet_type = request.GET.get('type', '')
    gender = request.GET.get('gender', '')
    birthdate = request.GET.get('birthdate', '')
    breed = request.GET.get('breed', '')
    
    context = {
        'pet_type': pet_type,
        'gender': gender,
        'birthdate': birthdate,
        'breed': breed
    }
    return render(request, 'main/cat_name.html', context)

def pet_birthdate(request):
    """Pet birthdate input page"""
    pet_type = request.GET.get('type', '')
    gender = request.GET.get('gender', '')
    
    context = {
        'pet_type': pet_type,
        'gender': gender
    }
    return render(request, 'main/pet_birthdate.html', context)

def health_status(request):
    """Health status selection page - now shows questionnaire"""
    pet_type = request.GET.get('type', '')
    gender = request.GET.get('gender', '')
    birthdate = request.GET.get('birthdate', '')
    breed = request.GET.get('breed', '')
    name = request.GET.get('name', '')
    
    if request.method == 'POST':
        # Store questionnaire data in session
        from django.http import JsonResponse
        import logging
        
        logger = logging.getLogger(__name__)
        
        try:
            # Get all POST data
            questionnaire_data = {}
            for key in request.POST.keys():
                values = request.POST.getlist(key)
                if len(values) == 1:
                    questionnaire_data[key] = values[0]
                else:
                    questionnaire_data[key] = values
            
            # Store in session
            request.session['questionnaire_data'] = questionnaire_data
            request.session['questionnaire_submitted'] = True
            request.session.modified = True
            
            logger.info(f"Questionnaire data stored in session: {list(questionnaire_data.keys())}")
            
            return JsonResponse({
                'success': True,
                'message': 'Questionnaire submitted successfully'
            })
        except Exception as e:
            logger.error(f"Error storing questionnaire data: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return JsonResponse({
                'success': False,
                'message': f'Error: {str(e)}'
            })
    
    context = {
        'pet_type': pet_type,
        'gender': gender,
        'birthdate': birthdate,
        'breed': breed,
        'name': name
    }
    
    # Render appropriate questionnaire template
    if pet_type == 'dog':
        return render(request, 'main/questionnaire_dog.html', context)
    else:
        return render(request, 'main/questionnaire_cat.html', context)

def insurance_programs(request):
    """Insurance program selection page"""
    pet_type = request.GET.get('type', '')
    gender = request.GET.get('gender', '')
    birthdate = request.GET.get('birthdate', '')
    breed = request.GET.get('breed', '')
    name = request.GET.get('name', '')
    is_healthy = request.GET.get('is_healthy', '')
    
    context = {
        'pet_type': pet_type,
        'gender': gender,
        'birthdate': birthdate,
        'breed': breed,
        'name': name,
        'is_healthy': is_healthy
    }
    return render(request, 'main/insurance_programs.html', context)

def non_covered(request):
    """Non-covered conditions page"""
    pet_type = request.GET.get('type', '')
    gender = request.GET.get('gender', '')
    birthdate = request.GET.get('birthdate', '')
    breed = request.GET.get('breed', '')
    name = request.GET.get('name', '')
    is_healthy = request.GET.get('is_healthy', '')
    
    context = {
        'pet_type': pet_type,
        'gender': gender,
        'birthdate': birthdate,
        'breed': breed,
        'name': name,
        'is_healthy': is_healthy
    }
    return render(request, 'main/non_covered.html', context)

def dog_health_conditions(request):
    """Dog health conditions page for underwriting"""
    pet_type = request.GET.get('type', '')
    gender = request.GET.get('gender', '')
    birthdate = request.GET.get('birthdate', '')
    breed = request.GET.get('breed', '')
    name = request.GET.get('name', '')
    
    # List of dog health conditions
    conditions = [
        'Δυσπλασία ισχίου',
        'Δυσπλασία αγκώνα',
        'Καταρράκτης',
        'Γλαύκωμα',
        'Καρδιακές παθήσεις',
        'Επιληψία',
        'Αλλεργίες δέρματος',
        'Οστεοαρθρίτιδα',
        'Διαβήτης',
        'Παχυσαρκία',
        'Προβλήματα θυρεοειδούς',
        'Νεφρικές παθήσεις',
        'Ηπατικές παθήσεις',
        'Αναπνευστικά προβλήματα',
        'Γαστρεντερικές διαταραχές',
        'Όγκοι/Καρκίνος',
        'Τραυματισμοί από ατυχήματα',
        'Χειρουργικές επεμβάσεις'
    ]
    
    context = {
        'pet_type': pet_type,
        'gender': gender,
        'birthdate': birthdate,
        'breed': breed,
        'name': name,
        'conditions': conditions
    }
    return render(request, 'main/dog_health_conditions.html', context)

def cat_health_conditions(request):
    """Cat health conditions page for underwriting"""
    pet_type = request.GET.get('type', '')
    gender = request.GET.get('gender', '')
    birthdate = request.GET.get('birthdate', '')
    breed = request.GET.get('breed', '')
    name = request.GET.get('name', '')
    
    # List of cat health conditions
    conditions = [
        'Καταρράκτης',
        'Γλαύκωμα',
        'Καρδιακές παθήσεις',
        'Αλλεργίες δέρματος',
        'Διαβήτης',
        'Παχυσαρκία',
        'Προβλήματα θυρεοειδούς',
        'Νεφρικές παθήσεις',
        'Ηπατικές παθήσεις',
        'Αναπνευστικά προβλήματα',
        'Γαστρεντερικές διαταραχές',
        'Όγκοι/Καρκίνος',
        'Τραυματισμοί από ατυχήματα',
        'Χειρουργικές επεμβάσεις',
        'FIV (Feline Immunodeficiency Virus)',
        'FeLV (Feline Leukemia Virus)',
        'FIP (Feline Infectious Peritonitis)',
        'Προβλήματα ουροποιητικού συστήματος'
    ]
    
    context = {
        'pet_type': pet_type,
        'gender': gender,
        'birthdate': birthdate,
        'breed': breed,
        'name': name,
        'conditions': conditions
    }
    return render(request, 'main/cat_health_conditions.html', context)

def user_data(request):
    """User data and pricing page"""
    pet_type = request.GET.get('type', '')
    gender = request.GET.get('gender', '')
    birthdate = request.GET.get('birthdate', '')
    breed = request.GET.get('breed', '')
    name = request.GET.get('name', '')
    second_pet_name = request.GET.get('secondPetName', '')
    second_pet_type = request.GET.get('secondPetType', '')
    second_pet_gender = request.GET.get('secondPetGender', '')
    second_pet_birthdate = request.GET.get('secondPetBirthdate', '')
    second_pet_breed = request.GET.get('second_pet_breed', '')
    
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
    
    # Extract weight for second pet
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
        
    # Pricing tables (MUST match frontend JavaScript exactly)
    DOG_PRICING = {
        'silver': {
            '10': {'annual': 166.75, 'six_month': 87.54, 'three_month': 45.86},
            '11-20': {'annual': 207.20, 'six_month': 108.78, 'three_month': 56.98},
            '21-40': {'annual': 234.14, 'six_month': 122.92, 'three_month': 64.39},
            '>40': {'annual': 254.36, 'six_month': 133.54, 'three_month': 69.95}
        },
        'gold': {
            '10': {'annual': 234.14, 'six_month': 122.92, 'three_month': 64.39},
            '11-20': {'annual': 261.09, 'six_month': 137.07, 'three_month': 71.80},
            '21-40': {'annual': 288.05, 'six_month': 151.23, 'three_month': 79.21},
            '>40': {'annual': 308.26, 'six_month': 161.84, 'three_month': 84.77}
        },
        'platinum': {
            '10': {'annual': 368.92, 'six_month': 193.69, 'three_month': 101.45},
            '11-20': {'annual': 389.15, 'six_month': 204.30, 'three_month': 107.02},
            '21-40': {'annual': 409.36, 'six_month': 214.91, 'three_month': 112.57},
            '>40': {'annual': 436.32, 'six_month': 229.07, 'three_month': 119.99}
        }
    }
    
    CAT_PRICING = {
        'silver': {
            '10': {'annual': 113.81, 'six_month': 59.75, 'three_month': 31.30},
            '11-20': {'annual': 141.02, 'six_month': 74.03, 'three_month': 38.78}
        },
        'gold': {
            '10': {'annual': 168.22, 'six_month': 88.32, 'three_month': 46.26},
            '11-20': {'annual': 188.61, 'six_month': 99.02, 'three_month': 51.87}
        },
        'platinum': {
            '10': {'annual': 277.02, 'six_month': 145.44, 'three_month': 76.18},
            '11-20': {'annual': 311.02, 'six_month': 163.28, 'three_month': 85.53}
        }
    }
    
    # Get program from URL or default to 'silver'
    program = request.GET.get('program', 'silver')
    second_pet_program = request.GET.get('secondPetProgram', 'silver')
    
    # Get pricing data
    pricing_data = None
    if pet_type == 'dog' and program in DOG_PRICING and weight_category in DOG_PRICING[program]:
        pricing_data = DOG_PRICING[program][weight_category].copy()
        # Add 'final' field for compatibility with JavaScript
        if 'annual' in pricing_data and 'final' not in pricing_data:
            pricing_data['final'] = pricing_data['annual']
    elif pet_type == 'cat' and program in CAT_PRICING and weight_category in CAT_PRICING[program]:
        pricing_data = CAT_PRICING[program][weight_category].copy()
        # Add 'final' field for compatibility with JavaScript
        if 'annual' in pricing_data and 'final' not in pricing_data:
            pricing_data['final'] = pricing_data['annual']
    
    # Get breed surcharges and add-ons from session (stored when questionnaire was submitted)
    special_breed_5_percent = False
    special_breed_20_percent = False
    additional_poisoning_coverage = False
    additional_blood_checkup = False
    
    # Check URL parameters first (for direct access)
    if request.GET.get('special_breed_5_percent') == 'true':
        special_breed_5_percent = True
    if request.GET.get('special_breed_20_percent') == 'true':
        special_breed_20_percent = True
    if request.GET.get('additional_poisoning_coverage') == 'true':
        additional_poisoning_coverage = True
    if request.GET.get('additional_blood_checkup') == 'true':
        additional_blood_checkup = True
    
    # Also check session data (stored when questionnaire was submitted)
    session_data = {}
    if 'questionnaire_data' in request.session:
        session_data = request.session['questionnaire_data']
        if isinstance(session_data, dict):
            # Check for breed surcharges
            session_5_percent = session_data.get('special_breed_5_percent')
            if session_5_percent:
                if isinstance(session_5_percent, list):
                    special_breed_5_percent = 'true' in session_5_percent or True in [v == 'true' for v in session_5_percent]
                else:
                    special_breed_5_percent = session_5_percent == 'true' or special_breed_5_percent
            
            session_20_percent = session_data.get('special_breed_20_percent')
            if session_20_percent:
                if isinstance(session_20_percent, list):
                    special_breed_20_percent = 'true' in session_20_percent or True in [v == 'true' for v in session_20_percent]
                else:
                    special_breed_20_percent = session_20_percent == 'true' or special_breed_20_percent
            
            # Check for add-ons
            session_poisoning = session_data.get('additional_poisoning_coverage')
            if session_poisoning:
                additional_poisoning_coverage = session_poisoning == 'true' or additional_poisoning_coverage
            
            session_blood = session_data.get('additional_blood_checkup')
            if session_blood:
                additional_blood_checkup = session_blood == 'true' or additional_blood_checkup
    
    # Calculate base price with breed surcharges
    base_price_breakdown = {
        'base_price': 0,
        'breed_surcharge_5_percent': 0,
        'breed_surcharge_20_percent': 0,
        'poisoning_coverage': 0,
        'blood_checkup': 0,
        'total': 0
    }
    
    if pricing_data and 'annual' in pricing_data:
        base_annual = pricing_data['annual']
        original_base = base_annual
        base_price_breakdown['base_price'] = original_base
        
        # Apply breed surcharges (cumulative - matching handle_application_submission logic)
        if special_breed_5_percent:
            surcharge_5 = base_annual * 0.05
            base_annual = base_annual * 1.05
            base_price_breakdown['breed_surcharge_5_percent'] = round(surcharge_5, 2)
        
        if special_breed_20_percent:
            # Calculate 20% on the current price (after 5% if applied)
            surcharge_20 = base_annual * 0.20
            base_annual = base_annual * 1.20
            base_price_breakdown['breed_surcharge_20_percent'] = round(surcharge_20, 2)
        
        # Calculate add-on prices based on program
        if additional_poisoning_coverage:
            poisoning_prices = {
                'silver': 18,
                'gold': 20,
                'platinum': 25
            }
            base_price_breakdown['poisoning_coverage'] = poisoning_prices.get(program, 18)
            base_annual += base_price_breakdown['poisoning_coverage']
        
        if additional_blood_checkup:
            base_price_breakdown['blood_checkup'] = 28  # Same for all programs
            base_annual += base_price_breakdown['blood_checkup']
        
        # Update all pricing fields with surcharges and add-ons applied
        if base_annual != original_base:
            surcharge_multiplier = base_annual / original_base
            pricing_data['annual'] = round(base_annual, 2)
            if 'six_month' in pricing_data:
                pricing_data['six_month'] = round(pricing_data['six_month'] * surcharge_multiplier, 2)
            if 'three_month' in pricing_data:
                pricing_data['three_month'] = round(pricing_data['three_month'] * surcharge_multiplier, 2)
            pricing_data['final'] = pricing_data['annual']
        
        base_price_breakdown['total'] = pricing_data['annual']
    
    # Get second pet pricing
    second_pet_pricing_data = None
    if second_pet_type and second_pet_program and second_pet_weight_category:
        if second_pet_type == 'dog' and second_pet_program in DOG_PRICING and second_pet_weight_category in DOG_PRICING[second_pet_program]:
            second_pet_pricing_data = DOG_PRICING[second_pet_program][second_pet_weight_category].copy()
            # Add 'final' field for compatibility with JavaScript
            if 'annual' in second_pet_pricing_data and 'final' not in second_pet_pricing_data:
                second_pet_pricing_data['final'] = second_pet_pricing_data['annual']
        elif second_pet_type == 'cat' and second_pet_program in CAT_PRICING and second_pet_weight_category in CAT_PRICING[second_pet_program]:
            second_pet_pricing_data = CAT_PRICING[second_pet_program][second_pet_weight_category].copy()
            # Add 'final' field for compatibility with JavaScript
            if 'annual' in second_pet_pricing_data and 'final' not in second_pet_pricing_data:
                second_pet_pricing_data['final'] = second_pet_pricing_data['annual']

    context = {
        'pet_type': pet_type,
        'gender': gender,
        'birthdate': birthdate,
        'breed': breed,
        'name': name,
        'weight_category': weight_category,
        'pricing_data': pricing_data,
        'program': program,
        'second_pet_name': second_pet_name,
        'second_pet_type': second_pet_type,
        'second_pet_gender': second_pet_gender,
        'second_pet_birthdate': second_pet_birthdate,
        'second_pet_breed': second_pet_breed,
        'second_pet_weight_category': second_pet_weight_category,
        'second_pet_pricing_data': second_pet_pricing_data,
        
        # Price breakdown data
        'price_breakdown': base_price_breakdown,
        'special_breed_5_percent': special_breed_5_percent,
        'special_breed_20_percent': special_breed_20_percent,
        'additional_poisoning_coverage': additional_poisoning_coverage,
        'additional_blood_checkup': additional_blood_checkup,
        
        # User data for pre-filling - check session first (from questionnaire), then URL params
        'user_full_name': '',
        'user_afm': '',
        'user_phone': '',
        'user_address': '',
        'user_postal_code': '',
        'user_email': '',
        'user_microchip': request.GET.get('user_microchip', ''),
    }
    
    # Get user data from session (stored when questionnaire was submitted)
    # session_data is already defined above if questionnaire_data exists
    if session_data and isinstance(session_data, dict):
        # Extract user data from session, handling both list and string values
        def get_session_value(key, default=''):
            value = session_data.get(key, default)
            if isinstance(value, list):
                return value[0] if value else default
            return value if value else default
        
        context['user_full_name'] = get_session_value('fullName', request.GET.get('user_full_name', ''))
        context['user_afm'] = get_session_value('afm', request.GET.get('user_afm', ''))
        context['user_phone'] = get_session_value('phone', request.GET.get('user_phone', ''))
        context['user_address'] = get_session_value('address', request.GET.get('user_address', ''))
        context['user_postal_code'] = get_session_value('postalCode', request.GET.get('user_postal_code', ''))
        context['user_email'] = get_session_value('email', request.GET.get('user_email', ''))
    else:
        # Fallback to URL parameters
        context['user_full_name'] = request.GET.get('user_full_name', '')
        context['user_afm'] = request.GET.get('user_afm', '')
        context['user_phone'] = request.GET.get('user_phone', '')
        context['user_address'] = request.GET.get('user_address', '')
        context['user_postal_code'] = request.GET.get('user_postal_code', '')
        context['user_email'] = request.GET.get('user_email', '')
    
    return render(request, 'main/user_data.html', context)

def handle_application_submission(request):
    """Handle insurance application form submission"""
    from .models import InsuranceApplication
    from datetime import datetime
    from django.http import JsonResponse
    import logging
    
    logger = logging.getLogger(__name__)
    
    try:
        # Parse birthdate - try multiple formats
        pet_birthdate = None
        birthdate_str = request.POST.get('birthdate', '')
        if birthdate_str:
            # Try YYYY-MM-DD format first
            try:
                pet_birthdate = datetime.strptime(birthdate_str, '%Y-%m-%d').date()
            except ValueError:
                # Try MM/DD/YYYY format
                try:
                    pet_birthdate = datetime.strptime(birthdate_str, '%m/%d/%Y').date()
                except ValueError:
                    # Try DD/MM/YYYY format
                    try:
                        pet_birthdate = datetime.strptime(birthdate_str, '%d/%m/%Y').date()
                    except ValueError:
                        logger.error(f"Could not parse birthdate: {birthdate_str}")
        
        # Validate required fields
        if not pet_birthdate:
            return JsonResponse({
                'success': False,
                'message': 'Παρακαλώ εισάγετε έγκυρη ημερομηνία γέννησης.'
            })
        
        pet_breed = request.POST.get('breed', '').strip()
        if not pet_breed:
            return JsonResponse({
                'success': False,
                'message': 'Παρακαλώ εισάγετε τη ράτσα του κατοικιδίου.'
            })
        
        # Parse second pet birthdate
        second_pet_birthdate = None
        if request.POST.get('secondPetBirthdate'):
            second_birthdate_str = request.POST.get('secondPetBirthdate', '')
            if second_birthdate_str:
                try:
                    second_pet_birthdate = datetime.strptime(second_birthdate_str, '%Y-%m-%d').date()
                except ValueError:
                    try:
                        second_pet_birthdate = datetime.strptime(second_birthdate_str, '%m/%d/%Y').date()
                    except ValueError:
                        try:
                            second_pet_birthdate = datetime.strptime(second_birthdate_str, '%d/%m/%Y').date()
                        except ValueError:
                            logger.error(f"Could not parse second pet birthdate: {second_birthdate_str}")
        
        # Calculate base premium from pricing tables
        pet_type_val = request.POST.get('type', '')
        program = request.POST.get('program', 'silver')
        breed = request.POST.get('breed', '')
        
        # Extract weight category from breed
        weight_category = None
        if breed:
            if 'έως 10 κιλά' in breed or 'up to 10' in breed.lower():
                weight_category = '10'
            elif '11-20 κιλά' in breed or '11-20' in breed:
                weight_category = '11-20'
            elif '21-40 κιλά' in breed or '21-40' in breed:
                weight_category = '21-40'
            elif '>40 κιλά' in breed or '>40' in breed:
                weight_category = '>40'
        
        # Get base pricing from tables (same as in user_data view)
        # Official pricing table - FINAL PRICES (matches official pricing spreadsheet)
        DOG_PRICING = {
            'silver': {'10': 166.75, '11-20': 207.20, '21-40': 234.14, '>40': 254.36},
            'gold': {'10': 234.14, '11-20': 261.09, '21-40': 288.05, '>40': 308.26},
            'platinum': {'10': 368.92, '11-20': 389.15, '21-40': 409.36, '>40': 436.32}
        }
        CAT_PRICING = {
            'silver': {'10': 113.81, '11-20': 141.02},
            'gold': {'10': 168.22, '11-20': 188.61},
            'platinum': {'10': 277.02, '11-20': 311.02}
        }
        
        # Get base premium
        base_premium = 0
        if pet_type_val == 'dog' and program in DOG_PRICING and weight_category in DOG_PRICING[program]:
            base_premium = DOG_PRICING[program][weight_category]
        elif pet_type_val == 'cat' and program in CAT_PRICING and weight_category in CAT_PRICING[program]:
            base_premium = CAT_PRICING[program][weight_category]
        
        # Apply breed surcharges from questionnaire (if available)
        # Check POST data first (from questionnaire submission)
        # Multiple checkboxes with same name come as a list
        special_breed_5_percent = False
        special_breed_20_percent = False
        
        # Check POST data
        post_5_percent = request.POST.getlist('special_breed_5_percent')
        post_20_percent = request.POST.getlist('special_breed_20_percent')
        
        if post_5_percent and 'true' in post_5_percent:
            special_breed_5_percent = True
        if post_20_percent and 'true' in post_20_percent:
            special_breed_20_percent = True
        
        # Also check session data (stored when questionnaire was submitted)
        if 'questionnaire_data' in request.session:
            session_data = request.session['questionnaire_data']
            if isinstance(session_data, dict):
                # Check for 5% surcharge in session
                session_5_percent = session_data.get('special_breed_5_percent')
                if session_5_percent:
                    if isinstance(session_5_percent, list):
                        special_breed_5_percent = 'true' in session_5_percent or True in [v == 'true' for v in session_5_percent]
                    else:
                        special_breed_5_percent = session_5_percent == 'true' or special_breed_5_percent
                # Check for 20% surcharge in session
                session_20_percent = session_data.get('special_breed_20_percent')
                if session_20_percent:
                    if isinstance(session_20_percent, list):
                        special_breed_20_percent = 'true' in session_20_percent or True in [v == 'true' for v in session_20_percent]
                    else:
                        special_breed_20_percent = session_20_percent == 'true' or special_breed_20_percent
        
        # Log initial base premium
        initial_premium = base_premium
        logger.info(f"Initial base premium before surcharges: {base_premium}")
        logger.info(f"Breed surcharges - 5%: {special_breed_5_percent}, 20%: {special_breed_20_percent}")
        
        # Apply surcharges to base premium (surcharges are cumulative if both selected)
        if special_breed_5_percent:
            base_premium = base_premium * 1.05  # Add 5% surcharge
            logger.info(f"Applied 5% breed surcharge. Base premium: {initial_premium} -> {base_premium}")
        if special_breed_20_percent:
            base_premium = base_premium * 1.20  # Add 20% surcharge
            logger.info(f"Applied 20% breed surcharge. Base premium: {base_premium}")
        
        # Round to 2 decimal places
        base_premium = round(base_premium, 2)
        logger.info(f"Final premium after breed surcharges: {base_premium} (was {initial_premium})")
        
        # Add extra features (poisoning coverage and blood checkup)
        extra_features_total = 0
        additional_poisoning = request.POST.get('additional_poisoning_coverage') == 'true'
        additional_blood_checkup = request.POST.get('additional_blood_checkup') == 'true'
        
        if additional_poisoning:
            # Poisoning coverage prices by program
            poisoning_prices = {
                'silver': 18,
                'gold': 20,
                'platinum': 25
            }
            poisoning_price = poisoning_prices.get(program, 18)
            extra_features_total += poisoning_price
            logger.info(f"Added poisoning coverage: +{poisoning_price}€")
        
        if additional_blood_checkup:
            # Blood checkup is 28€ for all programs
            extra_features_total += 28
            logger.info(f"Added blood checkup: +28€")
        
        base_premium += extra_features_total
        logger.info(f"Final premium after extra features: {base_premium}")
        
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
            pet_breed=pet_breed,
            pet_birthdate=pet_birthdate,
            pet_weight_category=extract_weight_from_breed(pet_breed),
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
            second_pet_health_status=request.POST.get('secondPetHealth', '') or '',
            second_pet_health_conditions=request.POST.get('secondPetHealthConditions', '') or '',
            
            # Pricing (with discount applied if code was used)
            annual_premium=base_premium,
            affiliate_code=affiliate_code_str if affiliate_code_str else None,
            discount_applied=discount_applied,
            
            # Contract PDF (will be generated later)
            contract_pdf_path='',
            
            # Status
            status='submitted'
        )
        
        # Create and save questionnaire
        # Get questionnaire data from session (stored when questionnaire was submitted) or from POST
        try:
            from .models import Questionnaire
            from datetime import datetime
            
            # Get questionnaire data from ALL sources: session, POST, and URL params
            # Priority: POST > Session > URL params (POST is most recent)
            questionnaire_data = {}
            
            # First, get from session (stored when questionnaire was submitted)
            if 'questionnaire_data' in request.session:
                session_data = request.session['questionnaire_data']
                logger.info(f"Retrieved questionnaire data from session with {len(session_data)} keys")
                # Convert QueryDict-like structure to regular dict
                for key, value in session_data.items():
                    if isinstance(value, list):
                        # For checkboxes with same name, if any is 'true', consider it True
                        if 'true' in value or True in value:
                            questionnaire_data[key] = 'true'
                        elif len(value) > 0:
                            # Keep the actual value (could be 'false' for radio buttons)
                            questionnaire_data[key] = value[0]
                        else:
                            questionnaire_data[key] = ''
                    else:
                        # Keep the value as-is (important for 'false' radio button values)
                        questionnaire_data[key] = value
                logger.info(f"Processed session questionnaire_data has {len(questionnaire_data)} keys: {list(questionnaire_data.keys())[:20]}")
            
            # Then, merge POST data (overrides session data - POST is more recent)
            for key in request.POST.keys():
                values = request.POST.getlist(key)
                # For checkboxes with same name (like special_breed_5_percent), if any is 'true', consider it True
                if 'true' in values or True in values:
                    questionnaire_data[key] = 'true'
                elif len(values) == 1:
                    questionnaire_data[key] = values[0]
                elif len(values) > 1:
                    questionnaire_data[key] = values  # Keep as list for processing
                else:
                    questionnaire_data[key] = ''
            
            # Also check URL parameters for any missing fields
            for key in request.GET.keys():
                if key not in questionnaire_data or not questionnaire_data[key]:
                    questionnaire_data[key] = request.GET.get(key, '')
            
            logger.info(f"Final merged questionnaire_data has {len(questionnaire_data)} keys from all sources")
            logger.info(f"Sample questionnaire_data keys: {list(questionnaire_data.keys())[:30]}")
            
            # Log questionnaire data for debugging
            logger.info(f"Creating questionnaire for application {application.id} with {len(questionnaire_data)} fields")
            
            # If questionnaire_data is empty, log a warning
            if not questionnaire_data or len(questionnaire_data) < 5:
                logger.warning(f"WARNING: Questionnaire data is very sparse! Only {len(questionnaire_data)} fields found.")
                logger.warning(f"POST keys: {list(request.POST.keys())[:30]}")
                logger.warning(f"Session has questionnaire_data: {'questionnaire_data' in request.session}")
                if 'questionnaire_data' in request.session:
                    session_keys = list(request.session['questionnaire_data'].keys()) if isinstance(request.session['questionnaire_data'], dict) else []
                    logger.warning(f"Session questionnaire_data keys: {session_keys[:30]}")
            
            def get_bool(key, default=False):
                # If key doesn't exist in questionnaire_data, return default (usually False)
                if key not in questionnaire_data:
                    return bool(default)  # Ensure it's always a boolean
                
                val = questionnaire_data.get(key, '')
                
                # Handle list values (multiple checkboxes with same name)
                if isinstance(val, list):
                    # If any value in list is 'true', return True
                    if 'true' in val or True in val:
                        return True
                    # If list has values, take first one
                    val = val[0] if val else ''
                
                # Handle string values
                if isinstance(val, str):
                    val_lower = val.lower().strip()
                    # Explicit 'false' or 'no' means False
                    if val_lower in ['false', 'no', '0', '']:
                        return False
                    # Explicit 'true' or 'yes' means True
                    if val_lower in ['true', 'yes', '1', 'on']:
                        return True
                    # Any non-empty string (for checkboxes) means True
                    if val_lower:
                        return True
                    # Empty string means False
                    return False
                
                # Handle boolean values
                if isinstance(val, bool):
                    return val
                
                # Handle None - return default as boolean
                if val is None:
                    return bool(default)
                
                # If value exists but is not recognized, return default as boolean
                return bool(default)
            
            def get_str(key, default=''):
                val = questionnaire_data.get(key, default)
                if isinstance(val, list):
                    val = val[0] if val else default
                return str(val) if val else default
            
            desired_start_date = None
            start_date_str = get_str('desired_start_date')
            if start_date_str:
                try:
                    desired_start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                except ValueError:
                    pass
            
            pet_type_val = request.POST.get('type', '') or get_str('type', '')
            is_dog = pet_type_val == 'dog'
            
            # Check for breed type - can come from breed_type field OR individual checkboxes
            breed_type = get_str('breed_type', '')
            if breed_type:
                is_purebred = breed_type == 'purebred'
                is_mixed = breed_type == 'mixed'
                is_crossbreed = breed_type == 'crossbreed'
            else:
                # Use individual checkbox fields
                is_purebred = get_bool('is_purebred')
                is_mixed = get_bool('is_mixed')
                is_crossbreed = get_bool('is_crossbreed')
            
            # Log what we're about to save
            logger.info(f"Questionnaire values to save:")
            logger.info(f"  Total fields in questionnaire_data: {len(questionnaire_data)}")
            logger.info(f"  Sample keys: {list(questionnaire_data.keys())[:30]}")
            logger.info(f"  has_other_insured_pet: {get_bool('has_other_insured_pet')} (raw: {questionnaire_data.get('has_other_insured_pet', 'NOT_FOUND')})")
            logger.info(f"  has_been_denied_insurance: {get_bool('has_been_denied_insurance')} (raw: {questionnaire_data.get('has_been_denied_insurance', 'NOT_FOUND')})")
            logger.info(f"  is_healthy: {get_bool('is_healthy')} (raw: {questionnaire_data.get('is_healthy', 'NOT_FOUND')})")
            logger.info(f"  special_breed_5_percent: {get_bool('special_breed_5_percent')} (raw: {questionnaire_data.get('special_breed_5_percent', 'NOT_FOUND')})")
            logger.info(f"  program: {get_str('program')} or POST: {request.POST.get('program', 'NONE')} or GET: {request.GET.get('program', 'NONE')}")
            logger.info(f"  payment_frequency: {get_str('payment_frequency')} or POST: {request.POST.get('payment_frequency', 'NONE')}")
            logger.info(f"  payment_method: {get_str('payment_method')} or POST: {request.POST.get('payment_method', 'NONE')}")
            
            # Build all questionnaire fields from all sources
            questionnaire_defaults = {
                'has_other_insured_pet': get_bool('has_other_insured_pet'),
                'has_been_denied_insurance': get_bool('has_been_denied_insurance'),
                'has_special_terms_imposed': get_bool('has_special_terms_imposed'),
                'pet_colors': get_str('pet_colors'),
                'pet_weight': get_str('pet_weight'),
                'is_purebred': is_purebred,
                'is_mixed': is_mixed,
                'is_crossbreed': is_crossbreed,
                'special_breed_5_percent': get_bool('special_breed_5_percent') if is_dog else False,
                'special_breed_20_percent': get_bool('special_breed_20_percent') if is_dog else False,
                'is_healthy': get_bool('is_healthy'),  # Get actual value, don't default
                'is_healthy_details': get_str('is_healthy_details'),
                'has_injury_illness_3_years': get_bool('has_injury_illness_3_years'),
                'has_injury_illness_details': get_str('has_injury_illness_details'),
                'has_surgical_procedure': get_bool('has_surgical_procedure'),
                'has_surgical_procedure_details': get_str('has_surgical_procedure_details'),
                'has_examination_findings': get_bool('has_examination_findings'),
                'has_examination_findings_details': get_str('has_examination_findings_details'),
                'is_sterilized': get_bool('is_sterilized'),
                'is_vaccinated_leishmaniasis': get_bool('is_vaccinated_leishmaniasis') if is_dog else False,
                'follows_vaccination_program': get_bool('follows_vaccination_program'),  # Get actual value
                'follows_vaccination_program_details': get_str('follows_vaccination_program_details'),
                'has_hereditary_disease': get_bool('has_hereditary_disease'),
                'has_hereditary_disease_details': get_str('has_hereditary_disease_details'),
                'program': get_str('program') or request.POST.get('program', '') or request.GET.get('program', ''),
                'additional_poisoning_coverage': get_bool('additional_poisoning_coverage'),
                'additional_blood_checkup': get_bool('additional_blood_checkup'),
                'desired_start_date': desired_start_date,
                'payment_method': get_str('payment_method') or request.POST.get('payment_method', '') or request.GET.get('payment_method', ''),
                'payment_frequency': get_str('payment_frequency') or request.POST.get('payment_frequency', '') or request.GET.get('payment_frequency', ''),
                'consent_terms_conditions': get_bool('consent_terms_conditions'),
                'consent_info_document': get_bool('consent_info_document'),
                'consent_email_notifications': get_bool('consent_email_notifications'),
                'consent_marketing': get_bool('consent_marketing'),
                'consent_data_processing': get_bool('consent_data_processing'),
                'consent_pet_gov_platform': get_bool('consent_pet_gov_platform'),
            }
            
            logger.info(f"Saving questionnaire with program: {questionnaire_defaults['program']}, payment_frequency: {questionnaire_defaults['payment_frequency']}, payment_method: {questionnaire_defaults['payment_method']}")
            
            questionnaire, created = Questionnaire.objects.get_or_create(
                application=application,
                defaults=questionnaire_defaults
            )
            
            if not created:
                # Update all fields if questionnaire already exists - use the same defaults dict
                for key, value in questionnaire_defaults.items():
                    setattr(questionnaire, key, value)
                questionnaire.save()
            
            # Log successful creation with detailed info
            logger.info(f"Questionnaire {'created' if created else 'updated'} successfully for application {application.id} (Questionnaire ID: {questionnaire.id})")
            logger.info(f"Questionnaire details - 5%: {questionnaire.special_breed_5_percent}, 20%: {questionnaire.special_breed_20_percent}, poisoning: {questionnaire.additional_poisoning_coverage}, blood: {questionnaire.additional_blood_checkup}")
            
            if 'questionnaire_data' in request.session:
                del request.session['questionnaire_data']
                if 'questionnaire_submitted' in request.session:
                    del request.session['questionnaire_submitted']
        except Exception as e:
            logger.error(f"Error creating/updating questionnaire for application {application.id}: {e}")
            import traceback
            logger.error(traceback.format_exc())
            # Even if there's an error, try to create an empty questionnaire so it's visible in admin
            try:
                Questionnaire.objects.get_or_create(application=application)
                logger.info(f"Created empty questionnaire for application {application.id} as fallback")
            except Exception as fallback_error:
                logger.error(f"Failed to create fallback questionnaire: {fallback_error}")
        
        # Link uploaded documents to application
        try:
            from .models import PetDocument
            # Get document IDs from session or POST
            document_ids = request.session.get('uploaded_document_ids', [])
            if not document_ids:
                # Try to get from POST
                document_ids_str = request.POST.get('document_ids', '')
                if document_ids_str:
                    document_ids = [int(id) for id in document_ids_str.split(',') if id.strip()]
            
            for doc_id in document_ids:
                try:
                    doc = PetDocument.objects.get(id=doc_id)
                    doc.application = application
                    doc.save()
                except PetDocument.DoesNotExist:
                    pass
            
            # Clear session
            if 'uploaded_document_ids' in request.session:
                del request.session['uploaded_document_ids']
        except Exception as e:
            logger.error(f"Error linking documents to application {application.id}: {e}")
            import traceback
            logger.error(traceback.format_exc())
        
        # Link uploaded photos to application
        try:
            from .models import PetPhoto
            # Get photo IDs from session or POST
            photo_ids = request.session.get('uploaded_photo_ids', [])
            if not photo_ids:
                # Try to get from POST
                photo_ids_str = request.POST.get('photo_ids', '')
                if photo_ids_str:
                    photo_ids = [int(id) for id in photo_ids_str.split(',') if id.strip()]
            
            for photo_id in photo_ids:
                try:
                    photo = PetPhoto.objects.get(id=photo_id)
                    photo.application = application
                    photo.save()
                except PetPhoto.DoesNotExist:
                    pass
            
            # Clear session
            if 'uploaded_photo_ids' in request.session:
                del request.session['uploaded_photo_ids']
        except Exception as e:
            logger.error(f"Error linking photos to application {application.id}: {e}")
            import traceback
            logger.error(traceback.format_exc())
        
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
            import traceback
            logger.error(traceback.format_exc())
        
        # Send notification emails (non-blocking - errors are logged but don't fail submission)
        try:
            from .email_utils import send_company_notification_email, send_customer_confirmation_email
            send_company_notification_email(application)
            send_customer_confirmation_email(application)
        except Exception as e:
            logger.error(f"Error sending emails for application {application.id}: {e}")
            import traceback
            logger.error(traceback.format_exc())
        
        return JsonResponse({
            'success': True,
            'application_id': application.id,
            'message': 'Η αίτηση υποβλήθηκε επιτυχώς!'
        })
        
    except Exception as e:
        logger.error(f"Error in handle_application_submission: {e}")
        import traceback
        logger.error(traceback.format_exc())
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
    return 0

def pet_documents(request):
    """Pet documents upload page"""
    pet_type = request.GET.get('type', '')
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

def contact_info(request):
    """Contact information page"""
    try:
        pet_type = request.GET.get('type', '')
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
        return render(request, 'main/contact_info.html', context)
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error in contact_info view: {e}")
        import traceback
        logger.error(traceback.format_exc())
        # Return a simple error page or redirect
        from django.http import HttpResponse
        return HttpResponse(f"Error loading page: {str(e)}", status=500)

def thank_you(request):
    """Thank you page after successful submission"""
    application_id = request.GET.get('application_id')
    application = None
    application_number = None
    
    if application_id:
        try:
            from .models import InsuranceApplication
            application = InsuranceApplication.objects.get(id=application_id)
            application_number = application.application_number
        except InsuranceApplication.DoesNotExist:
            pass
    
    # Also check URL parameter for application_number
    if not application_number:
        application_number = request.GET.get('application_number')
    
    # Use contract_number (same as admin and email) or application_number as fallback
    display_number = None
    if application:
        display_number = application.contract_number or application.application_number
    elif application_number:
        display_number = application_number
    
    context = {
        'application': application,
        'application_number': display_number,  # This will be contract_number or application_number
        'pet_name': application.pet_name if application else '',
        'pet_type': application.pet_type if application else '',
        'email': application.email if application else '',
        'full_name': application.full_name if application else '',
    }
    
    return render(request, 'main/thank_you.html', context)

@csrf_exempt
def upload_pet_document(request):
    """Handle pet document upload via AJAX"""
    import logging
    logger = logging.getLogger(__name__)
    
    logger.info(f"Upload request received - Method: {request.method}")
    logger.info(f"Request headers: {dict(request.headers)}")
    
    if request.method == 'POST':
        from .models import PetDocument
        
        try:
            logger.info(f"POST data keys: {list(request.POST.keys())}")
            logger.info(f"FILES keys: {list(request.FILES.keys())}")
            
            uploaded_file = request.FILES.get('file')
            if not uploaded_file:
                logger.warning("No file provided in request")
                return JsonResponse({'success': False, 'message': 'No file provided'})
            
            logger.info(f"File received: {uploaded_file.name}, Size: {uploaded_file.size}, Type: {uploaded_file.content_type}")
            
            # Create PetDocument record with file
            # Handle legacy columns with NOT NULL constraints in local DB
            from django.db import connection
            from django.utils import timezone
            from django.core.files.storage import default_storage
            
            # Check table structure for NOT NULL columns (database-agnostic)
            notnull_cols = {}
            try:
                with connection.cursor() as cursor:
                    vendor = connection.vendor
                    if vendor == 'sqlite':
                        cursor.execute("PRAGMA table_info(main_petdocument)")
                        table_info = cursor.fetchall()
                        notnull_cols = {row[1]: row[3] == 1 for row in table_info}
                    elif vendor == 'postgresql':
                        cursor.execute("""
                            SELECT column_name, is_nullable
                            FROM information_schema.columns
                            WHERE table_name = 'main_petdocument'
                        """)
                        table_info = cursor.fetchall()
                        notnull_cols = {row[0]: row[1] == 'NO' for row in table_info}
                    else:
                        # Fallback: assume no legacy columns
                        notnull_cols = {}
            except Exception as e:
                logger.warning(f"Could not check table structure: {e}")
                notnull_cols = {}
            
            # Check if we have legacy NOT NULL columns that aren't in model
            has_legacy_notnull = (
                notnull_cols.get('document_type', False) or
                (notnull_cols.get('pet_name', False) and not request.POST.get('pet_name')) or
                (notnull_cols.get('pet_type', False) and not request.POST.get('pet_type')) or
                notnull_cols.get('is_verified', False) or
                notnull_cols.get('user_id', False)
            )
            
            if has_legacy_notnull:
                # Use raw SQL to insert with all required legacy columns
                file_path = default_storage.save(f'pet_documents/{uploaded_file.name}', uploaded_file)
                now = timezone.now()
                pet_name = request.POST.get('pet_name', '') or ''
                pet_type = request.POST.get('pet_type', '') or ''
                
                with connection.cursor() as cursor:
                    # Build INSERT with all required columns
                    columns = ['file', 'original_filename', 'file_type', 'file_size', 'created_at', 'updated_at']
                    values = [file_path, uploaded_file.name, uploaded_file.content_type or 'application/octet-stream', uploaded_file.size, now, now]
                    placeholders = ['?' for _ in columns]
                    
                    # Add legacy columns if they exist and are NOT NULL
                    if 'document_type' in notnull_cols and notnull_cols['document_type']:
                        columns.append('document_type')
                        values.append('upload')
                        placeholders.append('?')
                    
                    if 'pet_name' in notnull_cols and notnull_cols['pet_name']:
                        columns.append('pet_name')
                        values.append(pet_name)
                        placeholders.append('?')
                    
                    if 'pet_type' in notnull_cols and notnull_cols['pet_type']:
                        columns.append('pet_type')
                        values.append(pet_type)
                        placeholders.append('?')
                    
                    if 'uploaded_at' in notnull_cols:
                        columns.append('uploaded_at')
                        values.append(now)
                        placeholders.append('?')
                    
                    if 'is_verified' in notnull_cols and notnull_cols['is_verified']:
                        columns.append('is_verified')
                        values.append(0)  # False in SQLite
                        placeholders.append('?')
                    
                    if 'user_id' in notnull_cols and notnull_cols['user_id']:
                        # user_id is NOT NULL - provide a default
                        user_id = None
                        if hasattr(request, 'user') and request.user.is_authenticated:
                            user_id = request.user.id
                        else:
                            # Get or create a default system user for uploads
                            try:
                                from django.contrib.auth.models import User
                                default_user, created = User.objects.get_or_create(
                                    username='upload_system',
                                    defaults={
                                        'email': 'system@hoolie.gr',
                                        'is_active': False,
                                        'is_staff': False
                                    }
                                )
                                user_id = default_user.id
                                if created:
                                    logger.info(f"Created default system user for uploads: {user_id}")
                            except Exception as e:
                                logger.error(f"Could not get/create default user: {e}")
                                # Fallback: try to use first user or ID 1
                                try:
                                    first_user = User.objects.first()
                                    user_id = first_user.id if first_user else 1
                                except:
                                    user_id = 1
                        
                        columns.append('user_id')
                        values.append(user_id)
                        placeholders.append('?')
                    
                    sql = f"INSERT INTO main_petdocument ({', '.join(columns)}) VALUES ({', '.join(placeholders)})"
                    cursor.execute(sql, values)
                    doc_id = cursor.lastrowid
                
                # Get the document object
                document = PetDocument.objects.get(id=doc_id)
                logger.info(f"Created document via raw SQL to handle legacy columns: {document.id}")
            else:
                # Normal creation if no legacy NOT NULL constraints
                document = PetDocument.objects.create(
                    file=uploaded_file,
                    original_filename=uploaded_file.name,
                    file_type=uploaded_file.content_type or 'application/octet-stream',
                    file_size=uploaded_file.size
                )
            
            logger.info(f"Document created successfully - ID: {document.id}, Path: {document.file.name}")
            
            # Store document ID in session for later linking to application
            if 'uploaded_document_ids' not in request.session:
                request.session['uploaded_document_ids'] = []
            request.session['uploaded_document_ids'].append(document.id)
            request.session.modified = True
            
            file_url = document.get_file_url()
            logger.info(f"File URL generated: {file_url}")
            
            return JsonResponse({
                'success': True,
                'document_id': document.id,
                'file_url': file_url,
                'file_name': document.original_filename,
                'file_size': document.file_size
            })
        except Exception as e:
            logger.error(f"Error uploading document: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return JsonResponse({'success': False, 'message': str(e)})
    
    logger.warning(f"Method not allowed: {request.method}")
    return JsonResponse({'success': False, 'message': 'Method not allowed'})

@csrf_exempt
def upload_pet_photo(request):
    """Handle pet photo upload via AJAX"""
    import logging
    logger = logging.getLogger(__name__)
    
    logger.info(f"Photo upload request received - Method: {request.method}")
    
    if request.method == 'POST':
        from .models import PetPhoto
        
        try:
            logger.info(f"POST data keys: {list(request.POST.keys())}")
            logger.info(f"FILES keys: {list(request.FILES.keys())}")
            
            uploaded_file = request.FILES.get('file')
            if not uploaded_file:
                logger.warning("No file provided in photo upload request")
                return JsonResponse({'success': False, 'message': 'No file provided'})
            
            logger.info(f"Photo received: {uploaded_file.name}, Size: {uploaded_file.size}, Type: {uploaded_file.content_type}")
            
            # Create PetPhoto record with file
            # Handle legacy columns if they exist (same as PetDocument)
            from django.db import connection
            from django.utils import timezone
            from django.core.files.storage import default_storage
            
            # Check if PetPhoto table exists and has legacy NOT NULL columns (database-agnostic)
            has_legacy = False
            notnull_cols = {}
            try:
                with connection.cursor() as cursor:
                    vendor = connection.vendor
                    if vendor == 'sqlite':
                        cursor.execute("PRAGMA table_info(main_petphoto)")
                        table_info = cursor.fetchall()
                        notnull_cols = {row[1]: row[3] == 1 for row in table_info}
                    elif vendor == 'postgresql':
                        cursor.execute("""
                            SELECT column_name, is_nullable
                            FROM information_schema.columns
                            WHERE table_name = 'main_petphoto'
                        """)
                        table_info = cursor.fetchall()
                        notnull_cols = {row[0]: row[1] == 'NO' for row in table_info}
                    has_legacy = any(col in notnull_cols and notnull_cols[col] for col in ['document_type', 'is_verified', 'user_id'])
            except Exception as e:
                logger.warning(f"Could not check PetPhoto table structure: {e}")
                has_legacy = False
                notnull_cols = {}
            
            if has_legacy:
                # Use raw SQL for photo upload too if needed
                file_path = default_storage.save(f'pet_photos/{uploaded_file.name}', uploaded_file)
                now = timezone.now()
                pet_name = request.POST.get('pet_name', '') or ''
                pet_type = request.POST.get('pet_type', '') or ''
                
                with connection.cursor() as cursor:
                    columns = ['file', 'original_filename', 'file_type', 'file_size', 'created_at', 'updated_at', 'uploaded_at']
                    values = [file_path, uploaded_file.name, uploaded_file.content_type or 'image/jpeg', uploaded_file.size, now, now, now]
                    placeholders = ['?' for _ in columns]
                    
                    # Add legacy columns if needed (same logic as PetDocument)
                    if 'document_type' in notnull_cols and notnull_cols['document_type']:
                        columns.append('document_type')
                        values.append('photo')
                        placeholders.append('?')
                    if 'pet_name' in notnull_cols and notnull_cols['pet_name']:
                        columns.append('pet_name')
                        values.append(pet_name)
                        placeholders.append('?')
                    if 'pet_type' in notnull_cols and notnull_cols['pet_type']:
                        columns.append('pet_type')
                        values.append(pet_type)
                        placeholders.append('?')
                    if 'is_verified' in notnull_cols and notnull_cols['is_verified']:
                        columns.append('is_verified')
                        values.append(0)
                        placeholders.append('?')
                    if 'user_id' in notnull_cols and notnull_cols['user_id']:
                        from django.contrib.auth.models import User
                        try:
                            default_user, _ = User.objects.get_or_create(
                                username='upload_system',
                                defaults={'email': 'system@hoolie.gr', 'is_active': False, 'is_staff': False}
                            )
                            columns.append('user_id')
                            values.append(default_user.id)
                            placeholders.append('?')
                        except:
                            pass
                    
                    sql = f"INSERT INTO main_petphoto ({', '.join(columns)}) VALUES ({', '.join(placeholders)})"
                    cursor.execute(sql, values)
                    photo_id = cursor.lastrowid
                
                photo = PetPhoto.objects.get(id=photo_id)
                logger.info(f"Created photo via raw SQL: {photo.id}")
            else:
                # Normal creation
                photo = PetPhoto.objects.create(
                    file=uploaded_file,
                    original_filename=uploaded_file.name,
                    file_type=uploaded_file.content_type or 'image/jpeg',
                    file_size=uploaded_file.size
                )
            
            logger.info(f"Photo created successfully - ID: {photo.id}, Path: {photo.file.name}")
            
            # Store photo ID in session for later linking to application
            if 'uploaded_photo_ids' not in request.session:
                request.session['uploaded_photo_ids'] = []
            request.session['uploaded_photo_ids'].append(photo.id)
            request.session.modified = True
            
            file_url = photo.get_file_url()
            logger.info(f"Photo URL generated: {file_url}")
            
            return JsonResponse({
                'success': True,
                'photo_id': photo.id,
                'file_url': file_url,
                'file_name': photo.original_filename,
                'file_size': photo.file_size
            })
        except Exception as e:
            logger.error(f"Error uploading photo: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return JsonResponse({'success': False, 'message': str(e)})
    
    logger.warning(f"Method not allowed: {request.method}")
    return JsonResponse({'success': False, 'message': 'Method not allowed'})

@require_http_methods(["POST"])
def validate_affiliate_code(request):
    """Validate an affiliate/ambassador code and return discount information"""
    import json
    from .models import AmbassadorCode
    
    try:
        data = json.loads(request.body)
        code = data.get('code', '').strip().upper()
        
        if not code:
            return JsonResponse({
                'success': False,
                'error': 'Παρακαλώ εισάγετε έναν κωδικό συνεργάτη.'
            })
        
        try:
            affiliate_code = AmbassadorCode.objects.get(code=code)
            
            if not affiliate_code.is_valid():
                return JsonResponse({
                    'success': False,
                    'error': 'Ο κωδικός δεν είναι έγκυρος ή έχει λήξει.'
                })
            
            # Return success with discount information
            discount_info = {
                'type': 'percentage' if affiliate_code.discount_percentage > 0 else 'fixed',
                'value': float(affiliate_code.discount_percentage) if affiliate_code.discount_percentage > 0 else float(affiliate_code.discount_amount),
                'description': f"Έκπτωση {affiliate_code.discount_percentage}%" if affiliate_code.discount_percentage > 0 else f"Έκπτωση {affiliate_code.discount_amount}€"
            }
            
            return JsonResponse({
                'success': True,
                'message': f'Ο κωδικός "{code}" είναι έγκυρος!',
                'discount': discount_info
            })
            
        except AmbassadorCode.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Ο κωδικός δεν βρέθηκε.'
            })
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Μη έγκυρο αίτημα.'
        })
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error validating affiliate code: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return JsonResponse({
            'success': False,
            'error': 'Σφάλμα κατά την επικύρωση του κωδικού.'
        })

def serve_file(request, file_type, file_id):
    """Serve files from S3 or local storage"""
    from .models import PetDocument, PetPhoto
    from django.http import Http404, FileResponse, HttpResponseRedirect
    from django.conf import settings
    from django.core.files.storage import default_storage
    import os
    
    try:
        if file_type == 'document':
            file_obj = get_object_or_404(PetDocument, id=file_id)
        elif file_type == 'photo':
            file_obj = get_object_or_404(PetPhoto, id=file_id)
        else:
            raise Http404("Invalid file type")
        
        if not file_obj.file:
            raise Http404("File not found")
        
        # Check if using S3 storage (Bucketeer)
        if hasattr(settings, 'DEFAULT_FILE_STORAGE') and 's3boto3' in settings.DEFAULT_FILE_STORAGE.lower():
            # Using S3/Bucketeer - generate signed URL for private files
            try:
                import boto3
                from botocore.client import Config
                from botocore.exceptions import ClientError
                
                s3_client = boto3.client(
                    's3',
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                    region_name=settings.AWS_S3_REGION_NAME,
                    config=Config(signature_version='s3v4')
                )
                
                # Get the S3 key (path) of the file
                # Django storages stores files with AWS_LOCATION prefix (usually 'media/')
                s3_key = file_obj.file.name
                
                # Ensure the key includes the AWS_LOCATION prefix if it's not already there
                # Django's S3Boto3Storage automatically adds AWS_LOCATION to the key
                # But file.name might or might not include it depending on storage configuration
                if hasattr(settings, 'AWS_LOCATION') and settings.AWS_LOCATION:
                    # If the key doesn't start with the location prefix, add it
                    if not s3_key.startswith(settings.AWS_LOCATION + '/'):
                        # Check if it already starts with just the location (no slash)
                        if not s3_key.startswith(settings.AWS_LOCATION):
                            s3_key = f"{settings.AWS_LOCATION}/{s3_key}"
                
                # Check if file exists in S3 before generating signed URL
                try:
                    s3_client.head_object(
                        Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                        Key=s3_key
                    )
                except ClientError as e:
                    # File doesn't exist in S3
                    error_code = e.response.get('Error', {}).get('Code', '')
                    if error_code == '404' or error_code == 'NoSuchKey':
                        import logging
                        logger = logging.getLogger(__name__)
                        logger.warning(f"File not found in S3: {s3_key} (file_type={file_type}, file_id={file_id})")
                        raise Http404(f"File not found in storage: {s3_key}")
                    else:
                        # Other S3 error, re-raise
                        raise
                
                # File exists, generate signed URL (valid for 1 hour)
                # Use the corrected s3_key that includes AWS_LOCATION prefix
                signed_url = s3_client.generate_presigned_url(
                    'get_object',
                    Params={
                        'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                        'Key': s3_key
                    },
                    ExpiresIn=3600  # 1 hour
                )
                return HttpResponseRedirect(signed_url)
            except Http404:
                # Re-raise Http404
                raise
            except Exception as e:
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Error generating signed URL for {file_type}/{file_id}: {e}")
                import traceback
                logger.error(traceback.format_exc())
                # Check if file exists using default_storage (with proper key)
                # Try with AWS_LOCATION prefix if it exists
                check_key = file_obj.file.name
                if hasattr(settings, 'AWS_LOCATION') and settings.AWS_LOCATION:
                    if not check_key.startswith(settings.AWS_LOCATION + '/'):
                        if not check_key.startswith(settings.AWS_LOCATION):
                            check_key = f"{settings.AWS_LOCATION}/{check_key}"
                
                if default_storage.exists(check_key):
                    # File exists, try fallback to direct URL
                    s3_url = file_obj.file.url
                    if s3_url.startswith('http://'):
                        s3_url = s3_url.replace('http://', 'https://', 1)
                    return HttpResponseRedirect(s3_url)
                else:
                    # File doesn't exist
                    raise Http404(f"File not found: {file_obj.file.name} (checked as: {check_key})")
        else:
            # Using local storage - serve the file directly
            file_path = file_obj.file.path
            if os.path.exists(file_path):
                return FileResponse(open(file_path, 'rb'), content_type=file_obj.file_type)
            else:
                raise Http404("File not found")
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error serving file {file_type}/{file_id}: {e}")
        import traceback
        logger.error(traceback.format_exc())
        raise Http404("File not found")


def favicon(request):
    """Handle favicon requests - return 204 No Content to stop browser requests"""
    return HttpResponse(status=204)
