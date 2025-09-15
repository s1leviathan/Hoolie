"""
QR Code related views for contract verification and information
"""
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, Http404
from django.views.decorators.http import require_http_methods
from django.contrib import messages

from .models import InsuranceApplication


def contract_verification(request, contract_number):
    """View for contract verification via QR code"""
    try:
        application = get_object_or_404(InsuranceApplication, contract_number=contract_number)
        
        context = {
            'application': application,
            'verification_success': True,
        }
        
        return render(request, 'qr/contract_verification.html', context)
        
    except InsuranceApplication.DoesNotExist:
        context = {
            'contract_number': contract_number,
            'verification_success': False,
            'error_message': 'Το συμβόλαιο δεν βρέθηκε στο σύστημα.'
        }
        
        return render(request, 'qr/contract_verification.html', context)


def terms_and_conditions(request):
    """View for terms and conditions (accessed via QR code)"""
    context = {
        'page_title': 'Όροι και Προϋποθέσεις Ασφάλισης',
        'company_name': 'Wise Daedalus IKE',
    }
    
    return render(request, 'qr/terms_and_conditions.html', context)


def customer_portal(request, contract_number):
    """Customer portal access via QR code"""
    try:
        application = get_object_or_404(InsuranceApplication, contract_number=contract_number)
        
        context = {
            'application': application,
            'portal_sections': [
                {
                    'title': 'Στοιχεία Συμβολαίου',
                    'icon': '📄',
                    'description': 'Δείτε τα στοιχεία του συμβολαίου σας'
                },
                {
                    'title': 'Ιστορικό Πληρωμών',
                    'icon': '💳',
                    'description': 'Παρακολουθήστε τις πληρωμές σας'
                },
                {
                    'title': 'Υποβολή Αξίωσης',
                    'icon': '🏥',
                    'description': 'Υποβάλετε αίτημα αποζημίωσης'
                },
                {
                    'title': 'Επικοινωνία',
                    'icon': '📞',
                    'description': 'Επικοινωνήστε μαζί μας'
                }
            ]
        }
        
        return render(request, 'qr/customer_portal.html', context)
        
    except InsuranceApplication.DoesNotExist:
        messages.error(request, 'Το συμβόλαιο δεν βρέθηκε.')
        return render(request, 'qr/portal_error.html', {'contract_number': contract_number})


@require_http_methods(["GET"])
def contract_api_verification(request, contract_number):
    """API endpoint for contract verification (JSON response)"""
    try:
        application = get_object_or_404(InsuranceApplication, contract_number=contract_number)
        
        return JsonResponse({
            'success': True,
            'contract_number': application.contract_number,
            'client_name': application.full_name,
            'pet_name': application.pet_name,
            'pet_type': application.get_pet_type_display(),
            'program': application.get_program_display(),
            'start_date': application.contract_start_date.strftime('%d/%m/%Y') if application.contract_start_date else None,
            'end_date': application.contract_end_date.strftime('%d/%m/%Y') if application.contract_end_date else None,
            'status': application.status,
        })
        
    except InsuranceApplication.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Contract not found',
            'contract_number': contract_number
        }, status=404)



