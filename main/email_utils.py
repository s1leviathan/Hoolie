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
    """
    try:
        # Send email to company
        send_company_notification_email(application)
        
        # Send email to customer
        send_customer_confirmation_email(application)
        
        logger.info(f"Successfully sent notification emails for application {application.application_number}")
        
    except Exception as e:
        logger.error(f"Error sending notification emails for application {application.id}: {e}")
        raise

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
        pdf_path = None
        if application.contract_pdf_path and os.path.exists(application.contract_pdf_path):
            pdf_path = application.contract_pdf_path
        
        if pdf_path:
            try:
                with open(pdf_path, 'rb') as pdf:
                    email.attach(
                        f'application_{application.application_number}.pdf',
                        pdf.read(),
                        'application/pdf'
                    )
            except Exception as e:
                logger.warning(f"Could not attach PDF to company email: {e}")
        
        email.send()
        logger.info(f"Company notification email sent for application {application.application_number}")
        
    except Exception as e:
        logger.error(f"Error sending company notification email: {e}")
        raise

def send_customer_confirmation_email(application):
    """Send confirmation email to customer"""
    try:
        # Get customer's first name or last name for greeting
        customer_name_parts = application.full_name.split() if application.full_name else []
        if customer_name_parts:
            customer_greeting = customer_name_parts[0]  # Use first name
        else:
            customer_greeting = 'Κύριε/Κυρία'  # Fallback if no name
        
        subject = f'Επιβεβαίωση Αίτησης Ασφάλισης - {application.application_number}'
        
        # Prepare context
        context = {
            'application': application,
            'application_number': application.application_number,
            'customer_greeting': customer_greeting,
            'pet_name': application.pet_name,
            'has_second_pet': application.has_second_pet,
            'second_pet_name': application.second_pet_name if application.has_second_pet else None,
        }
        
        # Render HTML email
        html_message = render_to_string('emails/customer_confirmation.html', context)
        plain_message = strip_tags(html_message)
        
        # Create email
        email = EmailMultiAlternatives(
            subject=subject,
            body=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[application.email],
        )
        email.attach_alternative(html_message, "text/html")
        
        email.send()
        logger.info(f"Customer confirmation email sent to {application.email} for application {application.application_number}")
        
    except Exception as e:
        logger.error(f"Error sending customer confirmation email: {e}")
        raise

