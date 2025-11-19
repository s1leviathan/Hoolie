"""
Django management command to test email sending.
Usage: python manage.py test_email --to <email_address>
"""
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings


class Command(BaseCommand):
    help = 'Test email sending functionality'

    def add_arguments(self, parser):
        parser.add_argument(
            '--to',
            type=str,
            required=True,
            help='Email address to send test email to'
        )

    def handle(self, *args, **options):
        to_email = options['to']
        
        # Display current email configuration
        self.stdout.write(self.style.SUCCESS('\n📧 Current Email Configuration:'))
        self.stdout.write(f'  EMAIL_HOST: {settings.EMAIL_HOST}')
        self.stdout.write(f'  EMAIL_PORT: {settings.EMAIL_PORT}')
        self.stdout.write(f'  EMAIL_USE_SSL: {settings.EMAIL_USE_SSL}')
        self.stdout.write(f'  EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}')
        self.stdout.write(f'  EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}')
        self.stdout.write(f'  DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}')
        self.stdout.write(f'  COMPANY_EMAIL: {settings.COMPANY_EMAIL}\n')
        
        # Test email sending
        try:
            self.stdout.write(self.style.WARNING(f'📤 Sending test email to {to_email}...'))
            
            send_mail(
                subject='Test Email from Hoolie Pet Insurance',
                message='This is a test email from Hoolie Pet Insurance system.\n\nIf you receive this, the email configuration is working correctly!',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[to_email],
                fail_silently=False,
            )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Test email sent successfully to {to_email}!\n'
                    f'Please check your inbox (and spam folder) to confirm receipt.'
                )
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f'❌ Error sending test email:\n{str(e)}\n\n'
                    f'Please check:\n'
                    f'  1. EMAIL_HOST_USER and EMAIL_HOST_PASSWORD are set correctly\n'
                    f'  2. Email server credentials are valid\n'
                    f'  3. Firewall/network allows SMTP connections\n'
                    f'  4. SSL/TLS settings match your mail server configuration'
                )
            )
            raise

