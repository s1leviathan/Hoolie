#!/usr/bin/env python
"""
REAL FLOW TEST - Simulates the actual user flow to verify prices in PDF
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pet_insurance.settings')
django.setup()

from main.models import InsuranceApplication, Questionnaire
from main.fillpdf_utils import create_contract_field_mapping
from decimal import Decimal

def test_real_flow():
    """Test the REAL flow: Create app -> Save questionnaire -> Check PDF prices"""
    
    print("=" * 80)
    print("REAL FLOW TEST - Simulating Actual User Journey")
    print("=" * 80)
    
    scenarios = [
        {
            'name': '6-Month Payment - Dog Silver ≤10kg',
            'pet_type': 'dog',
            'program': 'silver',
            'weight': 'up_10',
            'frequency': 'six_month',
            'expected_price': 87.54,  # 166.75 * 0.525
        },
        {
            'name': '3-Month Payment - Dog Silver ≤10kg',
            'pet_type': 'dog',
            'program': 'silver',
            'weight': 'up_10',
            'frequency': 'three_month',
            'expected_price': 45.86,  # 166.75 * 0.275
        },
    ]
    
    all_passed = True
    
    for scenario in scenarios:
        print(f"\n{'='*80}")
        print(f"TEST: {scenario['name']}")
        print(f"{'='*80}")
        
        try:
            # STEP 1: Create application (as if user filled out form)
            print("\n[STEP 1] Creating application...")
            app = InsuranceApplication.objects.create(
                full_name="Test User",
                afm="123456789",
                phone="6912345678",
                address="Test Address",
                postal_code="12345",
                email="test@example.com",
                pet_name="TestPet",
                pet_type=scenario['pet_type'],
                pet_gender='male',
                pet_breed="Test Breed",
                pet_birthdate="2020-01-01",
                pet_weight_category=scenario['weight'],
                program=scenario['program'],
                health_status='healthy',
            )
            print(f"✓ Application created: {app.contract_number}")
            print(f"  Annual premium: {app.annual_premium}")
            print(f"  6-Month premium: {app.six_month_premium}")
            print(f"  3-Month premium: {app.three_month_premium}")
            
            # STEP 2: Save questionnaire with payment frequency (as if user selected it)
            print(f"\n[STEP 2] Saving questionnaire with frequency: {scenario['frequency']}...")
            questionnaire = Questionnaire.objects.create(
                application=app,
                payment_frequency=scenario['frequency'],
                program=scenario['program'],
            )
            print(f"✓ Questionnaire saved")
            
            # STEP 3: Refresh application and check premiums
            print(f"\n[STEP 3] Checking premiums after questionnaire save...")
            app.refresh_from_db()
            print(f"  Annual premium: {app.annual_premium}")
            print(f"  6-Month premium: {app.six_month_premium}")
            print(f"  3-Month premium: {app.three_month_premium}")
            
            # STEP 4: Check get_premium_for_frequency
            print(f"\n[STEP 4] Checking get_premium_for_frequency()...")
            premium_for_freq = app.get_premium_for_frequency()
            print(f"  get_premium_for_frequency() = {premium_for_freq:.2f}€")
            print(f"  Expected: {scenario['expected_price']:.2f}€")
            
            if abs(premium_for_freq - scenario['expected_price']) < 0.01:
                print(f"  ✅ CORRECT!")
            else:
                print(f"  ❌ WRONG! Difference: {abs(premium_for_freq - scenario['expected_price']):.2f}€")
                all_passed = False
            
            # STEP 5: Generate PDF field mapping (as if generating contract)
            print(f"\n[STEP 5] Generating PDF field mapping...")
            field_mapping = create_contract_field_mapping(
                application=app,
                pet_name="TestPet",
                pet_type_display="Σκύλος",
                pet_breed="Test Breed",
                pet_weight="έως 10 κιλά",
                pet_birthdate="01/01/2020",
                contract_suffix="",
                net_premium=0,
                fee=0,
                auxiliary=0,
                tax=0,
            )
            
            # STEP 6: Check PDF total price
            print(f"\n[STEP 6] Checking PDF total price...")
            total_price_str = field_mapping.get('text_37rpnu', '0€')
            total_price = float(total_price_str.replace('€', '').strip())
            print(f"  PDF Total (text_37rpnu): {total_price:.2f}€")
            print(f"  Expected: {scenario['expected_price']:.2f}€")
            
            if abs(total_price - scenario['expected_price']) < 0.01:
                print(f"  ✅ PDF PRICE IS CORRECT!")
            else:
                print(f"  ❌ PDF PRICE IS WRONG!")
                print(f"     Difference: {abs(total_price - scenario['expected_price']):.2f}€")
                all_passed = False
            
            # Show all PDF price fields
            print(f"\n📄 PDF Price Fields:")
            print(f"   Net Premium (text_33tjdu):     {field_mapping.get('text_33tjdu', 'N/A')}")
            print(f"   Management Fee (text_34k):     {field_mapping.get('text_34k', 'N/A')}")
            print(f"   Auxiliary (text_35poeh):       {field_mapping.get('text_35poeh', 'N/A')}")
            print(f"   IPT (text_36sfw):              {field_mapping.get('text_36sfw', 'N/A')}")
            print(f"   TOTAL (text_37rpnu):           {field_mapping.get('text_37rpnu', 'N/A')}")
            print(f"   Program (text_7tbbt):          {field_mapping.get('text_7tbbt', 'N/A')}")
            
            # Clean up
            app.delete()
            print(f"\n✓ Cleaned up test data")
            
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
            all_passed = False
    
    print(f"\n{'='*80}")
    if all_passed:
        print("✅ ALL REAL FLOW TESTS PASSED!")
    else:
        print("❌ SOME REAL FLOW TESTS FAILED!")
    print(f"{'='*80}")
    
    return all_passed

if __name__ == '__main__':
    success = test_real_flow()
    sys.exit(0 if success else 1)

