#!/usr/bin/env python
"""
Test script to verify payment frequency prices are correctly calculated and displayed
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pet_insurance.settings')
django.setup()

from main.models import InsuranceApplication, Questionnaire
from decimal import Decimal

def test_payment_frequency_prices():
    """Test that premiums are correctly calculated for all payment frequencies"""
    
    print("=" * 80)
    print("TESTING PAYMENT FREQUENCY PRICES")
    print("=" * 80)
    
    # Test scenarios
    scenarios = [
        {
            'name': 'Dog Silver ≤10kg - Annual',
            'pet_type': 'dog',
            'program': 'silver',
            'weight': 'up_10',
            'frequency': 'annual',
            'expected_annual': 166.75,
            'expected_6month': 87.54,  # 166.75 * 0.525
            'expected_3month': 45.86,  # 166.75 * 0.275
        },
        {
            'name': 'Dog Silver ≤10kg - 6-Month',
            'pet_type': 'dog',
            'program': 'silver',
            'weight': 'up_10',
            'frequency': 'six_month',
            'expected_annual': 166.75,
            'expected_6month': 87.54,
            'expected_3month': 45.86,
        },
        {
            'name': 'Dog Silver ≤10kg - 3-Month',
            'pet_type': 'dog',
            'program': 'silver',
            'weight': 'up_10',
            'frequency': 'three_month',
            'expected_annual': 166.75,
            'expected_6month': 87.54,
            'expected_3month': 45.86,
        },
        {
            'name': 'Dog Gold ≤10kg - 6-Month',
            'pet_type': 'dog',
            'program': 'gold',
            'weight': 'up_10',
            'frequency': 'six_month',
            'expected_annual': 234.14,
            'expected_6month': 122.92,  # 234.14 * 0.525
            'expected_3month': 64.39,  # 234.14 * 0.275
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
            
            # Check premiums
            annual = float(app.annual_premium) if app.annual_premium else 0
            six_month = float(app.six_month_premium) if app.six_month_premium else 0
            three_month = float(app.three_month_premium) if app.three_month_premium else 0
            
            print(f"\n📊 Premium Values:")
            print(f"   Annual:      {annual:.2f}€ (expected: {scenario['expected_annual']:.2f}€)")
            print(f"   6-Month:     {six_month:.2f}€ (expected: {scenario['expected_6month']:.2f}€)")
            print(f"   3-Month:     {three_month:.2f}€ (expected: {scenario['expected_3month']:.2f}€)")
            
            # Check get_premium_for_frequency
            premium_for_freq = app.get_premium_for_frequency()
            print(f"\n💰 get_premium_for_frequency() returns: {premium_for_freq:.2f}€")
            
            # Verify
            annual_ok = abs(annual - scenario['expected_annual']) < 0.01
            six_month_ok = abs(six_month - scenario['expected_6month']) < 0.01
            three_month_ok = abs(three_month - scenario['expected_3month']) < 0.01
            
            # Check if get_premium_for_frequency returns the correct value
            if scenario['frequency'] == 'annual':
                freq_ok = abs(premium_for_freq - scenario['expected_annual']) < 0.01
                expected_freq = scenario['expected_annual']
            elif scenario['frequency'] == 'six_month':
                freq_ok = abs(premium_for_freq - scenario['expected_6month']) < 0.01
                expected_freq = scenario['expected_6month']
            else:  # three_month
                freq_ok = abs(premium_for_freq - scenario['expected_3month']) < 0.01
                expected_freq = scenario['expected_3month']
            
            if annual_ok and six_month_ok and three_month_ok and freq_ok:
                print(f"\n✅ PASS: All premiums correct!")
            else:
                print(f"\n❌ FAIL:")
                if not annual_ok:
                    print(f"   - Annual premium incorrect")
                if not six_month_ok:
                    print(f"   - 6-Month premium incorrect")
                if not three_month_ok:
                    print(f"   - 3-Month premium incorrect")
                if not freq_ok:
                    print(f"   - get_premium_for_frequency() returned {premium_for_freq:.2f}€, expected {expected_freq:.2f}€")
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
    success = test_payment_frequency_prices()
    sys.exit(0 if success else 1)

