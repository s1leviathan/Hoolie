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
    """Send confirmation email to customer"""
    try:
        # Get customer's first name or last name for greeting
        customer_name_parts = application.full_name.split() if application.full_name else []
        if customer_name_parts:
            customer_greeting = customer_name_parts[0]  # Use first name
        else:
            customer_greeting = 'Κύριε/Κυρία'  # Fallback if no name
        
        # Use proper Greek subject for customer confirmation
        subject = f'Επιβεβαίωση Αίτησης Ασφάλισης - {application.application_number}'
        
        # Prepare context for email template
        context = {
            'application': application,
            'application_number': application.application_number,
            'customer_greeting': customer_greeting,
            'pet_name': application.pet_name,
            'has_second_pet': application.has_second_pet,
            'second_pet_name': application.second_pet_name if application.has_second_pet else None,
        }
        
        # Render plain text email template
        plain_message = render_to_string('emails/customer_confirmation.txt', context)
        
        # Send using EXACT same method as verification email (smtplib directly)
        # This bypasses Django's email backend which might format emails differently
        logger.info(f"Attempting to send customer confirmation email to {application.email} for application {application.application_number}")
        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            
            # Create message exactly like verification email
            msg = MIMEMultipart()
            msg['From'] = settings.DEFAULT_FROM_EMAIL
            msg['To'] = application.email
            msg['Subject'] = subject
            msg.attach(MIMEText(plain_message, 'plain'))
            
            # Connect and send exactly like verification email
            if settings.EMAIL_USE_SSL:
                server = smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT)
            else:
                server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
                if settings.EMAIL_USE_TLS:
                    server.starttls()
            
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            text = msg.as_string()
            result = server.sendmail(settings.DEFAULT_FROM_EMAIL, [application.email], text)
            server.quit()
            
            logger.info(f"Customer confirmation email sent successfully to {application.email}. SMTP returned: {result}. Application: {application.application_number}")
        except Exception as e:
            logger.error(f"Failed to send customer confirmation email to {application.email}: {e}")
            import traceback
            logger.error(traceback.format_exc())
            raise  # Re-raise to ensure we know if email fails
        
    except Exception as e:
        logger.error(f"Error sending customer confirmation email: {e}")
        # Don't raise - allow application to continue even if email fails

