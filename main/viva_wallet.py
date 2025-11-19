"""
Viva Wallet API Integration for Pet Insurance Payments
"""
import requests
import json
import base64
import hashlib
import hmac
from datetime import datetime, timedelta
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

class VivaWalletAPI:
    """Viva Wallet API integration class"""
    
    def __init__(self):
        # These should be in your settings.py
        self.merchant_id = getattr(settings, 'VIVA_WALLET_MERCHANT_ID', '')
        self.source_code = getattr(settings, 'VIVA_WALLET_SOURCE_CODE', '')
        self.client_id = getattr(settings, 'VIVA_WALLET_CLIENT_ID', '')
        self.client_secret = getattr(settings, 'VIVA_WALLET_CLIENT_SECRET', '')
        
        # Environment URLs
        self.is_production = getattr(settings, 'VIVA_WALLET_PRODUCTION', False)
        if self.is_production:
            self.api_base_url = "https://api.viva.com"
            self.checkout_url = "https://www.viva.com"
        else:
            self.api_base_url = "https://demo-api.viva.com"
            self.checkout_url = "https://demo.viva.com"
    
    def get_access_token(self):
        """Get OAuth2 access token for API authentication"""
        url = f"{self.api_base_url}/oauth2/token"
        
        # Encode credentials
        credentials = f"{self.client_id}:{self.client_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        
        headers = {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        data = {
            'grant_type': 'client_credentials'
        }
        
        try:
            response = requests.post(url, headers=headers, data=data)
            response.raise_for_status()
            return response.json().get('access_token')
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get Viva Wallet access token: {e}")
            return None
    
    def create_payment_order(self, application, payment_type='annual'):
        """
        Create a payment order for insurance application
        
        Args:
            application: InsuranceApplication instance
            payment_type: 'annual', 'six_month', or 'three_month'
        
        Returns:
            dict: Payment order response with order_code and checkout URL
        """
        access_token = self.get_access_token()
        if not access_token:
            return {'success': False, 'error': 'Failed to authenticate with Viva Wallet'}
        
        # Calculate amount based on payment type
        amount_mapping = {
            'annual': application.annual_premium,
            'six_month': getattr(application, 'six_month_premium', None),
            'three_month': getattr(application, 'three_month_premium', None)
        }
        
        amount = amount_mapping.get(payment_type, application.annual_premium)
        if not amount:
            return {'success': False, 'error': 'Invalid payment amount'}
        
        # Convert to cents (Viva Wallet uses cents)
        amount_cents = int(float(amount) * 100)
        
        url = f"{self.api_base_url}/checkout/v2/orders"
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        # Prepare order data
        order_data = {
            'amount': amount_cents,
            'customerTrns': f"Pet Insurance - {application.contract_number} ({payment_type})",
            'customer': {
                'email': application.email,
                'fullName': application.full_name,
                'phone': application.phone,
                'countryCode': 'GR',
                'requestLang': 'el-GR'
            },
            'paymentTimeout': 1800,  # 30 minutes
            'preauth': False,
            'allowRecurring': False,
            'maxInstallments': 0,
            'paymentNotification': True,
            'tipAmount': 0,
            'disableExactAmount': False,
            'disableCash': True,
            'disableWallet': False,
            'sourceCode': self.source_code,
            'merchantTrns': f"Contract: {application.contract_number}",
            'tags': [
                'pet-insurance',
                f'contract-{application.contract_number}',
                f'payment-{payment_type}',
                f'pet-{application.pet_type}'
            ]
        }
        
        try:
            response = requests.post(url, headers=headers, json=order_data)
            response.raise_for_status()
            
            result = response.json()
            order_code = result.get('orderCode')
            
            if order_code:
                checkout_url = f"{self.checkout_url}/web/checkout?ref={order_code}"
                return {
                    'success': True,
                    'order_code': order_code,
                    'checkout_url': checkout_url,
                    'amount': amount,
                    'payment_type': payment_type
                }
            else:
                return {'success': False, 'error': 'No order code received'}
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to create Viva Wallet payment order: {e}")
            return {'success': False, 'error': str(e)}
    
    def verify_webhook_signature(self, payload, signature):
        """Verify webhook signature for security"""
        if not self.client_secret:
            return False
        
        expected_signature = hmac.new(
            self.client_secret.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(signature, expected_signature)
    
    def get_transaction_details(self, transaction_id):
        """Get transaction details by transaction ID"""
        access_token = self.get_access_token()
        if not access_token:
            return None
        
        url = f"{self.api_base_url}/checkout/v2/transactions/{transaction_id}"
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get transaction details: {e}")
            return None
    
    def create_refund(self, transaction_id, amount=None, reason="Customer request"):
        """Create a refund for a transaction"""
        access_token = self.get_access_token()
        if not access_token:
            return {'success': False, 'error': 'Failed to authenticate'}
        
        url = f"{self.api_base_url}/checkout/v2/transactions/{transaction_id}/refunds"
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        refund_data = {
            'reason': reason
        }
        
        if amount:
            refund_data['amount'] = int(float(amount) * 100)  # Convert to cents
        
        try:
            response = requests.post(url, headers=headers, json=refund_data)
            response.raise_for_status()
            return {'success': True, 'data': response.json()}
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to create refund: {e}")
            return {'success': False, 'error': str(e)}

# Utility functions
def create_insurance_payment(application, payment_type='annual'):
    """
    Create a payment for an insurance application
    
    Args:
        application: InsuranceApplication instance
        payment_type: 'annual', 'six_month', or 'three_month'
    
    Returns:
        dict: Payment creation result
    """
    viva = VivaWalletAPI()
    return viva.create_payment_order(application, payment_type)

def verify_payment_webhook(request):
    """
    Verify and process a Viva Wallet webhook
    
    Args:
        request: Django request object
    
    Returns:
        dict: Webhook processing result
    """
    try:
        payload = request.body.decode('utf-8')
        signature = request.headers.get('X-Viva-Signature', '')
        
        viva = VivaWalletAPI()
        
        if not viva.verify_webhook_signature(payload, signature):
            return {'success': False, 'error': 'Invalid signature'}
        
        webhook_data = json.loads(payload)
        
        # Process webhook based on event type
        event_type = webhook_data.get('eventTypeId')
        
        if event_type == 1796:  # Payment completed
            return process_payment_success(webhook_data)
        elif event_type == 1797:  # Payment failed
            return process_payment_failure(webhook_data)
        elif event_type == 1798:  # Payment refunded
            return process_payment_refund(webhook_data)
        
        return {'success': True, 'message': 'Webhook processed'}
        
    except Exception as e:
        logger.error(f"Webhook processing error: {e}")
        return {'success': False, 'error': str(e)}

def process_payment_success(webhook_data):
    """Process successful payment webhook"""
    from .models import InsuranceApplication, PaymentTransaction
    
    try:
        event_data = webhook_data.get('eventData', {})
        transaction_id = event_data.get('transactionId')
        order_code = event_data.get('orderCode')
        amount = event_data.get('amount', 0) / 100  # Convert from cents
        
        # Find existing payment transaction by order_code
        try:
            payment = PaymentTransaction.objects.get(order_code=order_code)
            
            # Update payment with transaction details
            payment.viva_transaction_id = transaction_id
            payment.transaction_id = transaction_id
            payment.status = 'completed'
            payment.completed_at = timezone.now()
            payment.webhook_data = webhook_data
            payment.save()
            
            # Update application status
            application = payment.application
            application.status = 'paid'
            application.save()
            
            logger.info(f"Payment completed: {transaction_id}, Order: {order_code}, Amount: {amount}€")
            return {'success': True, 'message': 'Payment processed successfully'}
            
        except PaymentTransaction.DoesNotExist:
            # Try to find by viva_order_code if order_code doesn't match
            try:
                payment = PaymentTransaction.objects.get(viva_order_code=order_code)
                payment.viva_transaction_id = transaction_id
                payment.transaction_id = transaction_id
                payment.status = 'completed'
                payment.completed_at = timezone.now()
                payment.webhook_data = webhook_data
                payment.save()
                
                application = payment.application
                application.status = 'paid'
                application.save()
                
                logger.info(f"Payment completed (by viva_order_code): {transaction_id}, Order: {order_code}")
                return {'success': True, 'message': 'Payment processed successfully'}
            except PaymentTransaction.DoesNotExist:
                logger.error(f"Payment transaction not found for order_code: {order_code}")
                return {'success': False, 'error': f'Payment transaction not found for order: {order_code}'}
        
    except Exception as e:
        logger.error(f"Payment success processing error: {e}")
        return {'success': False, 'error': str(e)}

def process_payment_failure(webhook_data):
    """Process failed payment webhook"""
    from .models import InsuranceApplication, PaymentTransaction
    
    try:
        event_data = webhook_data.get('eventData', {})
        order_code = event_data.get('orderCode')
        
        if order_code:
            try:
                payment = PaymentTransaction.objects.get(order_code=order_code)
                payment.status = 'failed'
                payment.webhook_data = webhook_data
                payment.save()
                
                application = payment.application
                application.status = 'payment_failed'
                application.save()
                
                logger.warning(f"Payment failed: Order {order_code}")
                return {'success': True, 'message': 'Payment failure processed'}
            except PaymentTransaction.DoesNotExist:
                logger.warning(f"Payment transaction not found for failed order: {order_code}")
        
        logger.warning(f"Payment failed: {webhook_data}")
        return {'success': True, 'message': 'Payment failure processed'}
        
    except Exception as e:
        logger.error(f"Payment failure processing error: {e}")
        return {'success': False, 'error': str(e)}

def process_payment_refund(webhook_data):
    """Process refund webhook"""
    from .models import InsuranceApplication, PaymentTransaction
    
    try:
        event_data = webhook_data.get('eventData', {})
        transaction_id = event_data.get('transactionId')
        refund_amount = event_data.get('amount', 0) / 100  # Convert from cents
        
        if transaction_id:
            try:
                payment = PaymentTransaction.objects.get(viva_transaction_id=transaction_id)
                
                # Update refund information
                if payment.refund_amount:
                    payment.refund_amount += refund_amount
                else:
                    payment.refund_amount = refund_amount
                
                if payment.refund_amount >= payment.amount:
                    payment.status = 'refunded'
                else:
                    payment.status = 'partially_refunded'
                
                payment.refunded_at = timezone.now()
                payment.webhook_data = webhook_data
                payment.save()
                
                logger.info(f"Payment refunded: Transaction {transaction_id}, Amount: {refund_amount}€")
                return {'success': True, 'message': 'Refund processed'}
            except PaymentTransaction.DoesNotExist:
                logger.warning(f"Payment transaction not found for refund: {transaction_id}")
        
        logger.info(f"Payment refunded: {webhook_data}")
        return {'success': True, 'message': 'Refund processed'}
        
    except Exception as e:
        logger.error(f"Refund processing error: {e}")
        return {'success': False, 'error': str(e)}
