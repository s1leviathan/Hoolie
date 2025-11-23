"""
Django management command to verify email sending with detailed SMTP logging
"""
from django.core.management.base import BaseCommand
from django.conf import settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Command(BaseCommand):
    help = 'Verify email sending with detailed SMTP response logging'

    def add_arguments(self, parser):
        parser.add_argument(
            '--to',
            type=str,
            default='jimzourdoumis@gmail.com',
            help='Email address to send test email to'
        )

    def handle(self, *args, **options):
        recipient = options['to']
        
        self.stdout.write("=" * 70)
        self.stdout.write(self.style.SUCCESS("EMAIL SENDING VERIFICATION"))
        self.stdout.write("=" * 70)
        self.stdout.write(f"SMTP Host: {settings.EMAIL_HOST}")
        self.stdout.write(f"Port: {settings.EMAIL_PORT}")
        self.stdout.write(f"TLS: {settings.EMAIL_USE_TLS}, SSL: {settings.EMAIL_USE_SSL}")
        self.stdout.write(f"From: {settings.EMAIL_HOST_USER}")
        self.stdout.write(f"To: {recipient}")
        self.stdout.write("=" * 70)

        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = settings.DEFAULT_FROM_EMAIL
            msg['To'] = recipient
            msg['Subject'] = 'VERIFICATION TEST - Email Sending Test'
            
            body = 'This is a verification test to confirm emails are being sent from the server.'
            msg.attach(MIMEText(body, 'plain'))
            
            self.stdout.write("\n1. Connecting to SMTP server...")
            if settings.EMAIL_USE_SSL:
                server = smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT)
                self.stdout.write(self.style.SUCCESS(f"   ✅ Connected via SSL to {settings.EMAIL_HOST}:{settings.EMAIL_PORT}"))
            else:
                server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
                self.stdout.write(self.style.SUCCESS(f"   ✅ Connected to {settings.EMAIL_HOST}:{settings.EMAIL_PORT}"))
                if settings.EMAIL_USE_TLS:
                    server.starttls()
                    self.stdout.write(self.style.SUCCESS("   ✅ TLS started"))
            
            self.stdout.write("2. Authenticating...")
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            self.stdout.write(self.style.SUCCESS("   ✅ Authentication successful"))
            
            self.stdout.write("3. Sending email...")
            text = msg.as_string()
            result = server.sendmail(settings.DEFAULT_FROM_EMAIL, [recipient], text)
            self.stdout.write(self.style.SUCCESS(f"   ✅ Email sent! SMTP Response: {result}"))
            
            self.stdout.write("4. Closing connection...")
            server.quit()
            self.stdout.write(self.style.SUCCESS("   ✅ Connection closed"))
            
            self.stdout.write("\n" + "=" * 70)
            self.stdout.write(self.style.SUCCESS("✅ SUCCESS: Email was sent successfully to SMTP server"))
            self.stdout.write("=" * 70)
            self.stdout.write("\nThe email was accepted by the SMTP server.")
            self.stdout.write("If it's not in the inbox, Gmail is filtering it.")
            self.stdout.write("Check spam folder or wait a few minutes.")
            
        except smtplib.SMTPAuthenticationError as e:
            self.stdout.write(self.style.ERROR(f"\n❌ AUTHENTICATION ERROR: {e}"))
            self.stdout.write("The SMTP server rejected the credentials.")
            
        except smtplib.SMTPRecipientsRefused as e:
            self.stdout.write(self.style.ERROR(f"\n❌ RECIPIENT REFUSED: {e}"))
            self.stdout.write("The recipient email was rejected by the server.")
            
        except smtplib.SMTPSenderRefused as e:
            self.stdout.write(self.style.ERROR(f"\n❌ SENDER REFUSED: {e}"))
            self.stdout.write("The sender email was rejected by the server.")
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"\n❌ ERROR: {e}"))
            import traceback
            self.stdout.write(traceback.format_exc())

