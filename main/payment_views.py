"""
Viva Wallet Payment Views for Pet Insurance
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
import json
import logging

from .models import InsuranceApplication, PaymentTransaction
from .viva_wallet import VivaWalletAPI, create_insurance_payment, verify_payment_webhook
try:
from .qr_utils import generate_payment_qr_for_application
except ImportError:
    def generate_payment_qr_for_application(application):
        return None

logger = logging.getLogger(__name__)

class PaymentSelectionView(View):
    """View for selecting payment plan and initiating payment"""
    
    def get(self, request, application_id):
        application = get_object_or_404(InsuranceApplication, id=application_id)
        
        # Calculate different payment options
        annual_amount = application.annual_premium or 0
        six_month_amount = application.six_month_premium or (annual_amount * 0.55 if annual_amount else 0)
        three_month_amount = application.three_month_premium or (annual_amount * 0.30 if annual_amount else 0)
        
        payment_options = [
            {
                'type': 'annual',
                'name': 'Ετήσια Πληρωμή',
                'amount': annual_amount,
                'description': 'Πληρώστε για ολόκληρο το έτος και εξοικονομήστε χρήματα',
                'savings': 0,
                'recommended': True
            },
            {
                'type': 'six_month',
                'name': '6μηνη Πληρωμή',
                'amount': six_month_amount,
                'description': 'Πληρώστε για 6 μήνες',
                'savings': annual_amount - (six_month_amount * 2) if annual_amount and six_month_amount else 0,
                'recommended': False
            },
            {
                'type': 'three_month',
                'name': '3μηνη Πληρωμή',
                'amount': three_month_amount,
                'description': 'Πληρώστε για 3 μήνες',
                'savings': annual_amount - (three_month_amount * 4) if annual_amount and three_month_amount else 0,
                'recommended': False
            }
        ]
        
        # Generate QR codes for each payment option
        qr_codes = {}
        try:
            for option in payment_options:
                # Create a temporary order code for QR generation
                temp_order_code = f"TEMP-{application.contract_number}-{option['plan_type']}"
                qr_data = generate_payment_qr_for_application(application, temp_order_code)
                qr_codes[option['plan_type']] = qr_data
        except Exception as e:
            logger.warning(f"Could not generate QR codes: {e}")
        
        context = {
            'application': application,
            'payment_options': payment_options,
            'qr_codes': qr_codes,
        }
        
        return render(request, 'payments/payment_selection.html', context)
    
    def post(self, request, application_id):
        application = get_object_or_404(InsuranceApplication, id=application_id)
        payment_type = request.POST.get('payment_type', 'annual')
        
        # Create Viva Wallet payment order
        result = create_insurance_payment(application, payment_type)
        
        if result['success']:
            # Create payment transaction record
            payment = PaymentTransaction.objects.create(
                application=application,
                order_code=result['order_code'],
                viva_order_code=result['order_code'],  # Store for webhook matching
                amount=result['amount'],
                payment_type=payment_type,
                status='pending',
                checkout_url=result['checkout_url'],
                response_data=result
            )
            
            # Update application status
            application.status = 'payment_pending'
            application.save()
            
            # Redirect to Viva Wallet checkout
            return redirect(result['checkout_url'])
        else:
            messages.error(request, f"Σφάλμα δημιουργίας πληρωμής: {result.get('error', 'Άγνωστο σφάλμα')}")
            return redirect('payment_selection', application_id=application_id)


class PaymentSuccessView(View):
    """View for handling successful payment returns"""
    
    def get(self, request):
        order_code = request.GET.get('s')  # Viva Wallet success parameter
        
        if not order_code:
            messages.error(request, 'Δεν βρέθηκε κωδικός παραγγελίας')
            return redirect('main:index')
        
        try:
            payment = PaymentTransaction.objects.get(order_code=order_code)
            application = payment.application
            
            # Verify payment with Viva Wallet API
            viva = VivaWalletAPI()
            if payment.viva_transaction_id:
                transaction_details = viva.get_transaction_details(payment.viva_transaction_id)
                if transaction_details and transaction_details.get('statusId') == 'F':  # F = Success
                    payment.status = 'completed'
                    payment.save()
                    
                    application.status = 'paid'
                    application.save()
            
            context = {
                'payment': payment,
                'application': application,
                'success': payment.status == 'completed'
            }
            
            return render(request, 'payments/payment_success.html', context)
            
        except PaymentTransaction.DoesNotExist:
            messages.error(request, 'Δεν βρέθηκε η πληρωμή')
            return redirect('main:index')


class PaymentFailureView(View):
    """View for handling failed payment returns"""
    
    def get(self, request):
        order_code = request.GET.get('s')  # Viva Wallet parameter
        
        if order_code:
            try:
                payment = PaymentTransaction.objects.get(order_code=order_code)
                payment.status = 'failed'
                payment.save()
                
                application = payment.application
                application.status = 'payment_failed'
                application.save()
                
                context = {
                    'payment': payment,
                    'application': application,
                }
                
                return render(request, 'payments/payment_failure.html', context)
                
            except PaymentTransaction.DoesNotExist:
                pass
        
        messages.error(request, 'Η πληρωμή απέτυχε')
        return redirect('main:index')


@method_decorator(csrf_exempt, name='dispatch')
class VivaWalletWebhookView(View):
    """View for handling Viva Wallet webhooks"""
    
    def post(self, request):
        try:
            # Verify and process webhook
            result = verify_payment_webhook(request)
            
            if result['success']:
                logger.info(f"Webhook processed successfully: {result}")
                return HttpResponse('OK', status=200)
            else:
                logger.error(f"Webhook processing failed: {result}")
                return HttpResponse('Error', status=400)
                
        except Exception as e:
            logger.error(f"Webhook error: {e}")
            return HttpResponse('Error', status=500)


class PaymentStatusView(View):
    """AJAX view for checking payment status"""
    
    def get(self, request, payment_id):
        try:
            payment = PaymentTransaction.objects.get(id=payment_id)
            
            # Check with Viva Wallet if still pending
            if payment.status == 'pending' and payment.viva_transaction_id:
                viva = VivaWalletAPI()
                transaction_details = viva.get_transaction_details(payment.viva_transaction_id)
                
                if transaction_details:
                    status_id = transaction_details.get('statusId')
                    if status_id == 'F':  # Success
                        payment.status = 'completed'
                        payment.application.status = 'paid'
                        payment.application.save()
                    elif status_id in ['E', 'X']:  # Error or Cancelled
                        payment.status = 'failed'
                        payment.application.status = 'payment_failed'
                        payment.application.save()
                    
                    payment.save()
            
            return JsonResponse({
                'status': payment.status,
                'amount': str(payment.amount),
                'payment_type': payment.get_payment_type_display(),
                'created_at': payment.created_at.isoformat(),
                'is_successful': payment.is_successful()
            })
            
        except PaymentTransaction.DoesNotExist:
            return JsonResponse({'error': 'Payment not found'}, status=404)


class RefundPaymentView(View):
    """View for processing refunds (admin only)"""
    
    def post(self, request, payment_id):
        # Check if user is admin/staff
        if not request.user.is_staff:
            return JsonResponse({'error': 'Unauthorized'}, status=403)
        
        try:
            payment = PaymentTransaction.objects.get(id=payment_id)
            
            if not payment.can_be_refunded():
                return JsonResponse({'error': 'Payment cannot be refunded'}, status=400)
            
            refund_amount = request.POST.get('amount')
            reason = request.POST.get('reason', 'Admin refund')
            
            viva = VivaWalletAPI()
            result = viva.create_refund(
                payment.viva_transaction_id,
                amount=refund_amount,
                reason=reason
            )
            
            if result['success']:
                # Update payment record
                if refund_amount:
                    payment.refund_amount = float(refund_amount)
                    payment.status = 'partially_refunded' if float(refund_amount) < payment.amount else 'refunded'
                else:
                    payment.refund_amount = payment.amount
                    payment.status = 'refunded'
                
                payment.refund_reason = reason
                payment.save()
                
                return JsonResponse({
                    'success': True,
                    'message': 'Refund processed successfully',
                    'refund_amount': str(payment.refund_amount)
                })
            else:
                return JsonResponse({'error': result.get('error', 'Refund failed')}, status=400)
                
        except PaymentTransaction.DoesNotExist:
            return JsonResponse({'error': 'Payment not found'}, status=404)


def payment_history(request, application_id):
    """View for displaying payment history of an application"""
    application = get_object_or_404(InsuranceApplication, id=application_id)
    payments = PaymentTransaction.objects.filter(application=application).order_by('-created_at')
    
    context = {
        'application': application,
        'payments': payments,
    }
    
    return render(request, 'payments/payment_history.html', context)


# Utility views for AJAX calls
@require_http_methods(["GET"])
def get_payment_options(request, application_id):
    """AJAX endpoint to get payment options for an application"""
    try:
        application = InsuranceApplication.objects.get(id=application_id)
        
        annual_amount = float(application.annual_premium or 0)
        six_month_amount = float(application.six_month_premium or (annual_amount * 0.55))
        three_month_amount = float(application.three_month_premium or (annual_amount * 0.30))
        
        options = {
            'annual': {
                'amount': annual_amount,
                'name': 'Ετήσια Πληρωμή',
                'savings': 0
            },
            'six_month': {
                'amount': six_month_amount,
                'name': '6μηνη Πληρωμή',
                'savings': annual_amount - (six_month_amount * 2)
            },
            'three_month': {
                'amount': three_month_amount,
                'name': '3μηνη Πληρωμή',
                'savings': annual_amount - (three_month_amount * 4)
            }
        }
        
        return JsonResponse({'success': True, 'options': options})
        
    except InsuranceApplication.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Application not found'})


@csrf_exempt
@require_http_methods(["POST"])
def create_payment_intent(request):
    """AJAX endpoint to create payment intent"""
    try:
        data = json.loads(request.body)
        application_id = data.get('application_id')
        payment_type = data.get('payment_type', 'annual')
        
        application = InsuranceApplication.objects.get(id=application_id)
        
        # Create payment order
        result = create_insurance_payment(application, payment_type)
        
        if result['success']:
            # Create payment transaction record
            payment = PaymentTransaction.objects.create(
                application=application,
                order_code=result['order_code'],
                viva_order_code=result['order_code'],  # Store for webhook matching
                amount=result['amount'],
                payment_type=payment_type,
                status='pending',
                checkout_url=result['checkout_url'],
                response_data=result
            )
            
            return JsonResponse({
                'success': True,
                'checkout_url': result['checkout_url'],
                'order_code': result['order_code'],
                'amount': result['amount'],
                'payment_id': payment.id
            })
        else:
            return JsonResponse({
                'success': False,
                'error': result.get('error', 'Payment creation failed')
            })
            
    except Exception as e:
        logger.error(f"Payment intent creation error: {e}")
        return JsonResponse({'success': False, 'error': str(e)})
