"""
Email utilities for sending application notifications
"""
import os
import logging
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags

logger = logging.getLogger(__name__)

def send_application_notification_emails(application):
    """
    Send notification emails after application submission:
    1. Email to company about new application
    2. Email to customer with confirmation
    
    Note: This function never raises exceptions - email failures are logged but don't prevent
    the application from being saved. PDFs and documents are always generated regardless.
    """
    try:
        # Send email to company
        send_company_notification_email(application)
    except Exception as e:
        logger.error(f"Error sending company notification email for application {application.id}: {e}")
        # Don't raise - continue to try customer email
    
    try:
        # Send email to customer
        send_customer_confirmation_email(application)
    except Exception as e:
        logger.error(f"Error sending customer confirmation email for application {application.id}: {e}")
        # Don't raise - email failure doesn't prevent application submission
    
    logger.info(f"Email sending attempt completed for application {application.application_number}")

def send_company_notification_email(application):
    """Send email to company about new application submission"""
    try:
        subject = f'Νέα Αίτηση Ασφάλισης - {application.application_number}'
        
        # Prepare context
        context = {
            'application': application,
            'application_number': application.application_number,
            'pet_name': application.pet_name,
            'customer_name': application.full_name,
            'customer_email': application.email,
            'customer_phone': application.phone,
            'program': application.get_program_display_greek(),
            'annual_premium': application.annual_premium,
            'has_second_pet': application.has_second_pet,
            'second_pet_name': application.second_pet_name if application.has_second_pet else None,
        }
        
        # Render HTML email
        html_message = render_to_string('emails/company_notification.html', context)
        plain_message = strip_tags(html_message)
        
        # Create email
        email = EmailMultiAlternatives(
            subject=subject,
            body=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.COMPANY_EMAIL],
        )
        email.attach_alternative(html_message, "text/html")
        
        # Attach PDF if available (contract PDF contains all application data)
        # Works with both S3 and local storage
        if application.contract_pdf_path:
            try:
                from django.core.files.storage import default_storage
                if default_storage.exists(application.contract_pdf_path):
                    with default_storage.open(application.contract_pdf_path, 'rb') as pdf:
                        email.attach(
                            f'application_{application.application_number}.pdf',
                            pdf.read(),
                            'application/pdf'
                        )
            except Exception as e:
                logger.warning(f"Could not attach PDF to company email: {e}")
        
        email.send(fail_silently=False)
        logger.info(f"Company notification email sent for application {application.application_number}")
        
    except Exception as e:
        logger.error(f"Error sending company notification email: {e}")
        # Don't raise - allow application to continue even if email fails

def send_customer_confirmation_email(application):
    """Send confirmation email to customer (with CC to company)."""
    try:
        # Determine greeting
        name_parts = application.full_name.split() if application.full_name else []
        customer_greeting = name_parts[0] if name_parts else "Κύριε/Κυρία"

        # Use contract_number if exists, else fallback
        display_number = application.contract_number or application.application_number

        subject = f"Επιβεβαίωση Αίτησης Ασφάλισης - {display_number}"

        context = {
            'application': application,
            'application_number': display_number,
            'customer_greeting': customer_greeting,
            'pet_name': application.pet_name,
            'has_second_pet': application.has_second_pet,
            'second_pet_name': application.second_pet_name if application.has_second_pet else None,
        }

        plain_message = render_to_string('emails/customer_confirmation.txt', context)

        # Prepare SMTP message
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        msg = MIMEMultipart()
        msg['From'] = settings.DEFAULT_FROM_EMAIL
        msg['To'] = application.email
        msg['Subject'] = subject

        # ADD CC HERE
        msg['Cc'] = settings.COMPANY_EMAIL

        msg.attach(MIMEText(plain_message, 'plain'))

        # Prepare SMTP server
        if settings.EMAIL_USE_SSL:
            server = smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT)
        else:
            server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            if settings.EMAIL_USE_TLS:
                server.starttls()

        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

        # RECIPIENT LIST (TO + CC)
        recipients = [application.email, settings.COMPANY_EMAIL]

        result = server.sendmail(settings.DEFAULT_FROM_EMAIL, recipients, msg.as_string())
        server.quit()

        logger.info(f"Confirmation email sent to {application.email}, CC {settings.COMPANY_EMAIL}")

    except Exception as e:
        logger.error(f"Error sending customer confirmation email: {e}")


