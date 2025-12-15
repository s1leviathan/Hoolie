#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pet_insurance.settings')
django.setup()

from main.models import InsuranceApplication
from main.utils import generate_contract_pdf, recalculate_application_premium

# Get the latest contract
app = InsuranceApplication.objects.order_by('-created_at').first()

if app:
    print(f"Found latest contract:")
    print(f"  Contract Number: {app.contract_number}")
    print(f"  Application ID: {app.id}")
    print(f"  Program: {app.program}")
    print(f"  Pet Type: {app.pet_type}")
    
    if hasattr(app, 'questionnaire') and app.questionnaire:
        q = app.questionnaire
        print(f"  Payment Frequency: {q.payment_frequency}")
        print(f"  Poisoning Coverage: {q.additional_poisoning_coverage}")
        print(f"  Blood Checkup: {q.additional_blood_checkup}")
        
        print(f"\nCurrent Premiums:")
        print(f"  Annual: {app.annual_premium}")
        print(f"  6-Month: {app.six_month_premium}")
        print(f"  3-Month: {app.three_month_premium}")
        
        print(f"\nRecalculating premiums to include add-ons...")
        recalculate_application_premium(app)
        app.refresh_from_db()
        
        print(f"\nUpdated Premiums:")
        print(f"  Annual: {app.annual_premium}")
        print(f"  6-Month: {app.six_month_premium}")
        print(f"  3-Month: {app.three_month_premium}")
        
        print(f"\nRegenerating contract PDF...")
        try:
            result = generate_contract_pdf(app)
            if isinstance(result, list):
                print(f"✓ Generated {len(result)} contract(s):")
                for path in result:
                    print(f"  - {path}")
            else:
                print(f"✓ Contract generated: {result}")
            
            app.refresh_from_db()
            print(f"\nContract PDF path: {app.contract_pdf_path}")
            print(f"Contract generated flag: {app.contract_generated}")
        except Exception as e:
            print(f"✗ Error generating contract: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("\nNo questionnaire found - cannot regenerate contract")
else:
    print("No applications found")

