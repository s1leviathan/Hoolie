"""
URL patterns for QR code related views
"""
from django.urls import path
from . import qr_views

app_name = 'qr'

urlpatterns = [
    # Contract verification via QR code
    path('contract/verify/<str:contract_number>/', qr_views.contract_verification, name='contract_verification'),
    
    # Terms and conditions via QR code
    path('terms-and-conditions/', qr_views.terms_and_conditions, name='terms_and_conditions'),
    
    # Customer portal via QR code
    path('customer/portal/<str:contract_number>/', qr_views.customer_portal, name='customer_portal'),
    
    # API endpoint for contract verification
    path('api/contract/verify/<str:contract_number>/', qr_views.contract_api_verification, name='api_contract_verification'),
]



