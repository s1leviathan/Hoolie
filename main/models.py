from django.db import models
from datetime import date, timedelta
import uuid
from django.utils import timezone

class InsuranceApplication(models.Model):
    # Administrative fields
    contract_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    receipt_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    payment_code = models.CharField(max_length=50, unique=True, blank=True, null=True)
    contract_start_date = models.DateField(blank=True, null=True)
    contract_end_date = models.DateField(blank=True, null=True)
    submission_date = models.DateTimeField(auto_now_add=True)

    # User information
    full_name = models.CharField(max_length=255)
    afm = models.CharField(max_length=10)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=10)
    email = models.EmailField()
    microchip_number = models.CharField(max_length=50, blank=True, null=True)

    # First Pet information
    pet_name = models.CharField(max_length=100)
    pet_type = models.CharField(max_length=10, choices=[('dog', 'Σκύλος'), ('cat', 'Γάτα')])
    pet_gender = models.CharField(max_length=10, choices=[('male', 'Αρσενικό'), ('female', 'Θηλυκό')])
    pet_breed = models.CharField(max_length=100)
    pet_birthdate = models.DateField()
    pet_weight_category = models.CharField(max_length=10, blank=True, null=True)

    # Second Pet information (optional)
    has_second_pet = models.BooleanField(default=False)
    second_pet_name = models.CharField(max_length=100, blank=True, null=True)
    second_pet_type = models.CharField(max_length=10, choices=[('dog', 'Σκύλος'), ('cat', 'Γάτα')], blank=True, null=True)
    second_pet_gender = models.CharField(max_length=10, choices=[('male', 'Αρσενικό'), ('female', 'Θηλυκό')], blank=True, null=True)
    second_pet_breed = models.CharField(max_length=100, blank=True, null=True)
    second_pet_birthdate = models.DateField(blank=True, null=True)
    second_pet_weight_category = models.CharField(max_length=10, blank=True, null=True)

    # Insurance details
    program = models.CharField(max_length=20, choices=[('silver', 'Silver'), ('gold', 'Gold'), ('platinum', 'Platinum')])
    health_status = models.CharField(max_length=20, choices=[('healthy', 'Υγιές'), ('problems', 'Με προβλήματα')])
    health_conditions = models.TextField(blank=True, null=True)
    second_pet_health_status = models.CharField(max_length=20, choices=[('healthy', 'Υγιές'), ('problems', 'Με προβλήματα')], blank=True, null=True)
    second_pet_health_conditions = models.TextField(blank=True, null=True)

    # Pricing
    annual_premium = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    six_month_premium = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    three_month_premium = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # Status
    STATUS_CHOICES = [
        ('draft', 'Προσχέδιο'),
        ('submitted', 'Υποβλήθηκε'),
        ('payment_pending', 'Εκκρεμής Πληρωμή'),
        ('payment_failed', 'Αποτυχία Πληρωμής'),
        ('paid', 'Πληρώθηκε'),
        ('approved', 'Εγκρίθηκε'),
        ('active', 'Ενεργό'),
        ('rejected', 'Απορρίφθηκε'),
        ('cancelled', 'Ακυρώθηκε'),
        ('contact_form', 'Φόρμα Επικοινωνίας'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')

    # Contract generation
    contract_generated = models.BooleanField(default=False)
    contract_pdf_path = models.CharField(max_length=500, blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.contract_number:
            self.contract_number = f"HOL-{timezone.now().year}-{str(uuid.uuid4())[:6].upper()}"
        if not self.receipt_number:
            self.receipt_number = f"REC-{timezone.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:3].upper()}"
        if not self.payment_code:
            self.payment_code = str(uuid.uuid4()).replace('-', '')[:12].upper()
        if not self.contract_start_date:
            self.contract_start_date = timezone.now().date()
        if not self.contract_end_date:
            self.contract_end_date = self.contract_start_date + timedelta(days=364)
        super().save(*args, **kwargs)

    def get_pet_type_display_greek(self):
        return dict(self._meta.get_field('pet_type').choices).get(self.pet_type, self.pet_type)

    def get_program_display_greek(self):
        program_map = {
            'silver': 'Ασημένιο',
            'gold': 'Χρυσό',
            'platinum': 'Πλατινένιο'
        }
        return program_map.get(self.program, self.program)

    def get_weight_display(self, weight_category):
        weight_map = {
            '10': 'έως 10 κιλά',
            '11-20': '11-20 κιλά',
            '21-40': '21-40 κιλά',
            '>40': '>40 κιλά'
        }
        return weight_map.get(weight_category, weight_category)

    def __str__(self):
        return f"Application {self.contract_number} - {self.full_name}"


class PaymentTransaction(models.Model):
    """Model to track Viva Wallet payment transactions"""
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Εκκρεμής'),
        ('completed', 'Ολοκληρώθηκε'),
        ('failed', 'Αποτυχία'),
        ('cancelled', 'Ακυρώθηκε'),
        ('refunded', 'Επιστράφηκε'),
        ('partially_refunded', 'Μερικώς Επιστράφηκε'),
    ]
    
    PAYMENT_TYPE_CHOICES = [
        ('annual', 'Ετήσια Πληρωμή'),
        ('six_month', '6μηνη Πληρωμή'),
        ('three_month', '3μηνη Πληρωμή'),
    ]
    
    # Link to insurance application
    application = models.ForeignKey(InsuranceApplication, on_delete=models.CASCADE, related_name='payments')
    
    # Viva Wallet transaction details
    transaction_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    order_code = models.CharField(max_length=100, unique=True)
    
    # Payment details
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES, default='annual')
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=50, default='viva_wallet')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Viva Wallet specific data
    viva_transaction_id = models.CharField(max_length=100, null=True, blank=True)
    viva_order_code = models.CharField(max_length=100, null=True, blank=True)
    checkout_url = models.URLField(null=True, blank=True)
    
    # Webhook and response data
    webhook_data = models.JSONField(null=True, blank=True)
    response_data = models.JSONField(null=True, blank=True)
    
    # Refund information
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    refund_reason = models.TextField(null=True, blank=True)
    refunded_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Payment Transaction'
        verbose_name_plural = 'Payment Transactions'
    
    def __str__(self):
        return f"Payment {self.order_code} - {self.application.contract_number} - {self.amount}€"
    
    def is_successful(self):
        return self.status == 'completed'
    
    def can_be_refunded(self):
        return self.status == 'completed' and not self.refund_amount


class PaymentPlan(models.Model):
    """Model for different payment plans and pricing"""
    
    PLAN_TYPE_CHOICES = [
        ('annual', 'Ετήσιο'),
        ('six_month', '6μηνο'),
        ('three_month', '3μηνο'),
    ]
    
    name = models.CharField(max_length=100)
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPE_CHOICES)
    description = models.TextField(blank=True)
    
    # Pricing modifiers
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    additional_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Plan features
    installments = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['plan_type', 'name']
        verbose_name = 'Payment Plan'
        verbose_name_plural = 'Payment Plans'
    
    def __str__(self):
        return f"{self.name} ({self.get_plan_type_display()})"
    
    def calculate_amount(self, base_amount):
        """Calculate the final amount based on plan modifiers"""
        amount = float(base_amount)
        
        # Apply discount
        if self.discount_percentage > 0:
            amount = amount * (1 - float(self.discount_percentage) / 100)
        
        # Add additional fee
        amount += float(self.additional_fee)
        
        return round(amount, 2)