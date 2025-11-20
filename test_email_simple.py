#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pet_insurance.settings')
django.setup()

from django.conf import settings
from django.core.mail import send_mail

print("=" * 60)
print("EMAIL CONFIGURATION:")
print("=" * 60)
print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
print(f"EMAIL_USE_SSL: {settings.EMAIL_USE_SSL}")
print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
print(f"COMPANY_EMAIL: {settings.COMPANY_EMAIL}")
print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
print("=" * 60)

print("\n📤 Sending test email to d.zourdoumis@gmail.com...")
try:
    send_mail(
        subject='Test Email from Hoolie',
        message='This is a test email.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=['d.zourdoumis@gmail.com'],
        fail_silently=False,
    )
    print("✅ Email sent successfully!")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()


