#!/usr/bin/env python3
"""
Test command to generate sample contracts using the new template
"""
from django.core.management.base import BaseCommand
from django.conf import settings
from main.models import InsuranceApplication
from main.fillpdf_utils import generate_contract_with_fillpdf
import os
import tempfile
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Generate test contracts using the new template'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=3,
            help='Number of test contracts to generate (default: 3)'
        )

    def handle(self, *args, **options):
        count = options['count']
        
        self.stdout.write(self.style.SUCCESS(f'\n📄 Generating {count} test contracts with new template...\n'))
        
        # Get or create test applications
        applications = InsuranceApplication.objects.all()[:count]
        
        if not applications.exists():
            self.stdout.write(self.style.WARNING('No applications found in database. Creating sample applications...'))
            # Create sample applications for testing
            for i in range(count):
                app = InsuranceApplication.objects.create(
                    full_name=f"Test User {i+1}",
                    email=f"test{i+1}@example.com",
                    phone="2101234567",
                    address=f"Test Address {i+1}",
                    postal_code="12345",
                    afm="123456789",
                    pet_name=f"Test Pet {i+1}",
                    pet_type="dog" if i % 2 == 0 else "cat",
                    pet_gender="male",
                    pet_breed="Golden Retriever" if i % 2 == 0 else "Persian",
                    pet_birthdate="2020-01-01",
                    microchip_number=f"12345678901234{i}",
                    program=["silver", "gold", "platinum"][i % 3],
                    health_status="healthy",
                    annual_premium=166.75 if i % 2 == 0 else 113.81,
                    status='approved',
                    contract_number=f"HOL-2025-TEST{i+1:03d}",
                    receipt_number=f"REC-20250101-TEST{i+1:03d}",
                    payment_code=f"PAY-TEST{i+1:03d}",
                    contract_generated=False,
                    contract_start_date=datetime.now().date(),
                    contract_end_date=(datetime.now() + timedelta(days=365)).date(),
                )
                applications = list(applications) + [app]
        
        # Create output directory
        output_dir = os.path.join(settings.BASE_DIR, 'test_contracts')
        os.makedirs(output_dir, exist_ok=True)
        
        success_count = 0
        error_count = 0
        
        for i, application in enumerate(applications, 1):
            try:
                self.stdout.write(f'\n[{i}/{count}] Generating contract for: {application.contract_number or application.application_number}')
                self.stdout.write(f'  Client: {application.full_name}')
                self.stdout.write(f'  Pet: {application.pet_name} ({application.get_pet_type_display_greek()})')
                self.stdout.write(f'  Program: {application.get_program_display_greek()}')
                
                # Generate contract
                output_filename = f"contract_{application.contract_number or application.application_number}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                output_path = os.path.join(output_dir, output_filename)
                
                generate_contract_with_fillpdf(application, output_path, pet_number=1)
                
                if os.path.exists(output_path):
                    file_size = os.path.getsize(output_path)
                    self.stdout.write(self.style.SUCCESS(f'  ✅ Contract generated: {output_filename} ({file_size:,} bytes)'))
                    self.stdout.write(f'  📁 Location: {output_path}')
                    success_count += 1
                else:
                    self.stdout.write(self.style.ERROR(f'  ❌ Contract file not found after generation'))
                    error_count += 1
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  ❌ Error generating contract: {e}'))
                import traceback
                self.stdout.write(traceback.format_exc())
                error_count += 1
        
        # Summary
        self.stdout.write('\n' + '=' * 80)
        self.stdout.write(self.style.SUCCESS(f'✅ Successfully generated: {success_count} contracts'))
        if error_count > 0:
            self.stdout.write(self.style.ERROR(f'❌ Errors: {error_count}'))
        self.stdout.write(f'📁 Output directory: {output_dir}')
        self.stdout.write('=' * 80 + '\n')

