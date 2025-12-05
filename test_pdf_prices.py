#!/usr/bin/env python
"""
Test script to verify PDF generation uses correct prices for payment frequencies
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

def test_pdf_prices():
    """Test that PDF field mapping uses correct prices for all payment frequencies"""
    
    print("=" * 80)
    print("TESTING PDF PRICE GENERATION")
    print("=" * 80)
    
    # Test scenarios
    scenarios = [
        {
            'name': 'Dog Silver ≤10kg - Annual',
            'pet_type': 'dog',
            'program': 'silver',
            'weight': 'up_10',
            'frequency': 'annual',
            'expected_total': 166.75,
        },
        {
            'name': 'Dog Silver ≤10kg - 6-Month',
            'pet_type': 'dog',
            'program': 'silver',
            'weight': 'up_10',
            'frequency': 'six_month',
            'expected_total': 87.54,  # 166.75 * 0.525
        },
        {
            'name': 'Dog Silver ≤10kg - 3-Month',
            'pet_type': 'dog',
            'program': 'silver',
            'weight': 'up_10',
            'frequency': 'three_month',
            'expected_total': 45.86,  # 166.75 * 0.275
        },
        {
            'name': 'Dog Gold ≤10kg - 6-Month',
            'pet_type': 'dog',
            'program': 'gold',
            'weight': 'up_10',
            'frequency': 'six_month',
            'expected_total': 122.92,  # 234.14 * 0.525
        },
    ]
    
    all_passed = True
    
    for scenario in scenarios:
        print(f"\n{'='*80}")
        print(f"TEST: {scenario['name']}")
        print(f"{'='*80}")
        
        try:
            # Create application
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
            
            print(f"✓ Created application: {app.contract_number}")
            
            # Create questionnaire with payment frequency
            questionnaire = Questionnaire.objects.create(
                application=app,
                payment_frequency=scenario['frequency'],
                program=scenario['program'],
            )
            
            print(f"✓ Created questionnaire with frequency: {scenario['frequency']}")
            
            # Refresh application to get updated premiums
            app.refresh_from_db()
            
            # Get premium for frequency
            premium_for_freq = app.get_premium_for_frequency()
            print(f"✓ get_premium_for_frequency() = {premium_for_freq:.2f}€")
            
            # Generate PDF field mapping
            field_mapping = create_contract_field_mapping(
                application=app,
                pet_name="TestPet",
                pet_type_display="Σκύλος",
                pet_breed="Test Breed",
                pet_weight="έως 10 κιλά",
                pet_birthdate="01/01/2020",
                contract_suffix="",
                net_premium=0,  # Will be recalculated
                fee=0,
                auxiliary=0,
                tax=0,
            )
            
            # Extract total price from PDF field
            total_price_str = field_mapping.get('text_37rpnu', '0€')
            # Remove '€' and convert to float
            total_price = float(total_price_str.replace('€', '').strip())
            
            print(f"\n📄 PDF Field Values:")
            print(f"   text_33tjdu (Net Premium):     {field_mapping.get('text_33tjdu', 'N/A')}")
            print(f"   text_34k (Management Fee):    {field_mapping.get('text_34k', 'N/A')}")
            print(f"   text_35poeh (Auxiliary):      {field_mapping.get('text_35poeh', 'N/A')}")
            print(f"   text_36sfw (IPT):              {field_mapping.get('text_36sfw', 'N/A')}")
            print(f"   text_37rpnu (TOTAL):           {field_mapping.get('text_37rpnu', 'N/A')}")
            print(f"   text_7tbbt (Program):          {field_mapping.get('text_7tbbt', 'N/A')}")
            
            # Verify
            expected = scenario['expected_total']
            price_ok = abs(total_price - expected) < 0.01
            
            if price_ok:
                print(f"\n✅ PASS: PDF total price is correct ({total_price:.2f}€ = {expected:.2f}€)")
            else:
                print(f"\n❌ FAIL: PDF total price is incorrect!")
                print(f"   Expected: {expected:.2f}€")
                print(f"   Got:      {total_price:.2f}€")
                print(f"   Difference: {abs(total_price - expected):.2f}€")
                all_passed = False
            
            # Verify program display includes frequency
            program_display = field_mapping.get('text_7tbbt', '')
            if scenario['frequency'] == 'annual':
                expected_display = 'Ασημένιο Ετήσιο' if scenario['program'] == 'silver' else 'Χρυσό Ετήσιο'
            elif scenario['frequency'] == 'six_month':
                expected_display = 'Ασημένιο Εξαμηνιαίο' if scenario['program'] == 'silver' else 'Χρυσό Εξαμηνιαίο'
            else:  # three_month
                expected_display = 'Ασημένιο Τριμηνιαίο' if scenario['program'] == 'silver' else 'Χρυσό Τριμηνιαίο'
            
            if program_display == expected_display:
                print(f"✅ PASS: Program display is correct ({program_display})")
            else:
                print(f"❌ FAIL: Program display is incorrect!")
                print(f"   Expected: {expected_display}")
                print(f"   Got:      {program_display}")
                all_passed = False
            
            # Clean up
            app.delete()
            print(f"✓ Cleaned up test data")
            
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
            all_passed = False
    
    print(f"\n{'='*80}")
    if all_passed:
        print("✅ ALL TESTS PASSED!")
    else:
        print("❌ SOME TESTS FAILED!")
    print(f"{'='*80}")
    
    return all_passed

if __name__ == '__main__':
    success = test_pdf_prices()
    sys.exit(0 if success else 1)

