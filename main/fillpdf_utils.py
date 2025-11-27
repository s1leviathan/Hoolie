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
    
    print(f"  📄 Generating contract with fillpdf (Pet {pet_number})...")
    
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
        print(f"  📋 Using Pet 2 data: {pet_name} ({pet_type_display})")
    else:
        pet_name = application.pet_name
        pet_type_display = application.get_pet_type_display_greek()
        pet_breed = application.pet_breed
        pet_weight = application.get_weight_display(application.pet_weight_category) if application.pet_weight_category else ''
        pet_birthdate = application.pet_birthdate.strftime('%d/%m/%Y') if application.pet_birthdate else ''
        contract_suffix = "-PET1" if application.has_second_pet else ""
        print(f"  📋 Using Pet 1 data: {pet_name} ({pet_type_display})")
    
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
        print(f"  🔧 Filling PDF form with {len(data)} fields...")
        
        fillpdfs.write_fillable_pdf(
            template_path,
            output_path,
            data_dict=data,
            flatten=True,  # Make fields non-editable (baked into PDF)
        )
        
        print(f"  ✅ Contract generated successfully: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"  ❌ Error generating contract with fillpdf: {e}")
        raise

def get_pricing_values(application, pet_type, weight_category, program):
    """Get the EXACT pricing values from the official pricing table"""
    
    # EXACT pricing breakdown from the official table - NO APPROXIMATIONS!
    DOG_PRICING = {
        'silver': {
            '10': {'net_premium': 100.16, 'management_fee': 30.05, 'ipt': 19.53, 'final': 166.75},
            '11-20': {'net_premium': 125.20, 'management_fee': 37.56, 'ipt': 24.41, 'final': 207.20},
            '21-40': {'net_premium': 141.88, 'management_fee': 42.56, 'ipt': 27.67, 'final': 234.14},
            '>40': {'net_premium': 154.40, 'management_fee': 46.32, 'ipt': 30.11, 'final': 254.36}
        },
        'gold': {
            '10': {'net_premium': 141.88, 'management_fee': 42.56, 'ipt': 27.67, 'final': 234.14},
            '11-20': {'net_premium': 158.57, 'management_fee': 47.57, 'ipt': 30.92, 'final': 261.09},
            '21-40': {'net_premium': 175.27, 'management_fee': 52.58, 'ipt': 34.18, 'final': 288.05},
            '>40': {'net_premium': 187.78, 'management_fee': 56.33, 'ipt': 36.62, 'final': 308.26}
        },
        'platinum': {
            '10': {'net_premium': 225.34, 'management_fee': 67.60, 'ipt': 43.94, 'final': 368.92},
            '11-20': {'net_premium': 237.87, 'management_fee': 71.36, 'ipt': 46.38, 'final': 389.15},
            '21-40': {'net_premium': 250.38, 'management_fee': 75.11, 'ipt': 48.82, 'final': 409.36},
            '>40': {'net_premium': 267.07, 'management_fee': 80.12, 'ipt': 52.08, 'final': 436.32}
        }
    }
    
    CAT_PRICING = {
        'silver': {
            '10': {'net_premium': 67.37, 'management_fee': 20.21, 'ipt': 13.14, 'final': 113.81},
            '11-20': {'net_premium': 84.22, 'management_fee': 25.27, 'ipt': 16.42, 'final': 141.02}
        },
        'gold': {
            '10': {'net_premium': 101.07, 'management_fee': 30.32, 'ipt': 19.71, 'final': 168.22},
            '11-20': {'net_premium': 113.69, 'management_fee': 34.11, 'ipt': 22.17, 'final': 188.61}
        },
        'platinum': {
            '10': {'net_premium': 168.44, 'management_fee': 50.53, 'ipt': 32.84, 'final': 277.02},
            '11-20': {'net_premium': 189.49, 'management_fee': 56.85, 'ipt': 36.95, 'final': 311.02}
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
        return pricing_data['net_premium'], pricing_data['management_fee'], pricing_data['ipt'], pricing_data['final']
    
    # Fallback to calculated values if not found in table
    if application.annual_premium:
        final_price = float(application.annual_premium)
        # Use standard breakdown as fallback
        net_premium = final_price * 0.60  # Approximate from table ratios
        management_fee = final_price * 0.20
        ipt = final_price * 0.15
        return net_premium, management_fee, ipt, final_price
    
    return 0.0, 0.0, 0.0, 0.0

def create_contract_field_mapping(application, pet_name, pet_type_display, pet_breed, 
                                pet_weight, pet_birthdate, contract_suffix, 
                                net_premium, fee, auxiliary, tax):
    """Create field mapping for the fillable PDF contract
    
    Based on the Greek insurance contract template structure.
    Field names correspond to the actual form field names in the PDF.
    """
    
    # Get the correct pricing values based on weight category and program
    pet_type_code = 'dog' if 'Σκύλος' in pet_type_display else 'cat'
    weight_category = application.pet_weight_category if contract_suffix != "-PET2" else application.second_pet_weight_category
    program = application.program
    
    # Get EXACT pricing values from the official pricing table
    correct_net_premium, correct_management_fee, correct_ipt, final_price = get_pricing_values(application, pet_type_code, weight_category, program)
    
    # Calculate discount for second pet (if applicable)
    discount_amount = ""
    if contract_suffix == "-PET2" and application.has_second_pet:
        # SIMPLE: Take ΤΕΛΙΚΗ ΤΙΜΗ of second pet, apply -5% discount, show the difference
        
        # final_price = what the user actually pays (discounted price)
        # original_price = full price before 5% discount
        original_price = final_price / 0.95  # Reverse the 5% discount to get original
        discount = original_price - final_price  # The discount amount
        
        # Format the discount amount as requested
        discount_amount = f"-{discount:.2f}€"
    
    # Use EXACT IPT from the official pricing table
    ipt_amount = correct_ipt
    
    # Text field mappings - NEW TEMPLATE (ΑΣΦΑΛΙΣΤΗΡΙΟ ΣΥΜΒΟΛΑΙΟ ΤΕΛΙΚΟ PET (1) (2).pdf)
    # Map to new field names while keeping same data structure
    data = {
        # Header section
        "text_1bwie": application.contract_number or '',                # Contract number
        "text_2pcpc": application.receipt_number or '',                 # Receipt number
        "text_3ksjz": application.full_name or '',                     # Client name
        "text_4yiws": application.payment_code or '',                  # Payment code
        "text_5fgpc": application.contract_start_date.strftime('%d/%m/%Y') if application.contract_start_date else '',  # Start date
        "text_6zqkn": application.contract_end_date.strftime('%d/%m/%Y') if application.contract_end_date else '',     # End date
        "text_7tbbt": application.get_program_display_greek() or '',    # Program name
        
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
        "text_30vzyv": discount_amount,                                # Discount for second pet (or empty)
        "text_31mdpf": "",                                             # Empty
        "text_32crsg": "",                                             # Empty
        "text_33tjdu": f"{correct_net_premium:.2f}€",                  # Net Premium from pricing table
        "text_34k": f"{correct_management_fee:.2f}€",               # Management Fee from pricing table
        "text_35poeh": "",                                             # Empty
        "text_36sfw": f"{ipt_amount:.2f}€",                           # IPT from pricing table
        "text_37rpnu": f"{final_price:.2f}€",  # EXACT total from official pricing table
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
    print(f"  📋 Field mapping created with {len(data)} fields")
    print(f"  🔹 Contract: {data.get('text_1bwie', 'N/A')}")
    print(f"  🔹 Client: {data.get('text_8safe', 'N/A')}")
    print(f"  🔹 Pet: {data.get('text_14rclu', 'N/A')} ({data.get('text_15vsin', 'N/A')})")
    print(f"  🔹 Program: {data.get('text_7tbbt', 'N/A')}")
    print(f"  🔹 Net Premium: {data.get('text_33tjdu', 'N/A')}")
    print(f"  🔹 Management Fee: {data.get('text_34k', 'N/A')}")
    print(f"  🔹 Final Price (from table): {final_price:.2f}€")
    print(f"  🔹 IPT: {data.get('text_36sfw', 'N/A')}")
    print(f"  🔹 Total Paid: {data.get('text_37rpnu', 'N/A')}")
    if discount_amount:
        print(f"  🔹 Discount: {discount_amount}")
    
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
        print(f"✅ Test PDF generated: {output_path}")
        return True
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
