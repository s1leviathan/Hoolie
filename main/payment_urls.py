"""
URL configuration for Viva Wallet payment views
"""
from django.urls import path
from . import payment_views

app_name = 'payments'

urlpatterns = [
    # Payment flow
    path('select/<int:application_id>/', payment_views.PaymentSelectionView.as_view(), name='payment_selection'),
    path('success/', payment_views.PaymentSuccessView.as_view(), name='payment_success'),
    path('failure/', payment_views.PaymentFailureView.as_view(), name='payment_failure'),
    
    # Webhook
    path('webhook/viva/', payment_views.VivaWalletWebhookView.as_view(), name='viva_webhook'),
    
    # Payment management
    path('status/<int:payment_id>/', payment_views.PaymentStatusView.as_view(), name='payment_status'),
    path('refund/<int:payment_id>/', payment_views.RefundPaymentView.as_view(), name='refund_payment'),
    path('history/<int:application_id>/', payment_views.payment_history, name='payment_history'),
    
    # AJAX endpoints
    path('api/options/<int:application_id>/', payment_views.get_payment_options, name='get_payment_options'),
    path('api/create-intent/', payment_views.create_payment_intent, name='create_payment_intent'),
]



