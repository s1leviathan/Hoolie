#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pet_insurance.settings')
django.setup()

from main.models import InsuranceApplication
from main.utils import get_poisoning_price

# Get the last contract
app = InsuranceApplication.objects.order_by('-created_at').first()

if app:
    print(f"Contract Number: {app.contract_number}")
    print(f"Application Number: {app.application_number}")
    print(f"Created: {app.created_at}")
    print(f"Program: {app.program}")
    print(f"Pet Type: {app.pet_type}")
    print(f"Pet Weight Category: {app.pet_weight_category}")
    print(f"\nPremiums:")
    print(f"  Annual: {app.annual_premium}")
    print(f"  6-Month: {app.six_month_premium}")
    print(f"  3-Month: {app.three_month_premium}")
    
    if hasattr(app, 'questionnaire') and app.questionnaire:
        q = app.questionnaire
        print(f"\nQuestionnaire:")
        print(f"  Payment Frequency: {q.payment_frequency}")
        print(f"  Poisoning Coverage: {q.additional_poisoning_coverage}")
        print(f"  Blood Checkup: {q.additional_blood_checkup}")
        print(f"  Breed 5%: {q.special_breed_5_percent}")
        print(f"  Breed 20%: {q.special_breed_20_percent}")
        
        # Calculate what the breakdown should show
        if q.additional_poisoning_coverage:
            poisoning_annual = get_poisoning_price(app.program, "annual")
            poisoning_freq = get_poisoning_price(app.program, q.payment_frequency or "annual")
            print(f"\nPoisoning Price:")
            print(f"  Annual: {poisoning_annual}€")
            print(f"  For frequency ({q.payment_frequency}): {poisoning_freq}€")
            
        # Calculate expected total
        from main.fillpdf_utils import get_pricing_values, normalize_weight
        mapped_weight = normalize_weight(str(app.pet_weight_category))
        _, _, _, base_annual = get_pricing_values(app, app.pet_type, mapped_weight, app.program, "annual")
        print(f"\nBase Annual Price from Excel: {base_annual}€")
        
        # Calculate with surcharges and add-ons
        total = float(base_annual)
        if q.special_breed_5_percent:
            total = total * 1.05
        if q.special_breed_20_percent:
            total = total * 1.20
        if q.additional_poisoning_coverage:
            total += poisoning_annual
        if q.additional_blood_checkup:
            total += 28.00
            
        print(f"Expected Annual Total (with all add-ons): {total:.2f}€")
        print(f"Stored Annual Premium: {app.annual_premium}")
        print(f"Difference: {float(app.annual_premium or 0) - total:.2f}€")
    else:
        print("\nNo questionnaire found")
else:
    print("No applications found")

