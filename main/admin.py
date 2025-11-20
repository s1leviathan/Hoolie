from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import InsuranceApplication, PaymentTransaction, PaymentPlan, AmbassadorCode, PetDocument, PetPhoto, Questionnaire

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
        'questionnaire_link',
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
        'contract_end_date',
        'application_number',
        'contract_pdf_link',
        'documents_list',
        'photos_list',
        'questionnaire_link'
    ]
    
    fieldsets = (
        ('📋 Διοικητικά Στοιχεία', {
            'fields': (
                'application_number',
                'contract_number',
                'receipt_number',
                'payment_code',
                'status',
                'contract_generated',
                'contract_pdf_link',
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
                'health_conditions',
                'documents_list',
                'photos_list'
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
        }),
        ('📋 Ερωτηματολόγιο', {
            'fields': (
                'questionnaire_link',
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
    
    def contract_pdf_link(self, obj):
        """Display link to view/download contract PDF from S3"""
        if obj.contract_pdf_path:
            from django.core.files.storage import default_storage
            try:
                if default_storage.exists(obj.contract_pdf_path):
                    view_url = reverse('admin:view_contract', args=[obj.pk])
                    return format_html(
                        '<a href="{}" target="_blank" style="background: #007bff; color: white; padding: 5px 10px; text-decoration: none; border-radius: 3px;">📄 Προβολή PDF</a><br>'
                        '<small style="color: #6c757d;">Path: {}</small>',
                        view_url,
                        obj.contract_pdf_path
                    )
                else:
                    return format_html(
                        '<span style="color: #dc3545;">⚠️ PDF not found in storage</span><br>'
                        '<small style="color: #6c757d;">Path: {}</small>',
                        obj.contract_pdf_path
                    )
            except Exception as e:
                return format_html(
                    '<span style="color: #dc3545;">⚠️ Error: {}</span>',
                    str(e)
                )
        return format_html('<span style="color: #6c757d;">-</span>')
    contract_pdf_link.short_description = 'Συμβόλαιο PDF'
    
    def documents_list(self, obj):
        """Display list of uploaded documents with download links"""
        documents = obj.documents.all()
        if documents:
            links_html = []
            for doc in documents:
                url = doc.get_file_url()
                if url:
                    links_html.append(
                        f'<a href="{url}" target="_blank" style="display: inline-block; margin: 2px; padding: 3px 8px; background: #28a745; color: white; text-decoration: none; border-radius: 3px; font-size: 12px;">📎 {doc.original_filename}</a>'
                    )
                else:
                    links_html.append(
                        f'<span style="color: #dc3545; font-size: 12px;">⚠️ {doc.original_filename}</span>'
                    )
            return format_html('<div>{}</div>', mark_safe(' '.join(links_html)))
        return format_html('<span style="color: #6c757d;">Δεν υπάρχουν ανεβασμένα έγγραφα</span>')
    documents_list.short_description = 'Ανεβασμένα Έγγραφα'
    
    def photos_list(self, obj):
        """Display grid of uploaded photos with view links"""
        photos = obj.photos.all()
        if photos:
            photos_html = []
            for photo in photos:
                url = photo.get_file_url()
                if url:
                    photos_html.append(
                        f'<div style="display: inline-block; margin: 5px; text-align: center;">'
                        f'<a href="{url}" target="_blank" style="display: block;">'
                        f'<img src="{url}" alt="{photo.original_filename}" style="width: 100px; height: 100px; object-fit: cover; border-radius: 5px; border: 2px solid #28a745;">'
                        f'</a>'
                        f'<small style="display: block; margin-top: 3px; color: #666;">{photo.original_filename}</small>'
                        f'</div>'
                    )
                else:
                    photos_html.append(
                        f'<div style="display: inline-block; margin: 5px; text-align: center;">'
                        f'<span style="color: #dc3545; font-size: 12px;">⚠️ {photo.original_filename}</span>'
                        f'</div>'
                    )
            return format_html('<div style="display: flex; flex-wrap: wrap;">{}</div>', mark_safe(''.join(photos_html)))
        return format_html('<span style="color: #6c757d;">Δεν υπάρχουν ανεβασμένες φωτογραφίες</span>')
    photos_list.short_description = 'Ανεβασμένες Φωτογραφίες'
    
    def questionnaire_link(self, obj):
        """Display link to questionnaire with ID"""
        try:
            if hasattr(obj, 'questionnaire') and obj.questionnaire:
                questionnaire = obj.questionnaire
                url = reverse('admin:main_questionnaire_change', args=[questionnaire.pk])
                return format_html(
                    '<a href="{}" target="_blank" style="font-weight: bold; color: #007bff;">📋 Ερωτηματολόγιο (ID: {})</a>',
                    url, questionnaire.id
                )
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error getting questionnaire for application {obj.id}: {e}")
        return format_html('<span style="color: #dc3545; font-weight: bold;">⚠️ Δεν υπάρχει ερωτηματολόγιο</span>')
    questionnaire_link.short_description = 'Ερωτηματολόγιο'
    
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
        """View generated contract(s) from S3 or local storage"""
        from django.http import FileResponse, Http404, HttpResponse
        from django.core.files.storage import default_storage
        import zipfile
        from io import BytesIO
        
        try:
            application = InsuranceApplication.objects.get(pk=application_id)
            
            if not application.contract_pdf_path:
                raise Http404("Το συμβόλαιο δεν βρέθηκε")
            
            # Check if file exists in storage (S3 or local)
            if not default_storage.exists(application.contract_pdf_path):
                raise Http404("Το συμβόλαιο δεν βρέθηκε")
            
            # Check if there are multiple contracts (two pets)
            if application.has_second_pet and application.second_pet_name:
                # Look for both pet contracts in storage
                contract_files = []
                contract_number = application.contract_number
                
                # List files in contracts directory
                try:
                    # Get all files in contracts/ directory
                    contracts_dir = 'contracts/'
                    files = default_storage.listdir(contracts_dir)[1]  # Get files list
                    
                    for filename in files:
                        if (filename.startswith(f'contract_{contract_number}_pet') and 
                            filename.endswith('.pdf')):
                            file_path = f'{contracts_dir}{filename}'
                            if default_storage.exists(file_path):
                                contract_files.append((filename, file_path))
                except:
                    pass
                
                if len(contract_files) > 1:
                    # Create ZIP file with both contracts
                    zip_buffer = BytesIO()
                    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
                        for filename, file_path in contract_files:
                            with default_storage.open(file_path, 'rb') as pdf_file:
                                zip_file.writestr(filename, pdf_file.read())
                    
                    zip_buffer.seek(0)
                    response = HttpResponse(zip_buffer.read(), content_type='application/zip')
                    response['Content-Disposition'] = f'attachment; filename="{application.contract_number}_contracts.zip"'
                    return response
            
            # Single contract
            pdf_file = default_storage.open(application.contract_pdf_path, 'rb')
            return FileResponse(
                pdf_file,
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


@admin.register(PetDocument)
class PetDocumentAdmin(admin.ModelAdmin):
    """Admin interface for Pet Documents"""
    
    list_display = [
        'original_filename',
        'pet_name',
        'pet_type_display',
        'application_link',
        'file_size_display',
        'file_type',
        'uploaded_at',
        'file_download'
    ]
    
    list_filter = [
        'pet_type',
        'file_type',
        'uploaded_at',
        'application'
    ]
    
    search_fields = [
        'original_filename',
        'pet_name',
        'application__contract_number',
        'application__full_name',
        'application__email'
    ]
    
    readonly_fields = [
        'uploaded_at',
        'created_at',
        'updated_at',
        'file_size',
        'file_type',
        'original_filename'
    ]
    
    fieldsets = (
        ('📄 Αρχείο', {
            'fields': (
                'file',
                'original_filename',
                'file_size',
                'file_type'
            )
        }),
        ('🐾 Στοιχεία Κατοικιδίου', {
            'fields': (
                'pet_name',
                'pet_type'
            )
        }),
        ('📋 Σύνδεση με Αίτηση', {
            'fields': (
                'application',
            )
        }),
        ('📅 Χρονοσήματα', {
            'fields': (
                'uploaded_at',
                'created_at',
                'updated_at'
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
        return obj.pet_type or '-'
    pet_type_display.short_description = 'Είδος'
    
    def application_link(self, obj):
        """Link to the related application"""
        if obj.application:
            url = reverse('admin:main_insuranceapplication_change', args=[obj.application.pk])
            return format_html('<a href="{}">{}</a>', url, obj.application.contract_number or obj.application.application_number)
        return '-'
    application_link.short_description = 'Αίτηση'
    
    def file_size_display(self, obj):
        """Display file size in human-readable format"""
        if obj.file_size:
            if obj.file_size < 1024:
                return f"{obj.file_size} B"
            elif obj.file_size < 1024 * 1024:
                return f"{obj.file_size / 1024:.2f} KB"
            else:
                return f"{obj.file_size / (1024 * 1024):.2f} MB"
        return '-'
    file_size_display.short_description = 'Μέγεθος'
    
    def file_download(self, obj):
        """Link to download/view file"""
        if obj.file:
            url = obj.get_file_url()
            if url:
                return format_html('<a href="{}" target="_blank">📥 Προβολή/Λήψη</a>', url)
        return '-'
    file_download.short_description = 'Αρχείο'


@admin.register(PetPhoto)
class PetPhotoAdmin(admin.ModelAdmin):
    """Admin interface for Pet Photos"""
    
    list_display = [
        'photo_thumbnail',
        'original_filename',
        'pet_name',
        'pet_type_display',
        'application_link',
        'file_size_display',
        'file_type',
        'uploaded_at',
        'photo_view'
    ]
    
    list_filter = [
        'pet_type',
        'file_type',
        'uploaded_at',
        'application'
    ]
    
    search_fields = [
        'original_filename',
        'pet_name',
        'application__contract_number',
        'application__full_name',
        'application__email'
    ]
    
    readonly_fields = [
        'uploaded_at',
        'created_at',
        'updated_at',
        'file_size',
        'file_type',
        'original_filename'
    ]
    
    fieldsets = (
        ('📸 Φωτογραφία', {
            'fields': (
                'file',
                'original_filename',
                'file_size',
                'file_type'
            )
        }),
        ('🐾 Στοιχεία Κατοικιδίου', {
            'fields': (
                'pet_name',
                'pet_type'
            )
        }),
        ('📋 Σύνδεση με Αίτηση', {
            'fields': (
                'application',
            )
        }),
        ('📅 Χρονοσήματα', {
            'fields': (
                'uploaded_at',
                'created_at',
                'updated_at'
            ),
            'classes': ('collapse',)
        })
    )
    
    def photo_thumbnail(self, obj):
        """Display photo thumbnail"""
        if obj.file:
            url = obj.get_file_url()
            if url:
                return format_html(
                    '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 5px; border: 1px solid #ddd;">',
                    url
                )
        return '-'
    photo_thumbnail.short_description = 'Προεπισκόπηση'
    
    def pet_type_display(self, obj):
        """Display pet type with emoji"""
        if obj.pet_type == 'dog':
            return "🐕 Σκύλος"
        elif obj.pet_type == 'cat':
            return "🐱 Γάτα"
        return obj.pet_type or '-'
    pet_type_display.short_description = 'Είδος'
    
    def application_link(self, obj):
        """Link to the related application"""
        if obj.application:
            url = reverse('admin:main_insuranceapplication_change', args=[obj.application.pk])
            return format_html('<a href="{}">{}</a>', url, obj.application.contract_number or obj.application.application_number)
        return '-'
    application_link.short_description = 'Αίτηση'
    
    def file_size_display(self, obj):
        """Display file size in human-readable format"""
        if obj.file_size:
            if obj.file_size < 1024:
                return f"{obj.file_size} B"
            elif obj.file_size < 1024 * 1024:
                return f"{obj.file_size / 1024:.2f} KB"
            else:
                return f"{obj.file_size / (1024 * 1024):.2f} MB"
        return '-'
    file_size_display.short_description = 'Μέγεθος'
    
    def photo_view(self, obj):
        """Link to view photo"""
        if obj.file:
            url = obj.get_file_url()
            if url:
                return format_html('<a href="{}" target="_blank">📷 Προβολή</a>', url)
        return '-'
    photo_view.short_description = 'Φωτογραφία'


@admin.register(Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):
    """Admin interface for Questionnaires"""
    
    list_display = [
        'application_link',
        'program_display',
        'breed_surcharge_display',
        'payment_method_display',
        'payment_frequency_display',
        'desired_start_date',
        'created_at'
    ]
    
    list_filter = [
        'program',
        'payment_method',
        'payment_frequency',
        'created_at',
        'is_healthy',
        'has_hereditary_disease'
    ]
    
    search_fields = [
        'application__application_number',
        'application__contract_number',
        'application__full_name',
        'application__email',
        'application__pet_name'
    ]
    
    readonly_fields = [
        'created_at',
        'updated_at'
    ]
    
    fieldsets = (
        ('📋 Σύνδεση με Αίτηση', {
            'fields': (
                'application',
            )
        }),
        ('1.1 Ερωτηματολόγιο Συμβαλλόμενου', {
            'fields': (
                'has_other_insured_pet',
                'has_been_denied_insurance',
                'has_special_terms_imposed',
            )
        }),
        ('2. Στοιχεία Κατοικίδιου', {
            'fields': (
                'pet_colors',
                'pet_weight',
                'is_purebred',
                'is_mixed',
                'is_crossbreed',
                'special_breed_5_percent',
                'special_breed_20_percent',
            )
        }),
        ('2.2 Ερωτηματολόγιο Κατοικίδιου', {
            'fields': (
                'is_healthy',
                'is_healthy_details',
                'has_injury_illness_3_years',
                'has_injury_illness_details',
                'has_surgical_procedure',
                'has_surgical_procedure_details',
                'has_examination_findings',
                'has_examination_findings_details',
                'is_sterilized',
                'is_vaccinated_leishmaniasis',
                'follows_vaccination_program',
                'follows_vaccination_program_details',
                'has_hereditary_disease',
                'has_hereditary_disease_details',
            )
        }),
        ('3. Επιλογή Προγράμματος', {
            'fields': (
                'program',
                'additional_poisoning_coverage',
                'additional_blood_checkup',
            )
        }),
        ('4. Επιθυμητή Έναρξη', {
            'fields': (
                'desired_start_date',
            )
        }),
        ('5. Τρόπος Πληρωμής', {
            'fields': (
                'payment_method',
                'payment_frequency',
            )
        }),
        ('6. Δηλώσεις – Εξουσιοδοτήσεις – Συγκαταθέσεις', {
            'fields': (
                'consent_terms_conditions',
                'consent_info_document',
                'consent_email_notifications',
                'consent_marketing',
                'consent_data_processing',
                'consent_pet_gov_platform',
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
    
    def application_link(self, obj):
        """Link to the related application"""
        if obj.application:
            url = reverse('admin:main_insuranceapplication_change', args=[obj.application.pk])
            return format_html('<a href="{}">{}</a>', url, obj.application.application_number or obj.application.contract_number)
        return '-'
    application_link.short_description = 'Αίτηση'
    
    def program_display(self, obj):
        """Display program"""
        programs = {
            'silver': 'Silver',
            'gold': 'Gold',
            'platinum': 'Platinum',
            'dynasty': 'Dynasty'
        }
        return programs.get(obj.program, obj.program or '-')
    program_display.short_description = 'Πρόγραμμα'
    
    def payment_method_display(self, obj):
        """Display payment method"""
        methods = {
            'card': 'Κάρτα',
            'bank_deposit': 'Τραπεζική Κατάθεση',
            'cash': 'Μετρητά'
        }
        return methods.get(obj.payment_method, obj.payment_method or '-')
    payment_method_display.short_description = 'Τρόπος Πληρωμής'
    
    def payment_frequency_display(self, obj):
        """Display payment frequency"""
        frequencies = {
            'annual': 'Ετήσια',
            'six_month': 'Εξάμηνη',
            'three_month': 'Τριμηνιαία'
        }
        return frequencies.get(obj.payment_frequency, obj.payment_frequency or '-')
    payment_frequency_display.short_description = 'Συχνότητα'
    
    def breed_surcharge_display(self, obj):
        """Display breed surcharges"""
        surcharges = []
        if obj.special_breed_5_percent:
            surcharges.append('5%')
        if obj.special_breed_20_percent:
            surcharges.append('20%')
        if surcharges:
            return format_html('<span style="color: #dc3545; font-weight: bold;">{}</span>', ' + '.join(surcharges))
        return format_html('<span style="color: #6c757d;">-</span>')
    breed_surcharge_display.short_description = 'Επασφάλιστρο Ράτσας'
    
    def has_add_permission(self, request):
        """Disable manual addition - questionnaires are created through the application flow"""
        return False