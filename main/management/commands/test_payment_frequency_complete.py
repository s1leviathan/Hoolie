#!/usr/bin/env python3
"""
Complete integration test for payment frequency implementation
Tests with actual Django models
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from main.models import InsuranceApplication, Questionnaire
from datetime import date, timedelta


class Command(BaseCommand):
    help = 'Test payment frequency implementation with real models'

    def handle(self, *args, **options):
        self.stdout.write("\n" + "="*80)
        self.stdout.write(self.style.SUCCESS("🧪 PAYMENT FREQUENCY - COMPLETE INTEGRATION TEST"))
        self.stdout.write("="*80 + "\n")
        
        # Clean up any existing test data
        InsuranceApplication.objects.filter(full_name__startswith='TEST-').delete()
        
        test_scenarios = [
            {
                'name': 'Dog Silver - Annual',
                'program': 'silver',
                'pet_type': 'dog',
                'annual': 166.75,
                'six_month': 87.54,
                'three_month': 45.86,
                'frequency': 'annual',
                'expected_display': 'Ασημένιο Ετήσιο',
                'expected_price': 166.75,
                'expected_days': 364
            },
            {
                'name': 'Dog Gold - 6-Month',
                'program': 'gold',
                'pet_type': 'dog',
                'annual': 234.14,
                'six_month': 122.92,
                'three_month': 64.39,
                'frequency': 'six_month',
                'expected_display': 'Χρυσό Εξαμηνιαίο',
                'expected_price': 122.92,
                'expected_days': 182
            },
            {
                'name': 'Dog Platinum - 3-Month',
                'program': 'platinum',
                'pet_type': 'dog',
                'annual': 368.92,
                'six_month': 193.69,
                'three_month': 101.45,
                'frequency': 'three_month',
                'expected_display': 'Πλατινένιο Τριμηνιαίο',
                'expected_price': 101.45,
                'expected_days': 91
            },
            {
                'name': 'Cat Silver - Annual',
                'program': 'silver',
                'pet_type': 'cat',
                'annual': 113.81,
                'six_month': 59.75,
                'three_month': 31.30,
                'frequency': 'annual',
                'expected_display': 'Ασημένιο Ετήσιο',
                'expected_price': 113.81,
                'expected_days': 364
            },
        ]
        
        passed = 0
        failed = 0
        
        for i, scenario in enumerate(test_scenarios, 1):
            self.stdout.write("\n" + "="*80)
            self.stdout.write(f"📋 TEST {i}: {scenario['name']}")
            self.stdout.write("="*80 + "\n")
            
            try:
                # Create application
                app = InsuranceApplication.objects.create(
                    full_name=f"TEST-{scenario['name']}",
                    email=f"test{i}@example.com",
                    phone="6912345678",
                    address="Test Address 123",
                    postal_code="12345",
                    afm="123456789",
                    pet_name=f"TestPet{i}",
                    pet_type=scenario['pet_type'],
                    pet_gender='male',
                    pet_breed="Test Breed",
                    pet_birthdate=date(2020, 1, 1),
                    program=scenario['program'],
                    health_status='healthy',
                    annual_premium=scenario['annual'],
                    six_month_premium=scenario['six_month'],
                    three_month_premium=scenario['three_month'],
                    status='submitted',
                    pet_weight_category='up_10'
                )
                
                self.stdout.write(f"✅ Application created: {app.contract_number}")
                
                # Create questionnaire with payment frequency
                questionnaire = Questionnaire.objects.create(
                    application=app,
                    payment_frequency=scenario['frequency'],
                    program=scenario['program']
                )
                
                self.stdout.write(f"✅ Questionnaire created with frequency: {scenario['frequency']}")
                
                # Refresh application to get questionnaire relationship
                app.refresh_from_db()
                
                # Test methods
                display = app.get_program_with_frequency_display()
                freq_display = app.get_payment_frequency_display_greek()
                price = app.get_premium_for_frequency()
                end_date = app.calculate_contract_end_date()
                days = (end_date - app.contract_start_date).days
                
                # Display results
                self.stdout.write("\n📊 RESULTS:")
                self.stdout.write(f"   Program Display: {display}")
                self.stdout.write(f"   Frequency Display: {freq_display}")
                self.stdout.write(f"   Premium: {price:.2f}€")
                self.stdout.write(f"   Start Date: {app.contract_start_date.strftime('%d/%m/%Y')}")
                self.stdout.write(f"   End Date: {end_date.strftime('%d/%m/%Y')} ({days} days)")
                
                # Verify
                checks = {
                    'Display': display == scenario['expected_display'],
                    'Price': abs(price - scenario['expected_price']) < 0.01,
                    'Days': days == scenario['expected_days']
                }
                
                self.stdout.write("\n✅ VERIFICATION:")
                all_passed = True
                for check_name, check_passed in checks.items():
                    if check_passed:
                        self.stdout.write(self.style.SUCCESS(f"   ✅ {check_name}"))
                    else:
                        self.stdout.write(self.style.ERROR(f"   ❌ {check_name}"))
                        all_passed = False
                
                if all_passed:
                    self.stdout.write(self.style.SUCCESS("\n   ✅ ALL CHECKS PASSED!"))
                    passed += 1
                else:
                    self.stdout.write(self.style.ERROR("\n   ❌ SOME CHECKS FAILED!"))
                    failed += 1
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"\n❌ ERROR: {e}"))
                import traceback
                self.stdout.write(traceback.format_exc())
                failed += 1
        
        # Summary
        self.stdout.write("\n" + "="*80)
        self.stdout.write("📊 FINAL RESULTS")
        self.stdout.write("="*80 + "\n")
        
        total = passed + failed
        self.stdout.write(f"Total Tests: {total}")
        self.stdout.write(self.style.SUCCESS(f"✅ Passed: {passed}"))
        if failed > 0:
            self.stdout.write(self.style.ERROR(f"❌ Failed: {failed}"))
        
        self.stdout.write("\n" + "="*80)
        
        if failed == 0:
            self.stdout.write(self.style.SUCCESS("🎉 100% TESTS PASSED!"))
            self.stdout.write(self.style.SUCCESS("✅ Payment frequency display working"))
            self.stdout.write(self.style.SUCCESS("✅ Pricing calculations correct"))
            self.stdout.write(self.style.SUCCESS("✅ Contract dates accurate"))
            self.stdout.write(self.style.SUCCESS("✅ Ready for production!"))
        else:
            self.stdout.write(self.style.ERROR("⚠️ TESTS FAILED - Fix issues before deploying"))
        
        self.stdout.write("="*80 + "\n")
        
        # Clean up test data
        if self.stdout.isatty():
            response = input("\nDelete test data? (y/n): ")
            if response.lower() == 'y':
                InsuranceApplication.objects.filter(full_name__startswith='TEST-').delete()
                self.stdout.write(self.style.SUCCESS("✅ Test data cleaned up"))


