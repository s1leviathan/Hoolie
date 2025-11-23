"""
Django management command to test customer confirmation email.
Usage: python manage.py test_customer_email --email d.zourdoumis@gmail.com
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date
from main.models import InsuranceApplication
from main.email_utils import send_customer_confirmation_email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


class Command(BaseCommand):
    help = 'Test customer confirmation email with sample data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            default='d.zourdoumis@gmail.com',
            help='Email address to send customer confirmation email to (default: d.zourdoumis@gmail.com)'
        )

    def handle(self, *args, **options):
        recipient_email = options['email']
        
        self.stdout.write(self.style.SUCCESS('\n📧 Testing Customer Confirmation Email\n'))
        self.stdout.write(f'  Recipient: {recipient_email}')
        self.stdout.write(f'  From: {settings.DEFAULT_FROM_EMAIL}\n')
        
        try:
            # Create a sample application for testing
            self.stdout.write(self.style.WARNING('📝 Creating sample application...'))
            
            sample_app = InsuranceApplication(
                # User information
                full_name='Dimitris Zourdoumis',
                afm='123456789',
                phone='2101234567',
                address='Test Address 123',
                postal_code='10434',
                email=recipient_email,  # Will be overridden in email send
                microchip_number='123456789012345',
                
                # First Pet information
                pet_name='Ρέξ',
                pet_type='dog',
                pet_gender='male',
                pet_breed='Κοκέρ Σπάνιελ (έως 10 κιλά)',
                pet_birthdate=date(2020, 1, 15),
                pet_weight_category='10',
                
                # Insurance details
                program='gold',
                health_status='healthy',
                health_conditions='',
                
                # Pricing
                annual_premium=450.00,
                six_month_premium=240.00,
                three_month_premium=130.00,
                
                # Status
                status='submitted',
                has_second_pet=False,
            )
            
            # Save to generate application number
            sample_app.save()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Sample application created:\n'
                    f'  Application Number: {sample_app.application_number}\n'
                    f'  Pet: {sample_app.pet_name}\n'
                )
            )
            
            # Send customer confirmation email
            self.stdout.write(self.style.WARNING('\n📤 Sending customer confirmation email...'))
            
            # Get customer's first name for greeting
            customer_name_parts = sample_app.full_name.split() if sample_app.full_name else []
            if customer_name_parts:
                customer_greeting = customer_name_parts[0]
            else:
                customer_greeting = 'Κύριε/Κυρία'
            
            subject = f'Επιβεβαίωση Αίτησης Ασφάλισης - {sample_app.application_number}'
            
            # Prepare context
            context = {
                'application': sample_app,
                'application_number': sample_app.application_number,
                'customer_greeting': customer_greeting,
                'pet_name': sample_app.pet_name,
                'has_second_pet': sample_app.has_second_pet,
                'second_pet_name': sample_app.second_pet_name if sample_app.has_second_pet else None,
            }
            
            # Render HTML and plain text emails
            html_message = render_to_string('emails/customer_confirmation.html', context)
            plain_message = render_to_string('emails/customer_confirmation.txt', context)
            
            # Send plain text email first to ensure delivery
            from django.core.mail import send_mail
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient_email],
                fail_silently=False,
            )
            
            # Also try sending HTML version (but don't fail if it doesn't work)
            try:
                email = EmailMultiAlternatives(
                    subject=subject,
                    body=plain_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[recipient_email],
                )
                email.attach_alternative(html_message, "text/html")
                email.send(fail_silently=True)
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"HTML email failed but plain text sent: {e}"))
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Customer confirmation email sent successfully!\n\n'
                    f'📬 Please check: {recipient_email}\n\n'
                    f'Note: The sample application (ID: {sample_app.id}, Number: {sample_app.application_number}) '
                    f'has been created in the database for testing purposes.\n'
                )
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f'❌ Error sending test email:\n{str(e)}\n\n'
                    f'Please check:\n'
                    f'  1. Email configuration is correct\n'
                    f'  2. EMAIL_HOST_PASSWORD is set correctly\n'
                    f'  3. Email server is accessible\n'
                    f'  4. SSL/TLS settings match your mail server configuration'
                )
            )
            raise

