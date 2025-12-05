"""
Clean fillable PDF contract generation using fillpdf library
"""
import os
from tempfile import TemporaryDirectory
from django.conf import settings
from django.core.files.base import ContentFile
from fillpdf import fillpdfs
from datetime import datetime
# QR utils import - optional (only needed if QR codes are generated)
try:
    from .qr_utils import generate_contract_verification_qr, generate_terms_qr
except ImportError:
    # QR utils not available - contracts will work without QR codes
    generate_contract_verification_qr = None
    generate_terms_qr = None

def generate_contract_with_fillpdf(application, output_path, pet_number=1):
    """Generate contract using fillpdf library - much cleaner approach"""
    
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"  [PDF] Generating contract with fillpdf (Pet {pet_number}) for application {application.id}...")
    
    # Path to the fillable PDF template - NEW TEMPLATE
    template_path = os.path.join(settings.BASE_DIR, 'ΑΣΦΑΛΙΣΤΗΡΙΟ ΣΥΜΒΟΛΑΙΟ ΤΕΛΙΚΟ PET (1) (2).pdf')
    
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Fillable PDF template not found: {template_path}")
    
    # Determine which pet data to use
    if pet_number == 2 and application.has_second_pet:
        pet_name = application.second_pet_name
        pet_type_display = 'Γάτα' if application.second_pet_type == 'cat' else 'Σκύλος'
        pet_breed = application.second_pet_breed
        pet_weight = application.get_weight_display(application.second_pet_weight_category) if application.second_pet_weight_category else ''
        pet_birthdate = application.second_pet_birthdate.strftime('%d/%m/%Y') if application.second_pet_birthdate else ''
        contract_suffix = "-PET2"
        logger.info(f"  [INFO] Using Pet 2 data: {pet_name} ({pet_type_display})")
    else:
        pet_name = application.pet_name
        pet_type_display = application.get_pet_type_display_greek()
        pet_breed = application.pet_breed
        pet_weight = application.get_weight_display(application.pet_weight_category) if application.pet_weight_category else ''
        pet_birthdate = application.pet_birthdate.strftime('%d/%m/%Y') if application.pet_birthdate else ''
        contract_suffix = "-PET1" if application.has_second_pet else ""
        logger.info(f"  [INFO] Using Pet 1 data: {pet_name} ({pet_type_display})")
    
    # Calculate premium breakdown
    if application.annual_premium:
        net_premium = float(application.annual_premium) * 0.85
        fee = float(application.annual_premium) * 0.05
        auxiliary = float(application.annual_premium) * 0.02
        tax = float(application.annual_premium) * 0.08
    else:
        net_premium = fee = auxiliary = tax = 0
    
    # Create field mapping based on your contract template
    data = create_contract_field_mapping(
        application, pet_name, pet_type_display, pet_breed, 
        pet_weight, pet_birthdate, contract_suffix, 
        net_premium, fee, auxiliary, tax
    )
    
    try:
        # Fill the PDF using fillpdf
        logger.info(f"  [FILL] Filling PDF form with {len(data)} fields...")
        
        # First, fill without flattening so we can modify fonts
        temp_output = output_path.replace('.pdf', '_temp.pdf')
        fillpdfs.write_fillable_pdf(
            template_path,
            temp_output,
            data_dict=data,
            flatten=False,  # Don't flatten yet - we need to modify fonts first
        )
        
        # Normalize fonts using PyMuPDF
        try:
            import fitz  # PyMuPDF
            logger.info(f"  [FONT] Normalizing font sizes and families...")
            
            doc = fitz.open(temp_output)
            
            # Standardize font properties - Use Calibri for both English and Greek
            STANDARD_FONT = "Calibri"  # Calibri font (supports both English and Greek)
            STANDARD_FONT_SIZE = 10  # Standard font size
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                
                # Get all form fields/widgets
                for widget in page.widgets():
                    # Set default appearance for text fields
                    if widget.field_type == fitz.PDF_WIDGET_TYPE_TEXT:
                        # Set font properties for Calibri
                        widget.field_display = fitz.PDF_FIELD_DISPLAY_VISIBLE
                        widget.text_fontsize = STANDARD_FONT_SIZE
                        # Try to set Calibri font - PyMuPDF will use it if available
                        try:
                            widget.text_font = STANDARD_FONT
                        except:
                            # If Calibri not available, try alternative approach
                            # Use default appearance string with Calibri
                            try:
                                # Set default appearance with Calibri
                                widget.set_text_value(widget.field_value, fontname=STANDARD_FONT, fontsize=STANDARD_FONT_SIZE)
                            except:
                                logger.warning(f"  [WARNING] Could not set Calibri font for field, using default")
                        widget.update()
            
            # Save the modified PDF
            doc.save(output_path, incremental=False, encryption=fitz.PDF_ENCRYPT_KEEP)
            doc.close()
            
            # Remove temp file
            if os.path.exists(temp_output):
                os.remove(temp_output)
            
            logger.info(f"  [FONT] Font normalization completed")
            
        except ImportError:
            logger.warning(f"  [WARNING] PyMuPDF (fitz) not available, skipping font normalization")
            # If PyMuPDF not available, just use the filled PDF as-is
            if os.path.exists(temp_output):
                import shutil
                shutil.move(temp_output, output_path)
        except Exception as font_error:
            logger.warning(f"  [WARNING] Error normalizing fonts: {font_error}, using filled PDF as-is")
            # If font normalization fails, use the filled PDF
            if os.path.exists(temp_output):
                import shutil
                shutil.move(temp_output, output_path)
        
        # Flatten the final PDF to make it non-editable
        try:
            import fitz  # PyMuPDF
            doc = fitz.open(output_path)
            for page_num in range(len(doc)):
                page = doc[page_num]
                # Flatten form fields (make them non-editable)
                page.flatten()
            doc.save(output_path, incremental=False, encryption=fitz.PDF_ENCRYPT_KEEP)
            doc.close()
            logger.info(f"  [FLATTEN] PDF flattened successfully")
        except Exception as flatten_error:
            logger.warning(f"  [WARNING] Could not flatten PDF: {flatten_error}")
        
        logger.info(f"  [OK] Contract generated successfully: {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"  [ERROR] Error generating contract with fillpdf: {e}")
        raise

def get_pricing_values(application, pet_type, weight_category, program):
    """Get the EXACT pricing values from the official pricing table"""
    
    # EXACT pricing breakdown from the official table - NO APPROXIMATIONS!
    DOG_PRICING = {
        'silver': {
            '10': {'net_premium': 100.16, 'management_fee': 30.05, 'auxiliary_fund': 0.80, 'ipt': 19.53, 'final': 166.75},
            '11-20': {'net_premium': 125.20, 'management_fee': 37.56, 'auxiliary_fund': 1.00, 'ipt': 24.41, 'final': 207.20},
            '21-40': {'net_premium': 141.88, 'management_fee': 42.56, 'auxiliary_fund': 1.13, 'ipt': 27.67, 'final': 234.14},
            '>40': {'net_premium': 154.40, 'management_fee': 46.32, 'auxiliary_fund': 1.24, 'ipt': 30.11, 'final': 254.36}
        },
        'gold': {
            '10': {'net_premium': 141.88, 'management_fee': 42.56, 'auxiliary_fund': 1.13, 'ipt': 27.67, 'final': 234.14},
            '11-20': {'net_premium': 158.57, 'management_fee': 47.57, 'auxiliary_fund': 1.27, 'ipt': 30.92, 'final': 261.09},
            '21-40': {'net_premium': 175.27, 'management_fee': 52.58, 'auxiliary_fund': 1.40, 'ipt': 34.18, 'final': 288.05},
            '>40': {'net_premium': 187.78, 'management_fee': 56.33, 'auxiliary_fund': 1.50, 'ipt': 36.62, 'final': 308.26}
        },
        'platinum': {
            '10': {'net_premium': 225.34, 'management_fee': 67.60, 'auxiliary_fund': 1.80, 'ipt': 43.94, 'final': 368.92},
            '11-20': {'net_premium': 237.87, 'management_fee': 71.36, 'auxiliary_fund': 1.90, 'ipt': 46.38, 'final': 389.15},
            '21-40': {'net_premium': 250.38, 'management_fee': 75.11, 'auxiliary_fund': 2.00, 'ipt': 48.82, 'final': 409.36},
            '>40': {'net_premium': 267.07, 'management_fee': 80.12, 'auxiliary_fund': 2.14, 'ipt': 52.08, 'final': 436.32}
        }
    }
    
    CAT_PRICING = {
        'silver': {
            '10': {'net_premium': 67.37, 'management_fee': 20.21, 'auxiliary_fund': 0.54, 'ipt': 13.14, 'final': 113.81},
            '11-20': {'net_premium': 84.22, 'management_fee': 25.27, 'auxiliary_fund': 0.67, 'ipt': 16.42, 'final': 141.02}
        },
        'gold': {
            '10': {'net_premium': 101.07, 'management_fee': 30.32, 'auxiliary_fund': 0.81, 'ipt': 19.71, 'final': 168.22},
            '11-20': {'net_premium': 113.69, 'management_fee': 34.11, 'auxiliary_fund': 0.91, 'ipt': 22.17, 'final': 188.61}
        },
        'platinum': {
            '10': {'net_premium': 168.44, 'management_fee': 50.53, 'auxiliary_fund': 1.35, 'ipt': 32.84, 'final': 277.02},
            '11-20': {'net_premium': 189.49, 'management_fee': 56.85, 'auxiliary_fund': 1.52, 'ipt': 36.95, 'final': 311.02}
        }
    }
    
    # Map weight categories from model to pricing table keys
    weight_mapping = {
        'up_10': '10',
        '10_25': '11-20', 
        '25_40': '21-40',
        'over_40': '>40'
    }
    
    # Get the correct pricing table
    pricing_table = DOG_PRICING if pet_type == 'dog' else CAT_PRICING
    
    # Map weight category
    mapped_weight = weight_mapping.get(weight_category, weight_category)
    
    # Get EXACT pricing for the specific program and weight
    if program in pricing_table and mapped_weight in pricing_table[program]:
        pricing_data = pricing_table[program][mapped_weight]
        return (pricing_data['net_premium'], 
                pricing_data['management_fee'], 
                pricing_data.get('auxiliary_fund', 0.0),  # ΤΕΑ-ΕΑΠΑΕΕ (0.8%)
                pricing_data['ipt'], 
                pricing_data['final'])
    
    # Fallback to calculated values if not found in table
    if application.annual_premium:
        final_price = float(application.annual_premium)
        # Use standard breakdown as fallback
        net_premium = final_price * 0.60  # Approximate from table ratios
        management_fee = final_price * 0.20
        # Calculate auxiliary fund (0.8% of reference premium)
        reference_premium = net_premium / 0.6
        auxiliary_fund = reference_premium * 0.008
        ipt = final_price * 0.15
        return net_premium, management_fee, auxiliary_fund, ipt, final_price
    
    return 0.0, 0.0, 0.0, 0.0, 0.0

def create_contract_field_mapping(application, pet_name, pet_type_display, pet_breed, 
                                pet_weight, pet_birthdate, contract_suffix, 
                                net_premium, fee, auxiliary, tax):
    """Create field mapping for the fillable PDF contract
    
    Based on the Greek insurance contract template structure.
    Field names correspond to the actual form field names in the PDF.
    """
    import logging
    logger = logging.getLogger(__name__)
    
    # Get the correct pricing values based on weight category and program
    pet_type_code = 'dog' if 'Σκύλος' in pet_type_display else 'cat'
    weight_category = application.pet_weight_category if contract_suffix != "-PET2" else application.second_pet_weight_category
    program = application.program
    
    # Get EXACT pricing values from the official pricing table (includes auxiliary fund)
    correct_net_premium, correct_management_fee, auxiliary_fund, correct_ipt, base_final_price = get_pricing_values(application, pet_type_code, weight_category, program)
    
    # Use the ACTUAL final price from application (includes surcharges and extra features)
    actual_final_price = float(application.annual_premium) if application.annual_premium else base_final_price
    
    # Calculate surcharges/discounts for display in ΕΚΠΤΩΣΕΙΣ | ΕΠΙΒΑΡΥΝΣΕΙΣ section
    surcharges_discounts = []
    
    # Initialize add-on fields (for the 2 fields beneath in PDF)
    addon_poisoning = ""
    addon_blood = ""
    
    # Check for breed surcharges - try to get questionnaire
    try:
        # Try to access questionnaire via relationship
        questionnaire = None
        if hasattr(application, 'questionnaire'):
            try:
                questionnaire = application.questionnaire
            except Exception:
                # If questionnaire doesn't exist, try to get it directly
                from .models import Questionnaire
                try:
                    questionnaire = Questionnaire.objects.get(application=application)
                except Questionnaire.DoesNotExist:
                    questionnaire = None
        
        if questionnaire:
            logger.info(f"  🔍 Found questionnaire ID: {questionnaire.id}")
            logger.info(f"  🔍 special_breed_5_percent: {questionnaire.special_breed_5_percent} (type: {type(questionnaire.special_breed_5_percent)})")
            logger.info(f"  🔍 special_breed_20_percent: {questionnaire.special_breed_20_percent} (type: {type(questionnaire.special_breed_20_percent)})")
            logger.info(f"  🔍 additional_poisoning_coverage: {questionnaire.additional_poisoning_coverage} (type: {type(questionnaire.additional_poisoning_coverage)})")
            logger.info(f"  🔍 additional_blood_checkup: {questionnaire.additional_blood_checkup} (type: {type(questionnaire.additional_blood_checkup)})")
            
            # Breed surcharges first (5% and 20%)
            # Only show the ones that are actually True
            # Calculate 20% on price AFTER 5% is applied (if 5% is active)
            price_after_surcharges = base_final_price
            
            # Check if 5% is actually True (not just truthy)
            if questionnaire.special_breed_5_percent is True:
                surcharge_5 = base_final_price * 0.05
                price_after_surcharges = base_final_price * 1.05
                surcharges_discounts.append(f"+{surcharge_5:.2f}€ (Επασφάλιστρο 5%)")
                logger.info(f"  [OK] Added 5% surcharge: {surcharge_5:.2f}€")
            
            # Check if 20% is actually True (not just truthy) - only if it's selected
            if questionnaire.special_breed_20_percent is True:
                # Calculate 20% on the price AFTER 5% surcharge (if 5% was applied)
                surcharge_20 = price_after_surcharges * 0.20
                surcharges_discounts.append(f"+{surcharge_20:.2f}€ (Επασφάλιστρο 20%)")
                logger.info(f"  [OK] Added 20% surcharge: {surcharge_20:.2f}€ (calculated on price after 5%: {price_after_surcharges:.2f}€)")
            
            # Add-ons below breed surcharges (poisoning coverage and blood checkup)
            # Store separately for the 2 fields beneath in PDF (text_31mdpf and text_32crsg)
            if questionnaire.additional_poisoning_coverage is True:
                poisoning_prices = {'silver': 18, 'gold': 20, 'platinum': 25, 'dynasty': 25}
                poisoning_price = poisoning_prices.get(program, 18)
                addon_poisoning = f"+{poisoning_price:.2f}€ (Δηλητηρίαση)"
                # Don't add to surcharges_discounts - goes in separate field text_31mdpf
                logger.info(f"  [OK] Added poisoning coverage: {poisoning_price:.2f}€ (will go in text_31mdpf)")
            
            if questionnaire.additional_blood_checkup is True:
                addon_blood = f"+28.00€ (Αιματολογικό Check Up)"
                # Don't add to surcharges_discounts - goes in separate field text_32crsg
                logger.info(f"  [OK] Added blood checkup: 28.00€ (will go in text_32crsg)")
        else:
            logger.warning(f"  ⚠️ No questionnaire found for application {application.id}")
    except Exception as e:
        import traceback
        logger.error(f"  [ERROR] Error accessing questionnaire: {e}")
        logger.error(traceback.format_exc())
    
    # Calculate discount for second pet (if applicable)
    if contract_suffix == "-PET2" and application.has_second_pet:
        # Calculate discount amount
        original_price = actual_final_price / 0.95  # Reverse the 5% discount
        discount = original_price - actual_final_price
        surcharges_discounts.append(f"-{discount:.2f}€ (2ο κατοικίδιο)")
    
    # Format surcharges/discounts for display
    surcharges_text = "\n".join(surcharges_discounts) if surcharges_discounts else ""
    logger.info(f"  [INFO] Surcharges/Discounts text: '{surcharges_text}'")
    logger.info(f"  [INFO] Number of surcharges: {len(surcharges_discounts)}")
    
    # Use EXACT IPT from the official pricing table (proportionally adjusted if price changed)
    # If actual price differs from base, adjust IPT proportionally
    if actual_final_price != base_final_price and base_final_price > 0:
        price_multiplier = actual_final_price / base_final_price
        ipt_amount = correct_ipt * price_multiplier
    else:
        ipt_amount = correct_ipt
    
    # Text field mappings - NEW TEMPLATE (ΑΣΦΑΛΙΣΤΗΡΙΟ ΣΥΜΒΟΛΑΙΟ ΤΕΛΙΚΟ PET (1) (2).pdf)
    # Map to new field names while keeping same data structure
    data = {
        # Header section
        "text_1bwie": application.contract_number or '',                # Contract number
        "text_2pcpc": '',                                              # Receipt number - not used (no active payment system)
        "text_3ksjz": application.full_name or '',                     # Client name
        "text_4yiws": '',                                              # Payment code - not used (no active payment system)
        "text_5fgpc": application.contract_start_date.strftime('%d/%m/%Y') if application.contract_start_date else '',  # Start date
        "text_6zqkn": application.contract_end_date.strftime('%d/%m/%Y') if application.contract_end_date else '',     # End date
        "text_7tbbt": application.get_program_with_frequency_display() or '',    # Program name with payment frequency (e.g., "Ασημένιο Ετήσιο")
        
        # Client information section
        "text_8safe": application.full_name or '',                       # Client Full Name
        "text_9vyoe": application.afm or '',                           # AFM
        "text_10eqtr": application.phone or '',                        # Phone number
        "text_11qthp": application.address or '',                      # Address
        "text_12ul": application.postal_code or '',                  # Postal code
        "text_13liqu": application.email or '',                        # Email
        
        # Pet information section
        "text_14rclu": pet_name or '',                                 # Pet name
        "text_15vsin": pet_type_display or '',                         # Pet type
        "text_16jfkm": pet_breed or '',                                 # Breed
        "text_17ltlp": pet_weight or '',                               # Pet weight category
        "text_18yuy": pet_birthdate or '',                            # Pet birthdate
        "text_19nqjo": application.microchip_number or '',             # Microchip number
        
        # Premium breakdown section
        "text_29bsjj": "",                                             # Empty
        "text_30vzyv": surcharges_text,                                # ΕΚΠΤΩΣΕΙΣ | ΕΠΙΒΑΡΥΝΣΕΙΣ (surcharges/discounts - breed surcharges only)
        "text_31mdpf": addon_poisoning,  # Add-on: Poisoning coverage (field beneath)
        "text_32crsg": addon_blood,  # Add-on: Blood checkup (field beneath)
        "text_33tjdu": f"{correct_net_premium:.2f}€",                  # Net Premium from pricing table
        "text_34k": f"{correct_management_fee:.2f}€",               # Management Fee from pricing table
        "text_35poeh": f"{auxiliary_fund:.2f}€",                     # Επικουρικό (ΤΕΑ-ΕΑΠΑΕΕ 0.8%) from pricing table - for display only (already included in final price)
        "text_36sfw": f"{ipt_amount:.2f}€",                           # IPT (adjusted if surcharges applied)
        "text_37rpnu": f"{actual_final_price:.2f}€",  # ACTUAL final price (includes surcharges and extra features)
    }
    
    # Checkbox mappings for coverage options - NEW TEMPLATE
    # All coverage options are checked for all programs
    # Export value from PDF: 'Yes_sexk'
    checkbox_data = {
        # Coverage checkboxes (ΚΑΛΥΠΤΟΜΕΝΟΙ ΚΙΝΔΥΝΟΙ / ΠΡΟΣΘΕΤΕΣ ΠΑΡΟΧΕΣ)
        "checkbox_20jmec": "Yes_sexk",  # Ιατροφαρμακευτική Περίθαλψη
        "checkbox_21jvmm": "Yes_sexk",  # (Coverage option - likely Κάλυψη Κατοικιδίου από Ατύχημα και Ασθένεια)
        "checkbox_22cjxd": "Yes_sexk",  # Διάγνωση με Hoolie AI
        "checkbox_23cdss": "Yes_sexk",  # Αποκατάσταση
        "checkbox_24bmgz": "Yes_sexk",  # (Coverage option - likely Απώλεια Διαβατηρίου)
        "checkbox_25yhjf": "Yes_sexk",  # Νομική Προστασία Ιδιοκτήτη Κατοικιδίου
        "checkbox_26wldx": "Yes_sexk",  # Κάλυψη Αποχαιρετισμού
        "checkbox_27sj": "Yes_sexk",  # Επείγοντα / Νοσηλείες
        "checkbox_28okyh": "Yes_sexk",  # Απώλεια / Κλοπή
    }
    
    # Combine text and checkbox data
    data.update(checkbox_data)
    
    # Log the mapping for debugging
    print(f"  [INFO] Field mapping created with {len(data)} fields")
    print(f"  [*] Contract: {data.get('text_1bwie', 'N/A')}")
    print(f"  [*] Client: {data.get('text_8safe', 'N/A')}")
    print(f"  [*] Pet: {data.get('text_14rclu', 'N/A')} ({data.get('text_15vsin', 'N/A')})")
    print(f"  [*] Program + Frequency: {data.get('text_7tbbt', 'N/A')}")
    print(f"  [*] Net Premium: {data.get('text_33tjdu', 'N/A')}")
    print(f"  [*] Management Fee: {data.get('text_34k', 'N/A')}")
    print(f"  [*] Auxiliary Fund (ΤΕΑ-ΕΑΠΑΕΕ): {data.get('text_35poeh', 'N/A')}")
    print(f"  [*] Final Price (from table): {base_final_price:.2f}€")
    print(f"  [*] Actual Final Price (with surcharges): {actual_final_price:.2f}€")
    print(f"  [*] IPT: {data.get('text_36sfw', 'N/A')}")
    print(f"  [*] Total Paid: {data.get('text_37rpnu', 'N/A')}")
    if surcharges_text:
        print(f"  [*] Surcharges/Discounts: {surcharges_text}")
    
    return data

def test_fillpdf_generation():
    """Test function to verify fillpdf works correctly"""
    
    template_path = "ασφαλιστηριο συμβολαιο κατοικοιδιου (2).pdf"
    output_path = "test_fillpdf_output.pdf"
    
    # Sample test data
    test_data = {
        "text_1avcg": "HOL-2025-TEST001",
        "text_2zncn": "REC-TEST-001", 
        "text_3fzya": "Δημήτρης Ζουρμούδης",
        "text_4terx": "PAY-TEST-123456",
        "text_5fwyk": "Δημήτρης Ζουρμούδης",
        "text_11fgkt": "Μπάντι",
        "text_12lquc": "Σκύλος",
        "text_17qimv": "Χρυσό",
        "text_34zqyp": "664.06€",
        "checkbox_20eqnd": "Yes_vfmt",
        "checkbox_22jvbr": "Yes_zjqp",
        "checkbox_23crbw": "Yes_zjqp",
    }
    
    try:
        fillpdfs.write_fillable_pdf(
            template_path,
            output_path,
            data_dict=test_data,
            flatten=True,
        )
        print(f"[OK] Test PDF generated: {output_path}")
        return True
    except Exception as e:
        print(f"[ERROR] Test failed: {e}")
        return False
