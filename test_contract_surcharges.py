#!/usr/bin/env python3
"""
Test contract generation with surcharges locally
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pet_insurance.settings')
django.setup()

from main.fillpdf_utils import generate_contract_with_fillpdf, create_contract_field_mapping
from datetime import datetime, date, timedelta
from decimal import Decimal

# Create a mock application with questionnaire
class MockApplication:
    def __init__(self):
        self.id = 999
        self.contract_number = 'HOL-2025-TEST-SURCHARGES'
        self.receipt_number = 'REC-TEST-001'
        self.payment_code = 'PAY-TEST-001'
        self.full_name = 'Test User'
        self.afm = '123456789'
        self.phone = '2101234567'
        self.email = 'test@example.com'
        self.address = 'Test Address 123'
        self.postal_code = '10441'
        self.pet_name = 'Test Pet'
        self.pet_type = 'dog'
        self.pet_breed = 'Pit Bull'
        self.microchip_number = '123456789012345'
        self.program = 'gold'
        self.contract_start_date = date.today()
        self.contract_end_date = date.today() + timedelta(days=365)
        self.has_second_pet = False
        self.pet_weight_category = '11-20'
        self.annual_premium = Decimal('313.31')  # Base 261.09 + 20% (52.22) = 313.31
        self.microchip_number = '123456789012345'
        self.pet_birthdate = date(2020, 1, 1)
        
    def get_program_display_greek(self):
        return 'Χρυσό'
    
    def get_pet_type_display_greek(self):
        return 'Σκύλος'
    
    def get_weight_display(self, weight_category):
        weight_map = {
            '10': 'έως 10 κιλά',
            '11-20': '11-20 κιλά',
            '21-40': '21-40 κιλά',
            '>40': '>40 κιλά'
        }
        return weight_map.get(weight_category, weight_category)
    
    # Mock questionnaire
    class MockQuestionnaire:
        def __init__(self):
            self.id = 999
            self.special_breed_5_percent = False
            self.special_breed_20_percent = True  # 20% surcharge
            self.additional_poisoning_coverage = True  # +20€ for gold
            self.additional_blood_checkup = True  # +28€
    
    @property
    def questionnaire(self):
        return self.MockQuestionnaire()

def test_contract_surcharges():
    print("=" * 80)
    print("TESTING CONTRACT GENERATION WITH SURCHARGES")
    print("=" * 80)
    print()
    
    # Create mock application
    app = MockApplication()
    
    print(f"📋 Application Details:")
    print(f"  Contract: {app.contract_number}")
    print(f"  Pet: {app.pet_name} ({app.pet_breed})")
    print(f"  Program: {app.program}")
    print(f"  Base Price: 261.09€")
    print(f"  Annual Premium (with surcharges): {app.annual_premium}€")
    print()
    
    print(f"📋 Questionnaire Surcharges:")
    print(f"  Special Breed 5%: {app.questionnaire.special_breed_5_percent}")
    print(f"  Special Breed 20%: {app.questionnaire.special_breed_20_percent}")
    print(f"  Poisoning Coverage: {app.questionnaire.additional_poisoning_coverage}")
    print(f"  Blood Checkup: {app.questionnaire.additional_blood_checkup}")
    print()
    
    # Test the field mapping function directly
    print("🔧 Testing create_contract_field_mapping...")
    print()
    
    try:
        pet_name = app.pet_name
        pet_type_display = app.get_pet_type_display_greek()
        pet_breed = app.pet_breed
        pet_weight = '11-20 κιλά'
        pet_birthdate = '01/01/2020'
        contract_suffix = ""
        
        # These values don't matter for surcharges calculation
        net_premium = 158.57
        fee = 47.57
        auxiliary = 1.27
        tax = 30.92
        
        data = create_contract_field_mapping(
            app, pet_name, pet_type_display, pet_breed, 
            pet_weight, pet_birthdate, contract_suffix,
            net_premium, fee, auxiliary, tax
        )
        
        print("✅ Field mapping created successfully")
        print()
        print("📊 Contract Field Values:")
        print(f"  text_30vzyv (ΕΚΠΤΩΣΕΙΣ | ΕΠΙΒΑΡΥΝΣΕΙΣ): '{data.get('text_30vzyv', 'EMPTY')}'")
        print(f"  text_37rpnu (Total): '{data.get('text_37rpnu', 'EMPTY')}'")
        print()
        
        # Check if surcharges are present
        surcharges_text = data.get('text_30vzyv', '')
        if surcharges_text:
            print("✅ SUCCESS: Surcharges are present in the contract!")
            print(f"   Content: {surcharges_text}")
        else:
            print("❌ FAILED: Surcharges text is empty!")
            print("   This means the surcharges are not being calculated/displayed")
        
        print()
        
        # Now test full contract generation
        print("🔧 Testing full contract generation...")
        output_path = os.path.join(os.getcwd(), 'test_contracts', f'contract_surcharges_test_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf')
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        generate_contract_with_fillpdf(app, output_path, pet_number=1)
        
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"✅ Contract generated: {output_path}")
            print(f"   Size: {file_size:,} bytes")
        else:
            print(f"❌ Contract file not found: {output_path}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    print("=" * 80)

if __name__ == '__main__':
    test_contract_surcharges()

