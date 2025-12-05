from django.db import models
from datetime import date, timedelta
import uuid
from django.utils import timezone

class InsuranceApplication(models.Model):
    # Administrative fields
    application_number = models.CharField(max_length=20, unique=True, blank=True, null=True, help_text="Application number like HPI10001")
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

    # Contract generation (PDF contains all application data for admin access)
    contract_generated = models.BooleanField(default=False)
    contract_pdf_path = models.CharField(max_length=500, blank=True, null=True, help_text="Contract PDF with all application data")
    
    # Ambassador/Partner Code
    affiliate_code = models.CharField(max_length=50, blank=True, null=True, db_index=True)
    discount_applied = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Discount amount applied from affiliate code")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.application_number:
            # Generate application number like HPI10001
            last_app = InsuranceApplication.objects.order_by('-id').first()
            if last_app and last_app.id:
                next_num = last_app.id + 1
            else:
                next_num = 1
            self.application_number = f"HPI{10000 + next_num}"
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

    def get_payment_frequency_display_greek(self):
        """Get Greek display for payment frequency from questionnaire"""
        try:
            if hasattr(self, 'questionnaire') and self.questionnaire:
                questionnaire = self.questionnaire
                frequency_map = {
                    'annual': 'Ετήσιο',
                    'six_month': 'Εξαμηνιαίο',
                    'three_month': 'Τριμηνιαίο'
                }
                return frequency_map.get(questionnaire.payment_frequency, '')
        except Exception:
            pass
        return ''

    def get_program_with_frequency_display(self):
        """Get combined program and payment frequency display in Greek"""
        program = self.get_program_display_greek()
        frequency = self.get_payment_frequency_display_greek()
        
        if frequency:
            return f"{program} {frequency}"
        return program

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
    order_code = models.CharField(max_length=100, unique=True, null=True, blank=True, db_index=True)
    
    # Payment details
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES, default='annual')
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=50, default='viva_wallet', blank=True)
    
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


class AmbassadorCode(models.Model):
    """Model for Ambassador and Partner discount codes"""
    
    CODE_TYPE_CHOICES = [
        ('ambassador', 'Πρέσβης'),
        ('partner', 'Συνεργάτης'),
    ]
    
    code = models.CharField(max_length=50, unique=True, db_index=True, help_text="The discount code (e.g., PARTNER2024)")
    code_type = models.CharField(max_length=20, choices=CODE_TYPE_CHOICES, default='partner')
    name = models.CharField(max_length=200, help_text="Name of the ambassador/partner")
    description = models.TextField(blank=True, help_text="Description of the code")
    
    # Discount settings
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="Percentage discount (e.g., 10.00 for 10%)")
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Fixed discount amount in euros (0 = use percentage)")
    max_discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Maximum discount amount (null = no limit)")
    
    # Usage limits
    max_uses = models.IntegerField(null=True, blank=True, help_text="Maximum number of times this code can be used (null = unlimited)")
    current_uses = models.IntegerField(default=0, help_text="Current number of times used")
    
    # Validity
    is_active = models.BooleanField(default=True)
    valid_from = models.DateTimeField(null=True, blank=True, help_text="Code valid from this date (null = no start date)")
    valid_until = models.DateTimeField(null=True, blank=True, help_text="Code valid until this date (null = no expiry)")
    
    # Tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=200, blank=True, help_text="Who created this code")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Ambassador/Partner Code'
        verbose_name_plural = 'Ambassador/Partner Codes'
        indexes = [
            models.Index(fields=['code', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.code} ({self.get_code_type_display()}) - {self.name}"
    
    def is_valid(self):
        """Check if code is currently valid"""
        if not self.is_active:
            return False
        
        # Check usage limit
        if self.max_uses and self.current_uses >= self.max_uses:
            return False
        
        # Check date validity
        now = timezone.now()
        if self.valid_from and now < self.valid_from:
            return False
        if self.valid_until and now > self.valid_until:
            return False
        
        return True
    
    def calculate_discount(self, base_amount):
        """Calculate discount amount for a given base amount"""
        if not self.is_valid():
            return 0
        
        amount = float(base_amount)
        discount = 0
        
        if self.discount_amount > 0:
            # Fixed discount amount
            discount = float(self.discount_amount)
        elif self.discount_percentage > 0:
            # Percentage discount
            discount = amount * (float(self.discount_percentage) / 100)
        
        # Apply maximum discount limit if set
        if self.max_discount and discount > float(self.max_discount):
            discount = float(self.max_discount)
        
        return round(discount, 2)
    
    def apply_discount(self, base_amount):
        """Apply discount and return final amount"""
        discount = self.calculate_discount(base_amount)
        final_amount = float(base_amount) - discount
        return round(max(0, final_amount), 2), discount
    
    def increment_usage(self):
        """Increment usage counter"""
        self.current_uses += 1
        self.save(update_fields=['current_uses', 'updated_at'])


class PetDocument(models.Model):
    """Model to store user-uploaded pet documents"""
    
    # Link to insurance application (optional - can be uploaded before application is created)
    application = models.ForeignKey(InsuranceApplication, on_delete=models.CASCADE, related_name='documents', null=True, blank=True)
    
    # Document details
    file = models.FileField(upload_to='pet_documents/%Y/%m/%d/', help_text="Uploaded pet document")
    original_filename = models.CharField(max_length=255, help_text="Original filename")
    file_size = models.IntegerField(help_text="File size in bytes")
    file_type = models.CharField(max_length=50, help_text="MIME type of the file")
    
    # Pet information (for documents uploaded before application creation)
    pet_name = models.CharField(max_length=100, blank=True, null=True)
    pet_type = models.CharField(max_length=10, choices=[('dog', 'Σκύλος'), ('cat', 'Γάτα')], blank=True, null=True)
    
    # Metadata
    uploaded_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Pet Document'
        verbose_name_plural = 'Pet Documents'
    
    def __str__(self):
        return f"Document: {self.original_filename} - {self.pet_name or 'Unknown'}"
    
    def get_file_url(self):
        """Get the URL to access the file - always use serve_file view for reliability"""
        if self.file:
            from django.urls import reverse
            # Always use serve_file view which handles S3 signed URLs on-demand
            return reverse('main:serve_file', kwargs={'file_type': 'document', 'file_id': self.id})
        return None


class PetPhoto(models.Model):
    """Model to store user-uploaded pet photos (minimum 5 required for application)"""
    
    # Link to insurance application (optional - can be uploaded before application is created)
    application = models.ForeignKey(InsuranceApplication, on_delete=models.CASCADE, related_name='photos', null=True, blank=True)
    
    # Photo details
    file = models.ImageField(upload_to='pet_photos/%Y/%m/%d/', help_text="Uploaded pet photo")
    original_filename = models.CharField(max_length=255, help_text="Original filename")
    file_size = models.IntegerField(help_text="File size in bytes")
    file_type = models.CharField(max_length=50, help_text="MIME type of the file")
    
    # Pet information (for photos uploaded before application creation)
    pet_name = models.CharField(max_length=100, blank=True, null=True)
    pet_type = models.CharField(max_length=10, choices=[('dog', 'Σκύλος'), ('cat', 'Γάτα')], blank=True, null=True)
    
    # Photo metadata
    uploaded_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Pet Photo'
        verbose_name_plural = 'Pet Photos'
    
    def __str__(self):
        return f"Photo: {self.original_filename} - {self.pet_name or 'Unknown'}"
    
    def get_file_url(self):
        """Get the URL to access the photo - always use serve_file view for reliability"""
        if self.file:
            from django.urls import reverse
            # Always use serve_file view which handles S3 signed URLs on-demand
            return reverse('main:serve_file', kwargs={'file_type': 'photo', 'file_id': self.id})
        return None


class Questionnaire(models.Model):
    """Model to store comprehensive insurance questionnaire answers"""
    
    # Link to insurance application
    application = models.OneToOneField(InsuranceApplication, on_delete=models.CASCADE, related_name='questionnaire', null=True, blank=True)
    
    # Section 1.1: Questionnaire for the Insured (YES/NO)
    has_other_insured_pet = models.BooleanField(default=False, help_text="Α. Έχετε άλλο, ήδη ασφαλιζόμενο κατοικίδιο στο ίδιο ασφαλιστικό πρόγραμμα;")
    has_been_denied_insurance = models.BooleanField(default=False, help_text="Β. Σας έχουν αρνηθεί ή ακυρώσει την ανανέωση ή σας έχουν ή αρνηθεί στο παρελθόν πρότασή σας")
    has_special_terms_imposed = models.BooleanField(default=False, help_text="Γ. Σας έχουν επιβάλλει Ειδικούς Όρους στο παρελθόν")
    
    # Section 2: Pet Details (stored in InsuranceApplication, but questionnaire may have additional info)
    pet_colors = models.CharField(max_length=200, blank=True, null=True, help_text="Χρώματα κατοικιδίου")
    pet_weight = models.CharField(max_length=50, blank=True, null=True, help_text="Βάρος")
    is_purebred = models.BooleanField(default=False, help_text="Καθαρόαιμο")
    is_mixed = models.BooleanField(default=False, help_text="Ημίαιμο")
    is_crossbreed = models.BooleanField(default=False, help_text="Διασταύρωση ράτσας")
    
    # Section 2.1: Special Breed Cases (surcharges applied in pricing)
    special_breed_5_percent = models.BooleanField(default=False, help_text="Cane Corso, Dogo Argentino, Rottweiler (5% surcharge)")
    special_breed_20_percent = models.BooleanField(default=False, help_text="Pit Bull, French Bulldog, English Bulldog, Chow Chow (20% surcharge)")
    
    # Section 2.2: Pet Questionnaire (YES/NO with details)
    is_healthy = models.BooleanField(default=True, help_text="Α. Το κατοικίδιο είναι υγιές κατά την ημερομηνία αίτησης;")
    is_healthy_details = models.TextField(blank=True, null=True, help_text="Εάν ΟΧΙ, περισσότερες λεπτομέρειες")
    
    has_injury_illness_3_years = models.BooleanField(default=False, help_text="Β. Υπήρξε τραυματισμός, ασθένεια τα τελευταία 3 έτη;")
    has_injury_illness_details = models.TextField(blank=True, null=True, help_text="Εάν ΝΑΙ, περισσότερες λεπτομέρειες")
    
    has_surgical_procedure = models.BooleanField(default=False, help_text="Γ. Έχει υποβληθεί σε χειρουργική επέμβαση;")
    has_surgical_procedure_details = models.TextField(blank=True, null=True, help_text="Εάν ΝΑΙ, περισσότερες λεπτομέρειες")
    
    has_examination_findings = models.BooleanField(default=False, help_text="Δ. Έχει υποβληθεί σε εξέταση (ακτινογραφία, MRI, υπερηχογράφημα) και υπήρξαν ευρήματα;")
    has_examination_findings_details = models.TextField(blank=True, null=True, help_text="Εάν ΝΑΙ, περισσότερες λεπτομέρειες")
    
    is_sterilized = models.BooleanField(default=False, help_text="Ε. Έχει υποβληθεί σε στείρωση;")
    
    is_vaccinated_leishmaniasis = models.BooleanField(default=False, help_text="Ζ. Το κατοικίδιο έχει εμβολιαστεί κατά της λεϊσμανίασης;")
    
    follows_vaccination_program = models.BooleanField(default=True, help_text="Η. Ακολουθεί πιστά το πρόγραμμα εμβολιασμών;")
    follows_vaccination_program_details = models.TextField(blank=True, null=True, help_text="Εάν ΟΧΙ, περισσότερες λεπτομέρειες")
    
    has_hereditary_disease = models.BooleanField(default=False, help_text="Θ. Έχει το κατοικίδιο οποιαδήποτε κληρονομική ασθένεια;")
    has_hereditary_disease_details = models.TextField(blank=True, null=True, help_text="Αν ΝΑΙ, αναφέρετε ποια/ποιες")
    
    # Section 3: Program Selection
    program = models.CharField(max_length=20, choices=[('silver', 'Silver'), ('gold', 'Gold'), ('platinum', 'Platinum'), ('dynasty', 'Dynasty')], blank=True, null=True)
    additional_poisoning_coverage = models.BooleanField(default=False, help_text="Πρόσθετη Κάλυψη Δηλητηρίασης")
    additional_blood_checkup = models.BooleanField(default=False, help_text="Επιπλέον Παροχή Προνομιακού Αιματολογικού Check-Up με 28€/έτος")
    
    # Section 4: Desired Start Date
    desired_start_date = models.DateField(blank=True, null=True, help_text="Επιθυμητή Έναρξη Ασφάλισης")
    
    # Section 5: Payment Method
    PAYMENT_METHOD_CHOICES = [
        ('card', 'Χρεωστική/Πιστωτική/Προπληρωμένη κάρτα'),
        ('bank_deposit', 'Τραπεζική κατάθεση'),
        ('cash', 'Μετρητά'),
    ]
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, blank=True, null=True)
    PAYMENT_FREQUENCY_CHOICES = [
        ('annual', 'Ετήσια Πληρωμή'),
        ('six_month', 'Εξάμηνη Πληρωμή'),
        ('three_month', 'Τριμηνιαία Πληρωμή'),
    ]
    payment_frequency = models.CharField(max_length=20, choices=PAYMENT_FREQUENCY_CHOICES, blank=True, null=True)
    
    # Section 6: Declarations - Authorizations - Consents
    consent_terms_conditions = models.BooleanField(default=False, help_text="1. Γνωρίζω ότι στην ασφάλιση αυτή ισχύουν οι Γενικοί και Ειδικοί Όροι")
    consent_info_document = models.BooleanField(default=False, help_text="2. Παρέλαβα το ενημερωτικό έντυπο")
    consent_email_notifications = models.BooleanField(default=False, help_text="3. Ενημέρωση σχετικά με ασφάλιση μέσω E-mail")
    consent_marketing = models.BooleanField(default=False, help_text="4. Ενημέρωση για διαφημιστικούς, εμπορικούς σκοπούς")
    consent_data_processing = models.BooleanField(default=False, help_text="5. Ενημέρωση σχετικά με Επεξεργασία Προσωπικών Δεδομένων")
    consent_pet_gov_platform = models.BooleanField(default=False, help_text="Συναίνεση για χρήση πλατφόρμας pet.gov.gr")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Questionnaire'
        verbose_name_plural = 'Questionnaires'
    
    def __str__(self):
        try:
            if self.application:
                app_id = self.application.application_number or self.application.contract_number or f"ID: {self.application.pk}"
                return f"Questionnaire for {app_id}"
        except Exception:
            pass
        return f"Questionnaire {self.id}"