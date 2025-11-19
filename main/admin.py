from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import InsuranceApplication, PaymentTransaction, PaymentPlan, AmbassadorCode

@admin.register(InsuranceApplication)
class InsuranceApplicationAdmin(admin.ModelAdmin):
    """Admin interface for Insurance Applications"""
    
    list_display = [
        'contract_number', 
        'full_name', 
        'pet_name', 
        'pet_type_display',
        'program_display', 
        'status_display',
        'annual_premium',
        'affiliate_code_display',
        'created_at',
        'contract_actions'
    ]
    
    list_filter = [
        'status',
        'pet_type',
        'program',
        'has_second_pet',
        'contract_generated',
        'affiliate_code',
        'created_at',
        'contract_start_date'
    ]
    
    search_fields = [
        'contract_number',
        'receipt_number',
        'payment_code',
        'full_name',
        'email',
        'phone',
        'afm',
        'pet_name',
        'second_pet_name',
        'affiliate_code'
    ]
    
    readonly_fields = [
        'contract_number',
        'receipt_number', 
        'payment_code',
        'created_at',
        'updated_at',
        'contract_start_date',
        'contract_end_date'
    ]
    
    fieldsets = (
        ('📋 Διοικητικά Στοιχεία', {
            'fields': (
                'contract_number',
                'receipt_number',
                'payment_code',
                'status',
                'contract_generated',
                'contract_pdf_path'
            )
        }),
        ('📅 Ημερομηνίες', {
            'fields': (
                'created_at',
                'updated_at',
                'contract_start_date',
                'contract_end_date'
            )
        }),
        ('👤 Στοιχεία Πελάτη', {
            'fields': (
                'full_name',
                'afm',
                'phone',
                'email',
                'address',
                'postal_code'
            )
        }),
        ('🐾 Στοιχεία 1ου Κατοικιδίου', {
            'fields': (
                'pet_name',
                'pet_type',
                'pet_gender',
                'pet_breed',
                'pet_birthdate',
                'pet_weight_category',
                'microchip_number',
                'health_status',
                'health_conditions'
            )
        }),
        ('🐕 Στοιχεία 2ου Κατοικιδίου', {
            'fields': (
                'has_second_pet',
                'second_pet_name',
                'second_pet_type',
                'second_pet_gender',
                'second_pet_breed',
                'second_pet_birthdate',
                'second_pet_weight_category',
                'second_pet_health_status',
                'second_pet_health_conditions'
            ),
            'classes': ('collapse',)
        }),
        ('🛡️ Στοιχεία Ασφάλισης', {
            'fields': (
                'program',
                'annual_premium',
                'six_month_premium',
                'three_month_premium'
            )
        }),
        ('🎁 Κωδικός Συνεργάτη', {
            'fields': (
                'affiliate_code',
                'discount_applied'
            ),
            'classes': ('collapse',)
        })
    )
    
    def pet_type_display(self, obj):
        """Display pet type with emoji"""
        if obj.pet_type == 'dog':
            return "🐕 Σκύλος"
        elif obj.pet_type == 'cat':
            return "🐱 Γάτα"
        return obj.pet_type
    pet_type_display.short_description = 'Είδος'
    
    def program_display(self, obj):
        """Display program with color coding"""
        colors = {
            'silver': '#C0C0C0',
            'gold': '#FFD700', 
            'platinum': '#E5E4E2'
        }
        color = colors.get(obj.program, '#000')
        program_names = {
            'silver': 'Ασημένιο',
            'gold': 'Χρυσό',
            'platinum': 'Πλατινένιο'
        }
        name = program_names.get(obj.program, obj.program)
        return format_html(
            '<span style="color: {}; font-weight: bold;">🏆 {}</span>',
            color, name
        )
    program_display.short_description = 'Πρόγραμμα'
    
    def status_display(self, obj):
        """Display status with color coding"""
        colors = {
            'draft': '#6c757d',
            'submitted': '#007bff',
            'approved': '#28a745',
            'rejected': '#dc3545',
            'active': '#17a2b8',
            'expired': '#6f42c1'
        }
        color = colors.get(obj.status, '#000')
        return format_html(
            '<span style="color: {}; font-weight: bold;">●</span> {}',
            color, obj.get_status_display()
        )
    status_display.short_description = 'Κατάσταση'
    
    def affiliate_code_display(self, obj):
        """Display affiliate code with discount if applied"""
        if obj.affiliate_code:
            if obj.discount_applied > 0:
                return format_html(
                    '<span style="color: #28a745; font-weight: bold;">🎁 {}</span><br><small>-{}€</small>',
                    obj.affiliate_code,
                    obj.discount_applied
                )
            return format_html('<span style="color: #17a2b8;">🎁 {}</span>', obj.affiliate_code)
        return '-'
    affiliate_code_display.short_description = 'Κωδικός'
    
    def contract_actions(self, obj):
        """Display action buttons"""
        actions = []
        
        if not obj.contract_generated:
            generate_url = reverse('admin:generate_contract', args=[obj.pk])
            actions.append(
                f'<a href="{generate_url}" class="button" style="background: #28a745; color: white; padding: 5px 10px; text-decoration: none; border-radius: 3px;">📄 Δημιουργία Συμβολαίου</a>'
            )
        else:
            view_url = reverse('admin:view_contract', args=[obj.pk])
            actions.append(
                f'<a href="{view_url}" class="button" style="background: #007bff; color: white; padding: 5px 10px; text-decoration: none; border-radius: 3px;">👁️ Προβολή Συμβολαίου</a>'
            )
        
        return format_html(' '.join(actions))
    contract_actions.short_description = 'Ενέργειες'
    contract_actions.allow_tags = True
    
    def get_urls(self):
        """Add custom URLs for contract actions"""
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:application_id>/generate-contract/',
                self.admin_site.admin_view(self.generate_contract_view),
                name='generate_contract'
            ),
            path(
                '<int:application_id>/view-contract/',
                self.admin_site.admin_view(self.view_contract_view),
                name='view_contract'
            ),
        ]
        return custom_urls + urls
    
    def generate_contract_view(self, request, application_id):
        """Generate contract PDF(s)"""
        from django.http import HttpResponse, HttpResponseRedirect
        from django.contrib import messages
        from .utils import generate_contract_pdf
        
        try:
            application = InsuranceApplication.objects.get(pk=application_id)
            result = generate_contract_pdf(application)
            
            application.contract_generated = True
            
            # Handle both single and multiple contracts
            if isinstance(result, list):
                # Multiple contracts for two pets
                contract_paths = ', '.join(result)
                application.contract_pdf_path = result[0]  # Store first contract path
                messages.success(request, f'Δημιουργήθηκαν 2 συμβόλαια επιτυχώς: {contract_paths}')
            else:
                # Single contract
                application.contract_pdf_path = result
                messages.success(request, f'Το συμβόλαιο δημιουργήθηκε επιτυχώς: {result}')
            
            application.save()
            
        except Exception as e:
            messages.error(request, f'Σφάλμα κατά τη δημιουργία του συμβολαίου: {str(e)}')
        
        return HttpResponseRedirect(reverse('admin:main_insuranceapplication_changelist'))
    
    def view_contract_view(self, request, application_id):
        """View generated contract(s)"""
        from django.http import FileResponse, Http404, HttpResponse
        import os
        import zipfile
        from io import BytesIO
        
        try:
            application = InsuranceApplication.objects.get(pk=application_id)
            
            if not application.contract_pdf_path:
                raise Http404("Το συμβόλαιο δεν βρέθηκε")
            
            # Check if there are multiple contracts (two pets)
            if application.has_second_pet and application.second_pet_name:
                # Look for both pet contracts
                base_dir = os.path.dirname(application.contract_pdf_path)
                contract_files = []
                
                # Find all contract files for this application
                for filename in os.listdir(base_dir):
                    if (filename.startswith(f'contract_{application.contract_number}_pet') and 
                        filename.endswith('.pdf')):
                        filepath = os.path.join(base_dir, filename)
                        if os.path.exists(filepath):
                            contract_files.append((filename, filepath))
                
                if len(contract_files) > 1:
                    # Create ZIP file with both contracts
                    zip_buffer = BytesIO()
                    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
                        for filename, filepath in contract_files:
                            with open(filepath, 'rb') as pdf_file:
                                zip_file.writestr(filename, pdf_file.read())
                    
                    zip_buffer.seek(0)
                    response = HttpResponse(zip_buffer.read(), content_type='application/zip')
                    response['Content-Disposition'] = f'attachment; filename="{application.contract_number}_contracts.zip"'
                    return response
            
            # Single contract or fallback
            if not os.path.exists(application.contract_pdf_path):
                raise Http404("Το συμβόλαιο δεν βρέθηκε")
            
            return FileResponse(
                open(application.contract_pdf_path, 'rb'),
                as_attachment=False,
                filename=f'contract_{application.contract_number}.pdf'
            )
            
        except InsuranceApplication.DoesNotExist:
            raise Http404("Η αίτηση δεν βρέθηκε")
    
    def has_add_permission(self, request):
        """Disable manual addition - only through the application flow"""
        return False


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    """Admin interface for Payment Transactions"""
    
    list_display = [
        'order_code',
        'application_link',
        'amount',
        'payment_type_display',
        'status_display',
        'payment_method',
        'created_at',
        'completed_at',
        'refund_info'
    ]
    
    list_filter = [
        'status',
        'payment_type',
        'payment_method',
        'created_at',
        'completed_at'
    ]
    
    search_fields = [
        'order_code',
        'transaction_id',
        'viva_transaction_id',
        'viva_order_code',
        'application__contract_number',
        'application__full_name',
        'application__email'
    ]
    
    readonly_fields = [
        'transaction_id',
        'order_code',
        'viva_transaction_id',
        'viva_order_code',
        'created_at',
        'updated_at',
        'completed_at',
        'refunded_at',
        'webhook_data',
        'response_data'
    ]
    
    fieldsets = (
        ('📋 Βασικές Πληροφορίες', {
            'fields': (
                'application',
                'order_code',
                'transaction_id',
                'status',
                'payment_type',
                'payment_method'
            )
        }),
        ('💰 Ποσά', {
            'fields': (
                'amount',
                'refund_amount',
                'refund_reason'
            )
        }),
        ('🔗 Viva Wallet', {
            'fields': (
                'viva_transaction_id',
                'viva_order_code',
                'checkout_url'
            )
        }),
        ('📅 Χρονοσήματα', {
            'fields': (
                'created_at',
                'updated_at',
                'completed_at',
                'refunded_at'
            )
        }),
        ('📊 Δεδομένα', {
            'fields': (
                'webhook_data',
                'response_data'
            ),
            'classes': ('collapse',)
        })
    )
    
    def application_link(self, obj):
        """Link to the related application"""
        if obj.application:
            url = reverse('admin:main_insuranceapplication_change', args=[obj.application.pk])
            return format_html('<a href="{}">{}</a>', url, obj.application.contract_number)
        return '-'
    application_link.short_description = 'Αίτηση'
    
    def payment_type_display(self, obj):
        """Display payment type in Greek"""
        types = {
            'annual': 'Ετήσια',
            'six_month': '6μηνη',
            'three_month': '3μηνη'
        }
        return types.get(obj.payment_type, obj.payment_type)
    payment_type_display.short_description = 'Τύπος Πληρωμής'
    
    def status_display(self, obj):
        """Display status with color coding"""
        colors = {
            'pending': '#ffc107',
            'completed': '#28a745',
            'failed': '#dc3545',
            'cancelled': '#6c757d',
            'refunded': '#17a2b8',
            'partially_refunded': '#fd7e14'
        }
        color = colors.get(obj.status, '#000')
        return format_html(
            '<span style="color: {}; font-weight: bold;">●</span> {}',
            color, obj.get_status_display()
        )
    status_display.short_description = 'Κατάσταση'
    
    def refund_info(self, obj):
        """Display refund information"""
        if obj.refund_amount:
            return format_html(
                '<span style="color: #dc3545;">💰 Επιστροφή: {}€</span><br><small>{}</small>',
                obj.refund_amount,
                obj.refund_reason or 'Χωρίς λόγο'
            )
        return '-'
    refund_info.short_description = 'Επιστροφή'
    
    def has_add_permission(self, request):
        """Disable manual addition - payments are created through the payment flow"""
        return False


@admin.register(PaymentPlan)
class PaymentPlanAdmin(admin.ModelAdmin):
    """Admin interface for Payment Plans"""
    
    list_display = [
        'name',
        'plan_type_display',
        'discount_percentage',
        'additional_fee',
        'installments',
        'is_active',
        'created_at'
    ]
    
    list_filter = [
        'plan_type',
        'is_active',
        'created_at'
    ]
    
    search_fields = [
        'name',
        'description'
    ]
    
    fieldsets = (
        ('📋 Βασικές Πληροφορίες', {
            'fields': (
                'name',
                'plan_type',
                'description',
                'is_active'
            )
        }),
        ('💰 Τιμολόγηση', {
            'fields': (
                'discount_percentage',
                'additional_fee',
                'installments'
            )
        }),
        ('📅 Χρονοσήματα', {
            'fields': (
                'created_at',
                'updated_at'
            ),
            'classes': ('collapse',)
        })
    )
    
    def plan_type_display(self, obj):
        """Display plan type in Greek"""
        types = {
            'annual': 'Ετήσιο',
            'six_month': '6μηνο',
            'three_month': '3μηνο'
        }
        return types.get(obj.plan_type, obj.plan_type)
    plan_type_display.short_description = 'Τύπος Σχεδίου'


@admin.register(AmbassadorCode)
class AmbassadorCodeAdmin(admin.ModelAdmin):
    """Admin interface for Ambassador/Partner Codes"""
    
    list_display = [
        'code',
        'code_type_display',
        'name',
        'discount_display',
        'usage_display',
        'is_active',
        'validity_display',
        'created_at'
    ]
    
    list_filter = [
        'code_type',
        'is_active',
        'created_at',
        'valid_from',
        'valid_until'
    ]
    
    search_fields = [
        'code',
        'name',
        'description',
        'created_by'
    ]
    
    readonly_fields = [
        'created_at',
        'updated_at',
        'current_uses'
    ]
    
    fieldsets = (
        ('📋 Βασικές Πληροφορίες', {
            'fields': (
                'code',
                'code_type',
                'name',
                'description',
                'is_active',
                'created_by'
            )
        }),
        ('💰 Έκπτωση', {
            'fields': (
                'discount_percentage',
                'discount_amount',
                'max_discount'
            ),
            'description': 'Χρησιμοποιήστε είτε ποσοστό έκπτωσης είτε σταθερό ποσό. Αν και τα δύο είναι 0, δεν θα εφαρμοστεί έκπτωση.'
        }),
        ('📊 Όρια Χρήσης', {
            'fields': (
                'max_uses',
                'current_uses'
            )
        }),
        ('📅 Ισχύς', {
            'fields': (
                'valid_from',
                'valid_until'
            ),
            'description': 'Αφήστε κενό για να μην υπάρχει περιορισμός ημερομηνίας.'
        }),
        ('📅 Χρονοσήματα', {
            'fields': (
                'created_at',
                'updated_at'
            ),
            'classes': ('collapse',)
        })
    )
    
    def code_type_display(self, obj):
        """Display code type with emoji"""
        types = {
            'ambassador': '👤 Πρέσβης',
            'partner': '🤝 Συνεργάτης'
        }
        return types.get(obj.code_type, obj.code_type)
    code_type_display.short_description = 'Τύπος'
    
    def discount_display(self, obj):
        """Display discount information"""
        if obj.discount_percentage > 0:
            max_info = f" (μέγιστο: {obj.max_discount}€)" if obj.max_discount else ""
            return f"{obj.discount_percentage}%{max_info}"
        elif obj.discount_amount > 0:
            return f"{obj.discount_amount}€"
        return "Χωρίς έκπτωση"
    discount_display.short_description = 'Έκπτωση'
    
    def usage_display(self, obj):
        """Display usage information"""
        if obj.max_uses:
            return f"{obj.current_uses} / {obj.max_uses}"
        return f"{obj.current_uses} (απεριόριστα)"
    usage_display.short_description = 'Χρήσεις'
    
    def validity_display(self, obj):
        """Display validity period"""
        from django.utils import timezone
        now = timezone.now()
        
        if obj.valid_from and obj.valid_until:
            if obj.valid_from <= now <= obj.valid_until:
                return format_html('<span style="color: #28a745;">✓ Ενεργό</span>')
            elif now < obj.valid_from:
                return format_html('<span style="color: #ffc107;">⏳ Επόμενο</span>')
            else:
                return format_html('<span style="color: #dc3545;">✗ Έληξε</span>')
        elif obj.valid_from:
            if now >= obj.valid_from:
                return format_html('<span style="color: #28a745;">✓ Ενεργό</span>')
            else:
                return format_html('<span style="color: #ffc107;">⏳ Επόμενο</span>')
        elif obj.valid_until:
            if now <= obj.valid_until:
                return format_html('<span style="color: #28a745;">✓ Ενεργό</span>')
            else:
                return format_html('<span style="color: #dc3545;">✗ Έληξε</span>')
        else:
            return format_html('<span style="color: #28a745;">✓ Ενεργό</span>')
    validity_display.short_description = 'Ισχύς'