"""
Django management command to test application notification emails.
Usage: python manage.py test_application_emails --customer-email <email>
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
from main.models import InsuranceApplication
from main.email_utils import send_application_notification_emails
from django.conf import settings


class Command(BaseCommand):
    help = 'Test application notification emails (company and customer) with sample data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--customer-email',
            type=str,
            default='d.zourdoumis@gmail.com',
            help='Email address to send customer confirmation email to (default: d.zourdoumis@gmail.com)'
        )

    def handle(self, *args, **options):
        customer_email = options['customer_email']
        
        self.stdout.write(self.style.SUCCESS('\n📧 Testing Application Notification Emails\n'))
        self.stdout.write(f'  Company Email: {settings.COMPANY_EMAIL}')
        self.stdout.write(f'  Customer Email: {customer_email}')
        self.stdout.write(f'  From Email: {settings.DEFAULT_FROM_EMAIL}\n')
        
        try:
            # Create a sample application for testing
            self.stdout.write(self.style.WARNING('📝 Creating sample application...'))
            
            sample_app = InsuranceApplication(
                # User information
                full_name='Νίκος Στυλιανός',
                afm='123456789',
                phone='2101234567',
                address='Πατησίων 123',
                postal_code='10434',
                email=customer_email,
                microchip_number='123456789012345',
                
                # First Pet information
                pet_name='Ρέξ',
                pet_type='dog',
                pet_gender='male',
                pet_breed='Κοκέρ Σπάνιελ (έως 10 κιλά)',
                pet_birthdate=date(2020, 11, 11),
                pet_weight_category='10',
                
                # Second Pet information (optional)
                has_second_pet=True,
                second_pet_name='Μίμι',
                second_pet_type='cat',
                second_pet_gender='female',
                second_pet_breed='Περσική',
                second_pet_birthdate=date(2021, 5, 15),
                second_pet_weight_category='10',
                
                # Insurance details
                program='gold',
                health_status='healthy',
                health_conditions='',
                second_pet_health_status='healthy',
                second_pet_health_conditions='',
                
                # Pricing
                annual_premium=450.00,
                six_month_premium=240.00,
                three_month_premium=130.00,
                
                # Status
                status='submitted',
                
                # Ambassador code (optional)
                affiliate_code=None,
                discount_applied=0.00,
            )
            
            # Save to generate application number
            sample_app.save()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Sample application created:\n'
                    f'  Application Number: {sample_app.application_number}\n'
                    f'  Pet: {sample_app.pet_name} ({sample_app.get_pet_type_display_greek()})\n'
                    f'  Program: {sample_app.get_program_display_greek()}\n'
                    f'  Premium: €{sample_app.annual_premium}\n'
                )
            )
            
            # Send emails
            self.stdout.write(self.style.WARNING('\n📤 Sending notification emails...'))
            self.stdout.write('  1. Company notification email...')
            self.stdout.write('  2. Customer confirmation email...\n')
            
            send_application_notification_emails(sample_app)
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Test emails sent successfully!\n\n'
                    f'📬 Please check:\n'
                    f'  • Company email at: {settings.COMPANY_EMAIL}\n'
                    f'  • Customer email at: {customer_email}\n\n'
                    f'Note: The sample application (ID: {sample_app.id}, Number: {sample_app.application_number}) '
                    f'has been created in the database for testing purposes.\n'
                )
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f'❌ Error sending test emails:\n{str(e)}\n\n'
                    f'Please check:\n'
                    f'  1. Email configuration is correct\n'
                    f'  2. EMAIL_HOST_PASSWORD is set correctly\n'
                    f'  3. Email server is accessible\n'
                    f'  4. SSL/TLS settings match your mail server configuration'
                )
            )
            raise

