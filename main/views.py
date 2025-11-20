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

def pet_breed(request):
    """Dog breed selection page"""
    pet_type = request.GET.get('type', 'dog')
    gender = request.GET.get('gender', '')
    
    # Common dog breeds for dropdown
    dog_breeds = [
        'Λαμπραντόρ', 'Γερμανικός Ποιμενικός', 'Γκόλντεν Ριτρίβερ', 'Φρανσεζέ Μπουλντόγκ',
        'Μποξέρ', 'Γερμανικό Δαχτυλίδι', 'Ροτβάιλερ', 'Γερμανικό Δάχτυλο',
        'Γερμανικό Δάχτυλο', 'Γερμανικό Δάχτυλο', 'Γερμανικό Δάχτυλο', 'Γερμανικό Δάχτυλο'
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
    
    # Common cat breeds for dropdown  
    cat_breeds = [
        'Περσική', 'Μέιν Κουν', 'Βρετανική Κοντότριχη', 'Ράγκντολ',
        'Αμπισινιανή', 'Σιαμική', 'Αμερικανική Κοντότριχη', 'Σκωτσέζικη Κρέμα'
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
    
    context = {
        'pet_type': pet_type,
        'gender': gender,
        'birthdate': birthdate,
        'breed': breed,
        'name': name
    }
    return render(request, 'main/dog_health_conditions.html', context)

def cat_health_conditions(request):
    """Cat health conditions page for underwriting"""
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
        
    # Pricing tables (same as in frontend)
    DOG_PRICING = {
        'silver': {
            '10': {'annual': 180, 'six_month': 95, 'three_month': 50},
            '11-20': {'annual': 220, 'six_month': 115, 'three_month': 60},
            '21-40': {'annual': 280, 'six_month': 145, 'three_month': 75},
            '>40': {'annual': 350, 'six_month': 180, 'three_month': 95}
        },
        'gold': {
            '10': {'annual': 240, 'six_month': 125, 'three_month': 65},
            '11-20': {'annual': 300, 'six_month': 155, 'three_month': 80},
            '21-40': {'annual': 380, 'six_month': 195, 'three_month': 100},
            '>40': {'annual': 480, 'six_month': 245, 'three_month': 125}
        },
        'platinum': {
            '10': {'annual': 320, 'six_month': 165, 'three_month': 85},
            '11-20': {'annual': 400, 'six_month': 205, 'three_month': 105},
            '21-40': {'annual': 500, 'six_month': 255, 'three_month': 130},
            '>40': {'annual': 620, 'six_month': 315, 'three_month': 160}
        }
    }
    
    CAT_PRICING = {
        'silver': {
            '10': {'annual': 150, 'six_month': 78, 'three_month': 40},
            '11-20': {'annual': 180, 'six_month': 93, 'three_month': 48},
            '21-40': {'annual': 220, 'six_month': 113, 'three_month': 58},
            '>40': {'annual': 280, 'six_month': 143, 'three_month': 73}
        },
        'gold': {
            '10': {'annual': 200, 'six_month': 103, 'three_month': 53},
            '11-20': {'annual': 240, 'six_month': 123, 'three_month': 63},
            '21-40': {'annual': 300, 'six_month': 153, 'three_month': 78},
            '>40': {'annual': 380, 'six_month': 193, 'three_month': 98}
        },
        'platinum': {
            '10': {'annual': 260, 'six_month': 133, 'three_month': 68},
            '11-20': {'annual': 320, 'six_month': 163, 'three_month': 83},
            '21-40': {'annual': 400, 'six_month': 203, 'three_month': 103},
            '>40': {'annual': 500, 'six_month': 253, 'three_month': 128}
        }
    }
    
    # Get program from URL or default to 'silver'
    program = request.GET.get('program', 'silver')
    second_pet_program = request.GET.get('secondPetProgram', 'silver')
    
    # Get pricing data
    pricing_data = None
    if pet_type == 'dog' and program in DOG_PRICING and weight_category in DOG_PRICING[program]:
        pricing_data = DOG_PRICING[program][weight_category]
    elif pet_type == 'cat' and program in CAT_PRICING and weight_category in CAT_PRICING[program]:
        pricing_data = CAT_PRICING[program][weight_category]
    
    # Get second pet pricing
    second_pet_pricing_data = None
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
        
        # User data for pre-filling
        'user_full_name': request.GET.get('user_full_name', ''),
        'user_afm': request.GET.get('user_afm', ''),
        'user_phone': request.GET.get('user_phone', ''),
        'user_address': request.GET.get('user_address', ''),
        'user_postal_code': request.GET.get('user_postal_code', ''),
        'user_email': request.GET.get('user_email', ''),
    }
    
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
                        questionnaire_data[key] = value[0]
                    else:
                        questionnaire_data[key] = value
            else:
                # Fallback: get from POST
                for key in request.POST.keys():
                    values = request.POST.getlist(key)
                    if len(values) == 1:
                        questionnaire_data[key] = values[0]
                    else:
                        questionnaire_data[key] = values
            
            def get_bool(key, default=False):
                val = questionnaire_data.get(key, '')
                if isinstance(val, list):
                    val = val[0] if val else ''
                return val == 'true' or val is True
            
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
            
            breed_type = get_str('breed_type', '')
            is_purebred = breed_type == 'purebred'
            is_mixed = breed_type == 'mixed'
            is_crossbreed = breed_type == 'crossbreed'
            
            questionnaire, created = Questionnaire.objects.get_or_create(
                application=application,
                defaults={
                    'has_other_insured_pet': get_bool('has_other_insured_pet'),
                    'has_been_denied_insurance': get_bool('has_been_denied_insurance'),
                    'has_special_terms_imposed': get_bool('has_special_terms_imposed'),
                    'pet_colors': get_str('pet_colors'),
                    'pet_weight': get_str('pet_weight'),
                    'is_purebred': is_purebred,
                    'is_mixed': is_mixed,
                    'is_crossbreed': is_crossbreed,
                    'pet_breed_or_crossbreed': get_str('pet_breed_or_crossbreed'),
                    'special_breed_5_percent': get_bool('special_breed_5_percent') if is_dog else False,
                    'special_breed_20_percent': get_bool('special_breed_20_percent') if is_dog else False,
                    'is_healthy': get_bool('is_healthy'),
                    'is_healthy_details': get_str('is_healthy_details'),
                    'has_injury_illness_3_years': get_bool('has_injury_illness_3_years'),
                    'has_injury_illness_details': get_str('has_injury_illness_3_years_details'),
                    'has_surgical_procedure': get_bool('has_surgical_procedure'),
                    'has_surgical_procedure_details': get_str('has_surgical_procedure_details'),
                    'has_examination_findings': get_bool('has_examination_findings'),
                    'has_examination_findings_details': get_str('has_examination_findings_details'),
                    'is_sterilized': get_bool('is_sterilized'),
                    'is_vaccinated_leishmaniasis': get_bool('is_vaccinated_leishmaniasis') if is_dog else False,
                    'follows_vaccination_program': get_bool('follows_vaccination_program'),
                    'follows_vaccination_program_details': get_str('follows_vaccination_program_details'),
                    'has_hereditary_disease': get_bool('has_hereditary_disease'),
                    'has_hereditary_disease_details': get_str('has_hereditary_disease_details'),
                    'program': get_str('program') or request.POST.get('program', ''),
                    'additional_poisoning_coverage': get_bool('additional_poisoning_coverage'),
                    'additional_blood_checkup': get_bool('additional_blood_checkup'),
                    'desired_start_date': desired_start_date,
                    'payment_method': get_str('payment_method'),
                    'payment_frequency': get_str('payment_frequency') or request.POST.get('payment_frequency', ''),
                    'consent_terms_conditions': get_bool('consent_terms_conditions'),
                    'consent_info_document': get_bool('consent_info_document'),
                    'consent_email_notifications': get_bool('consent_email_notifications'),
                    'consent_marketing': get_bool('consent_marketing'),
                    'consent_data_processing': get_bool('consent_data_processing'),
                    'consent_pet_gov_platform': get_bool('consent_pet_gov_platform'),
                }
            )
            
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
                questionnaire.payment_frequency = get_str('payment_frequency') or request.POST.get('payment_frequency', '')
                questionnaire.consent_terms_conditions = get_bool('consent_terms_conditions')
                questionnaire.consent_info_document = get_bool('consent_info_document')
                questionnaire.consent_email_notifications = get_bool('consent_email_notifications')
                questionnaire.consent_marketing = get_bool('consent_marketing')
                questionnaire.consent_data_processing = get_bool('consent_data_processing')
                questionnaire.consent_pet_gov_platform = get_bool('consent_pet_gov_platform')
                questionnaire.save()
            
            if 'questionnaire_data' in request.session:
                del request.session['questionnaire_data']
                if 'questionnaire_submitted' in request.session:
                    del request.session['questionnaire_submitted']
        except Exception as e:
            logger.error(f"Error creating/updating questionnaire for application {application.id}: {e}")
            logger.error(traceback.format_exc())
        
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
            from .email_utils import send_company_notification_email, send_customer_notification_email
            send_company_notification_email(application)
            send_customer_notification_email(application)
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

def thank_you(request):
    """Thank you page after successful submission"""
    return render(request, 'main/thank_you.html')

def upload_pet_document(request):
    """Handle pet document upload via AJAX"""
    if request.method == 'POST':
        from .models import PetDocument
        
        try:
            uploaded_file = request.FILES.get('file')
            if not uploaded_file:
                return JsonResponse({'success': False, 'message': 'No file provided'})
            
            # Create PetDocument record with file
            document = PetDocument.objects.create(
                file=uploaded_file,
                original_filename=uploaded_file.name,
                file_type=uploaded_file.content_type or 'application/octet-stream',
                file_size=uploaded_file.size
            )
            
            # Store document ID in session for later linking to application
            if 'uploaded_document_ids' not in request.session:
                request.session['uploaded_document_ids'] = []
            request.session['uploaded_document_ids'].append(document.id)
            request.session.modified = True
            
            return JsonResponse({
                'success': True,
                'document_id': document.id,
                'file_url': document.get_file_url(),
                'file_name': document.original_filename,
                'file_size': document.file_size
            })
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error uploading document: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'})

def upload_pet_photo(request):
    """Handle pet photo upload via AJAX"""
    if request.method == 'POST':
        from .models import PetPhoto
        
        try:
            uploaded_file = request.FILES.get('file')
            if not uploaded_file:
                return JsonResponse({'success': False, 'message': 'No file provided'})
            
            # Create PetPhoto record with file
            photo = PetPhoto.objects.create(
                file=uploaded_file,
                original_filename=uploaded_file.name,
                file_type=uploaded_file.content_type or 'image/jpeg',
                file_size=uploaded_file.size
            )
            
            # Store photo ID in session for later linking to application
            if 'uploaded_photo_ids' not in request.session:
                request.session['uploaded_photo_ids'] = []
            request.session['uploaded_photo_ids'].append(photo.id)
            request.session.modified = True
            
            return JsonResponse({
                'success': True,
                'photo_id': photo.id,
                'file_url': photo.get_file_url(),
                'file_name': photo.original_filename,
                'file_size': photo.file_size
            })
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error uploading photo: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return JsonResponse({'success': False, 'message': str(e)})
    
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
        
        # Check if using S3 storage
        if hasattr(settings, 'DEFAULT_FILE_STORAGE') and 's3' in settings.DEFAULT_FILE_STORAGE.lower():
            # Using S3 - get the S3 URL and redirect (ensure HTTPS)
            s3_url = file_obj.file.url
            # Ensure URL uses HTTPS
            if s3_url.startswith('http://'):
                s3_url = s3_url.replace('http://', 'https://', 1)
            return HttpResponseRedirect(s3_url)
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
