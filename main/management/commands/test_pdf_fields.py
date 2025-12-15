#!/usr/bin/env python3
"""
Test PDF field generation with real models
"""
from django.core.management.base import BaseCommand
from main.models import InsuranceApplication, Questionnaire
from main.fillpdf_utils import create_contract_field_mapping
from datetime import date


class Command(BaseCommand):
    help = 'Test PDF field mapping with real models'

    def handle(self, *args, **options):
        self.stdout.write("\n" + "="*80)
        self.stdout.write(self.style.SUCCESS("📄 PDF FIELD MAPPING TEST"))
        self.stdout.write("="*80 + "\n")
        
        # Get test applications created by previous command
        test_apps = InsuranceApplication.objects.filter(
            full_name__startswith='TEST-'
        ).select_related('questionnaire')
        
        if not test_apps.exists():
            self.stdout.write(self.style.WARNING("No test applications found. Run test_payment_frequency_complete first."))
            return
        
        self.stdout.write(f"Found {test_apps.count()} test applications\n")
        
        for i, app in enumerate(test_apps, 1):
            self.stdout.write("\n" + "-"*80)
            self.stdout.write(f"📋 Application {i}: {app.contract_number}")
            self.stdout.write("-"*80 + "\n")
            
            try:
                # Get questionnaire
                if not hasattr(app, 'questionnaire') or not app.questionnaire:
                    self.stdout.write(self.style.WARNING("   No questionnaire found"))
                    continue
                
                questionnaire = app.questionnaire
                
                # Display application info
                self.stdout.write(f"   Program: {app.program}")
                self.stdout.write(f"   Payment Frequency: {questionnaire.payment_frequency}")
                self.stdout.write(f"   Annual Premium: {app.annual_premium}€")
                self.stdout.write(f"   6-Month Premium: {app.six_month_premium}€")
                self.stdout.write(f"   3-Month Premium: {app.three_month_premium}€")
                
                # Create field mapping (simulating PDF generation)
                field_mapping = create_contract_field_mapping(
                    application=app,
                    pet_name=app.pet_name,
                    pet_type_display=app.get_pet_type_display_greek(),
                    pet_breed=app.pet_breed,
                    pet_weight=app.get_weight_display('10') if app.pet_weight_category else '',
                    pet_birthdate=app.pet_birthdate.strftime('%d/%m/%Y') if app.pet_birthdate else '',
                    contract_suffix="",
                    net_premium=100.00,  # Dummy values for testing
                    fee=30.00,
                    auxiliary=1.00,
                    tax=20.00
                )
                
                # Display critical PDF fields
                self.stdout.write("\n📄 PDF FIELDS:")
                self.stdout.write(f"   text_5fgpc (Start Date):  {field_mapping.get('text_5fgpc', 'N/A')}")
                self.stdout.write(f"   text_6zqkn (End Date):    {field_mapping.get('text_6zqkn', 'N/A')}")
                self.stdout.write(self.style.SUCCESS(f"   text_7tbbt (Program):     {field_mapping.get('text_7tbbt', 'N/A')}"))
                self.stdout.write(self.style.SUCCESS(f"   text_37rpnu (Total):      {field_mapping.get('text_37rpnu', 'N/A')}"))
                
                # Calculate expected dates
                expected_end = app.calculate_contract_end_date()
                days_coverage = (expected_end - app.contract_start_date).days
                
                self.stdout.write(f"\n📅 DATE VERIFICATION:")
                self.stdout.write(f"   Start: {app.contract_start_date.strftime('%d/%m/%Y')}")
                self.stdout.write(f"   End: {expected_end.strftime('%d/%m/%Y')} ({days_coverage} days)")
                
                # Verify
                expected_price = app.get_premium_for_frequency()
                actual_price_str = field_mapping.get('text_37rpnu', '0€')
                actual_price = float(actual_price_str.replace('€', ''))
                
                price_ok = abs(actual_price - expected_price) < 0.01
                display_ok = app.get_program_with_frequency_display() in field_mapping.get('text_7tbbt', '')
                
                if price_ok and display_ok:
                    self.stdout.write(self.style.SUCCESS("\n   ✅ PDF FIELDS CORRECT!"))
                else:
                    self.stdout.write(self.style.ERROR("\n   ❌ PDF FIELDS INCORRECT!"))
                    if not price_ok:
                        self.stdout.write(f"      Expected price: {expected_price:.2f}€")
                        self.stdout.write(f"      Actual price: {actual_price:.2f}€")
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"\n❌ ERROR: {e}"))
                import traceback
                self.stdout.write(traceback.format_exc())
        
        self.stdout.write("\n" + "="*80)
        self.stdout.write(self.style.SUCCESS("✅ PDF FIELD TESTING COMPLETE"))
        self.stdout.write("="*80 + "\n")



