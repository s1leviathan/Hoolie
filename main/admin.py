from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import InsuranceApplication, PaymentTransaction, PaymentPlan, AmbassadorCode, PetDocument, PetPhoto, Questionnaire
from django.contrib import messages
from django.utils import timezone
from django.contrib import messages
from django.urls import path, reverse
from django.shortcuts import redirect
from django.utils.html import format_html
import logging
from .utils import get_poisoning_price
logger = logging.getLogger(__name__)



@admin.register(InsuranceApplication)
class InsuranceApplicationAdmin(admin.ModelAdmin):
    """Admin interface for Insurance Applications"""
    actions = ["export_today_contracts"]
    
    list_display = [
        'contract_number', 
        'full_name', 
        'assigned_admin_display',
        'pet_name', 
        'pet_type_display',
        'program_display', 
        'status_display',
        'premium_display',
        'affiliate_code_display',
        'questionnaire_link',
        'created_at',
        'contract_actions',
        'final_approval_buttons',
    ]
    
    list_filter = [
        'status',
        'assigned_to',
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
    
    # readonly_fields = [
    #     'contract_number',
    #     'created_at',
    #     'updated_at',
    #     'contract_start_date',
    #     'contract_end_date',
    #     'application_number',
    #     'contract_pdf_link',
    #     'documents_list',
    #     'photos_list',
    #     'questionnaire_link'
    # ]
    
    fieldsets = (
        ('👤 Ανάθεση & Τελικές Ενέργειες', {
            'fields': (
                'assigned_to',
                'final_approval_buttons',
            ),
            'classes': ('wide',),
            'description': '👤 Ορίστε ποιος διαχειριστής εργάζεται σε αυτή την αίτηση. Χρησιμοποιήστε τα παρακάτω κουμπιά για τελική έγκριση ή απόρριψη.'
        }),
        ('📋 Διοικητικά Στοιχεία', {
            'fields': (
                'application_number',
                'contract_number',
                ('receipt_number', 'payment_code'),
                'status',
                'contract_generated',
                'contract_pdf_link',
                'contract_pdf_path',
                ('section_admin_approved', 'section_admin_rejected'),
            ),
            'description': '💡 Σημείωση: Οι κωδικοί πληρωμής και απόδειξης μπορούν να προστεθούν χειροκίνητα αργότερα.'
        }),
        ('📅 Ημερομηνίες', {
            'fields': (
                'created_at',
                'updated_at',
                'contract_start_date',
                'contract_end_date',
                ('section_dates_approved', 'section_dates_rejected'),
            )
        }),
        ('👤 Στοιχεία Πελάτη', {
            'fields': (
                'full_name',
                'afm',
                'phone',
                'email',
                'address',
                'postal_code',
                ('section_customer_approved', 'section_customer_rejected'),
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
                'photos_list',
                ('section_pet1_approved', 'section_pet1_rejected'),
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
                'second_pet_health_conditions',
                ('section_pet2_approved', 'section_pet2_rejected'),
            ),
            'classes': ('collapse',)
        }),
        ('🛡️ Στοιχεία Ασφάλισης', {
            'fields': (
                'program',
                'annual_premium',
                'six_month_premium',
                'three_month_premium',
                ('section_insurance_approved', 'section_insurance_rejected'),
            )
        }),
        ('🎁 Κωδικός Συνεργάτη', {
            'fields': (
                'affiliate_code',
                'discount_applied',
                ('section_affiliate_approved', 'section_affiliate_rejected'),
            ),
            'classes': ('collapse',)
        }),
        ('📋 Ερωτηματολόγιο', {
            'fields': (
                'questionnaire_link',
                ('section_questionnaire_approved', 'section_questionnaire_rejected'),
            ),
            'classes': ('collapse',)
        })
    )


    readonly_fields = [
        'contract_number',
        'created_at',
        'updated_at',
        'contract_start_date',
        'contract_end_date',
        'application_number',
        'contract_pdf_link',
        'documents_list',
        'photos_list',
        'questionnaire_link',
        'final_approval_buttons',

        # 🔒 LOCK PRICES
        'annual_premium',
        'six_month_premium',
        'three_month_premium',
    ]

    
    def pet_type_display(self, obj):
        """Display pet type with emoji"""
        try:
            if not obj:
                return '-'
            if obj.pet_type == 'dog':
                return "🐕 Σκύλος"
            elif obj.pet_type == 'cat':
                return "🐱 Γάτα"
            return obj.pet_type or '-'
        except Exception:
            return '-'
    pet_type_display.short_description = 'Είδος'
    
    def program_display(self, obj):
        """Display program with color coding"""
        try:
            if not obj:
                return '-'
            colors = {
                'silver': '#C0C0C0',
                'gold': '#FFD700', 
                'platinum': '#E5E4E2'
            }
            color = colors.get(obj.program, '#000')
            # Use the new combined method that includes payment frequency
            name = obj.get_program_with_frequency_display()
            return format_html(
                '<span style="color: {}; font-weight: bold;">🏆 {}</span>',
                color, name
            )
        except Exception:
            return '-'
    program_display.short_description = 'Πρόγραμμα & Συχνότητα'
    
    def premium_display(self, obj):
        """Display premium amount based on selected payment frequency"""
        try:
            if not obj:
                return '-'
            
            premium = obj.get_premium_for_frequency()
            frequency = obj.get_payment_frequency_display_greek()
            
            if frequency:
                return format_html(
                    '<span style="font-weight: bold;">{:.2f}€</span><br><small style="color: #666;">{}</small>',
                    premium,
                    frequency
                )
            else:
                # Fallback to annual
                annual = float(obj.annual_premium) if obj.annual_premium else 0
                return format_html('<span style="font-weight: bold;">{:.2f}€</span>', annual)
        except Exception:
            return '-'
    premium_display.short_description = 'Ασφάλιστρο'
    
    def status_display(self, obj):
        """Display status with color coding"""
        try:
            if not obj:
                return '-'
            colors = {
                'draft': '#6c757d',
                'submitted': '#007bff',
                'approved': '#28a745',
                'rejected': '#dc3545',
                'active': '#17a2b8',
                'expired': '#6f42c1'
            }
            color = colors.get(obj.status, '#000')
            status_text = obj.get_status_display() if hasattr(obj, 'get_status_display') else (obj.status or '-')
            return format_html(
                '<span style="color: {}; font-weight: bold;">●</span> {}',
                color, status_text
            )
        except Exception:
            return '-'
    status_display.short_description = 'Κατάσταση'

   
    
    def affiliate_code_display(self, obj):
        """Display affiliate code with ambassador/partner name and discount if applied"""
        try:
            if not obj or not obj.affiliate_code:
                return '-'
            # Try to get the AmbassadorCode object to show the name
            try:
                ambassador_code = AmbassadorCode.objects.get(code=obj.affiliate_code)
                code_name = ambassador_code.name
                code_type = ambassador_code.get_code_type_display()
            except AmbassadorCode.DoesNotExist:
                code_name = None
                code_type = None
            
            # Build display string
            if code_name:
                display_text = f'🎁 {obj.affiliate_code}<br><small style="color: #6c757d;">{code_name} ({code_type})</small>'
            else:
                display_text = f'🎁 {obj.affiliate_code}'
            
            # Add discount if applied
            if hasattr(obj, 'discount_applied') and obj.discount_applied > 0:
                display_text += f'<br><small style="color: #28a745; font-weight: bold;">Έκπτωση: -{obj.discount_applied}€</small>'
            
            return format_html(display_text)
        except Exception as e:
            
            logger.error(f"Error in affiliate_code_display: {e}")
            return '-'
    affiliate_code_display.short_description = 'Κωδικός Συνεργάτη'
    
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
            from django.core.files.storage import default_storage
            links_html = []
            for doc in documents:
                if doc.file:
                    try:
                        # Check if file exists in storage
                        if default_storage.exists(doc.file.name):
                            url = doc.get_file_url()
                            if url:
                                links_html.append(
                                    f'<a href="{url}" target="_blank" style="display: inline-block; margin: 2px; padding: 3px 8px; background: #28a745; color: white; text-decoration: none; border-radius: 3px; font-size: 12px;">📎 {doc.original_filename}</a>'
                                )
                            else:
                                links_html.append(
                                    f'<span style="color: #dc3545; font-size: 12px;">⚠️ {doc.original_filename}</span>'
                                )
                        else:
                            # File doesn't exist in storage
                            links_html.append(
                                f'<span style="color: #dc3545; font-size: 12px;">⚠️ {doc.original_filename} <small>(Αρχείο λείπει)</small></span>'
                            )
                    except Exception:
                        links_html.append(
                            f'<span style="color: #dc3545; font-size: 12px;">⚠️ {doc.original_filename}</span>'
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
            from django.core.files.storage import default_storage
            photos_html = []
            for photo in photos:
                if photo.file:
                    try:
                        # Check if file exists in storage
                        if default_storage.exists(photo.file.name):
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
                        else:
                            # File doesn't exist in storage
                            photos_html.append(
                                f'<div style="display: inline-block; margin: 5px; text-align: center;">'
                                f'<span style="color: #dc3545; font-size: 12px;">⚠️ {photo.original_filename}</span><br>'
                                f'<small style="color: #6c757d; font-size: 10px;">Αρχείο λείπει</small>'
                                f'</div>'
                            )
                    except Exception:
                        photos_html.append(
                            f'<div style="display: inline-block; margin: 5px; text-align: center;">'
                            f'<span style="color: #dc3545; font-size: 12px;">⚠️ {photo.original_filename}</span>'
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
        """Display link to questionnaire with ID and status"""
        try:
            if hasattr(obj, 'questionnaire') and obj.questionnaire:
                questionnaire = obj.questionnaire
                url = reverse('admin:main_questionnaire_change', args=[questionnaire.pk])
                # Check if questionnaire has any data
                has_data = (
                    questionnaire.is_healthy is not None or
                    questionnaire.program or
                    questionnaire.payment_frequency or
                    questionnaire.has_other_insured_pet or
                    questionnaire.has_been_denied_insurance
                )
                status_icon = '✅' if has_data else '⚠️'
                status_text = 'Συμπληρωμένο' if has_data else 'Ατελές'
                return format_html(
                    '<a href="{}" target="_blank" style="font-weight: bold; color: #007bff; text-decoration: none;">{} 📋 Ερωτηματολόγιο (ID: {})</a><br><small style="color: #6c757d;">{}</small>',
                    url, status_icon, questionnaire.id, status_text
                )
            else:
                # Try to find questionnaire by application
                from .models import Questionnaire
                try:
                    questionnaire = Questionnaire.objects.get(application=obj)
                    url = reverse('admin:main_questionnaire_change', args=[questionnaire.pk])
                    return format_html(
                        '<a href="{}" target="_blank" style="font-weight: bold; color: #007bff; text-decoration: none;">📋 Ερωτηματολόγιο (ID: {})</a>',
                        url, questionnaire.id
                    )
                except Questionnaire.DoesNotExist:
                    pass
        except Exception as e:
         
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

    def export_today_contracts(self, request, queryset):
        from django.core.management import call_command
        from django.contrib import messages

        try:
            call_command("export_daily_contracts")
            messages.success(
                request,
                "Το αρχείο με τα σημερινά συμβόλαια εξήχθη στο /media/exports/contracts/"
            )
        except Exception as e:
            messages.error(request, f"Σφάλμα κατά την εξαγωγή: {str(e)}")

    export_today_contracts.short_description = "Εξαγωγή σημερινών συμβολαίων"


    def approve_button(self, obj):
        if obj.status != 'approved':
            url = reverse('admin:main_insuranceapplication_approve', args=[obj.pk])
            return format_html(
                '<a href="{}" class="button" '
                'style="background:#28a745;color:white;padding:5px 10px;'
                'text-decoration:none;border-radius:3px;">✔ Έγκριση</a>',
                url
            )
        return format_html('<span style="color:#28a745;font-weight:bold;">✔ Εγκεκριμένο</span>')

    approve_button.short_description = "Έγκριση"
    approve_button.allow_tags = True
    
    def assigned_admin_display(self, obj):
        """Display assigned admin prominently"""
        try:
            if obj and obj.assigned_to:
                name = obj.assigned_to.get_full_name() or obj.assigned_to.username or 'Unknown'
                return format_html(
                    '<span style="background: #007bff; color: white; padding: 4px 8px; border-radius: 3px; font-weight: bold;">👤 {}</span>',
                    name
                )
        except Exception:
            pass
        return format_html('<span style="color: #6c757d;">Δεν έχει ανατεθεί</span>')
    assigned_admin_display.short_description = 'Ανατεθειμένος Διαχειριστής'
    
    def final_approval_buttons(self, obj):
        """Display final approval/rejection buttons"""
        try:
            if not obj or not hasattr(obj, 'pk') or not obj.pk:
                return '-'
            
            approve_url = reverse('admin:main_insuranceapplication_final_approve', args=[obj.pk])
            reject_url = reverse('admin:main_insuranceapplication_final_reject', args=[obj.pk])
            
            buttons = []
            status = getattr(obj, 'status', None) or 'submitted'
            
            if status != 'approved':
                buttons.append(
                    format_html(
                        '<a href="{}" class="button" '
                        'style="background:#28a745;color:white;padding:10px 20px;'
                        'text-decoration:none;border-radius:5px;font-weight:bold;font-size:14px;'
                        'margin-right:10px;display:inline-block;">'
                        '✔ Τελική Έγκριση</a>',
                        approve_url
                    )
                )
            
            if status != 'rejected':
                buttons.append(
                    format_html(
                        '<a href="{}" class="button" '
                        'style="background:#dc3545;color:white;padding:10px 20px;'
                        'text-decoration:none;border-radius:5px;font-weight:bold;font-size:14px;'
                        'display:inline-block;">'
                        '✗ Τελική Απόρριψη</a>',
                        reject_url
                    )
                )
            
            if status == 'approved':
                buttons.append(
                    format_html(
                        '<span style="background:#28a745;color:white;padding:10px 20px;'
                        'border-radius:5px;font-weight:bold;font-size:14px;display:inline-block;">'
                        '✅ Εγκρίθηκε</span>'
                    )
                )
            elif status == 'rejected':
                buttons.append(
                    format_html(
                        '<span style="background:#dc3545;color:white;padding:10px 20px;'
                        'border-radius:5px;font-weight:bold;font-size:14px;display:inline-block;">'
                        '❌ Απορρίφθηκε</span>'
                    )
                )
            
            return format_html(''.join(buttons)) if buttons else '-'
        except Exception as e:
            logger.error(f"Error in final_approval_buttons: {e}")
            return format_html('<span style="color: #dc3545;">Error</span>')
    final_approval_buttons.short_description = 'Τελικές Ενέργειες'
    final_approval_buttons.allow_tags = True

    def get_urls(self):
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
            path(
                '<int:application_id>/approve/',
                self.admin_site.admin_view(self.approve_single_application),
                name='main_insuranceapplication_approve'
            ),
            path(
                '<int:application_id>/final-approve/',
                self.admin_site.admin_view(self.final_approve_application),
                name='main_insuranceapplication_final_approve'
            ),
            path(
                '<int:application_id>/final-reject/',
                self.admin_site.admin_view(self.final_reject_application),
                name='main_insuranceapplication_final_reject'
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
    
    def approve_single_application(self, request, application_id):
            try:
                application = InsuranceApplication.objects.get(pk=application_id)
                application.status = 'approved'
                application.approved_at = timezone.now()
                application.save(update_fields=['status', 'approved_at'])
                messages.success(request, "Η αίτηση εγκρίθηκε επιτυχώς.")
            except InsuranceApplication.DoesNotExist:
                messages.error(request, "Η αίτηση δεν βρέθηκε.")
            
            return redirect('admin:main_insuranceapplication_changelist')
    
    def final_approve_application(self, request, application_id):
        """Final approval action"""
        try:
            application = InsuranceApplication.objects.get(pk=application_id)
            application.status = 'approved'
            application.approved_at = timezone.now()
            application.save(update_fields=['status', 'approved_at'])
            messages.success(request, "✅ Η αίτηση εγκρίθηκε τελικά.")
        except InsuranceApplication.DoesNotExist:
            messages.error(request, "Η αίτηση δεν βρέθηκε.")
        except Exception as e:
            logger.error(f"Error in final_approve_application: {e}")
            messages.error(request, f"Σφάλμα κατά την έγκριση: {str(e)}")
        
        return redirect('admin:main_insuranceapplication_change', application_id)
    
    def final_reject_application(self, request, application_id):
        """Final rejection action"""
        try:
            application = InsuranceApplication.objects.get(pk=application_id)
            application.status = 'rejected'
            application.save(update_fields=['status'])
            messages.success(request, "❌ Η αίτηση απορρίφθηκε τελικά.")
        except InsuranceApplication.DoesNotExist:
            messages.error(request, "Η αίτηση δεν βρέθηκε.")
        except Exception as e:
            logger.error(f"Error in final_reject_application: {e}")
            messages.error(request, f"Σφάλμα κατά την απόρριψη: {str(e)}")
        
        return redirect('admin:main_insuranceapplication_change', application_id)

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
    
    def save_model(self, request, obj, form, change):
        try:
            # Auto-assign to current admin if not already assigned
            if obj and hasattr(request, 'user') and request.user and request.user.is_authenticated:
                if not obj.assigned_to:
                    obj.assigned_to = request.user
        except Exception as e:
            logger.warning(f"Error auto-assigning admin: {e}")
        
        super().save_model(request, obj, form, change)

        # Sync program to questionnaire
        if hasattr(obj, "questionnaire") and obj.questionnaire:
            obj.questionnaire.program = obj.program
            obj.questionnaire.save(update_fields=["program"])

        from .utils import recalculate_application_premium
        recalculate_application_premium(obj)

        obj.refresh_from_db()

        

        try:
            obj.update_contract_dates_for_frequency()
        except Exception:
            pass




    
    def has_add_permission(self, request):
        return True


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
        return True


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
            from django.core.files.storage import default_storage
            try:
                # Check if file exists in storage
                if default_storage.exists(obj.file.name):
                    url = obj.get_file_url()
                    if url:
                        return format_html('<a href="{}" target="_blank">📥 Προβολή/Λήψη</a>', url)
                else:
                    return format_html(
                        '<span style="color: #dc3545;">⚠️ Αρχείο λείπει</span><br>'
                        '<small style="color: #6c757d;">{}</small>',
                        obj.file.name
                    )
            except Exception as e:
                return format_html(
                    '<span style="color: #dc3545;">⚠️ Σφάλμα: {}</span>',
                    str(e)
                )
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
            from django.core.files.storage import default_storage
            try:
                # Check if file exists in storage
                if default_storage.exists(obj.file.name):
                    url = obj.get_file_url()
                    if url:
                        return format_html(
                            '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 5px; border: 1px solid #ddd;">',
                            url
                        )
                else:
                    return format_html(
                        '<span style="color: #dc3545; font-size: 10px;">⚠️ Αρχείο λείπει</span>'
                    )
            except Exception:
                return format_html(
                    '<span style="color: #dc3545; font-size: 10px;">⚠️ Σφάλμα</span>'
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
            from django.core.files.storage import default_storage
            try:
                # Check if file exists in storage
                if default_storage.exists(obj.file.name):
                    url = obj.get_file_url()
                    if url:
                        return format_html('<a href="{}" target="_blank">📷 Προβολή</a>', url)
                else:
                    return format_html(
                        '<span style="color: #dc3545;">⚠️ Αρχείο λείπει</span><br>'
                        '<small style="color: #6c757d;">{}</small>',
                        obj.file.name
                    )
            except Exception as e:
                return format_html(
                    '<span style="color: #dc3545;">⚠️ Σφάλμα: {}</span>',
                    str(e)
                )
        return '-'
    photo_view.short_description = 'Φωτογραφία'


@admin.register(Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):
    """Admin interface for Questionnaires"""

    # Hide the 6th consent field
    exclude = ('consent_pet_gov_platform',)

    
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
        'id',  # Allow searching by questionnaire ID
    ]
    
    def get_search_results(self, request, queryset, search_term):
        """Custom search that handles application relationships safely"""
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        if search_term:
            # Also search in related application fields
            from django.db.models import Q
            application_filters = Q(
                application__application_number__icontains=search_term
            ) | Q(
                application__contract_number__icontains=search_term
            ) | Q(
                application__full_name__icontains=search_term
            ) | Q(
                application__email__icontains=search_term
            ) | Q(
                application__pet_name__icontains=search_term
            )
            queryset = queryset.filter(application_filters)
            use_distinct = True
        return queryset, use_distinct
    
    readonly_fields = [
        'created_at',
        'updated_at',
        # Application fields (read-only, displayed for reference)
        'application_contract_number',
        # 'application_receipt_number',  # Hidden - no active payment system
        # 'application_payment_code',     # Hidden - no active payment system
        'application_full_name',
        'price_breakdown_display',
        'application_phone',
        'application_email',
        'application_address',
        'application_postal_code',
        'application_afm',
        'application_annual_premium',
        'application_six_month_premium',
        'application_three_month_premium',
        'application_program',
        'application_pet_name',
        'application_pet_type',
        'application_pet_breed',
        'application_pet_birthdate',
        'application_microchip',
    ]
    
    fieldsets = (
        ('📋 Σύνδεση με Αίτηση', {
            'fields': (
                'application',
                'application_contract_number',
                # 'application_receipt_number',  # Hidden - no active payment system
                # 'application_payment_code',     # Hidden - no active payment system
            )
        }),
        ('👤 Στοιχεία Επικοινωνίας', {
            'fields': (
                'application_full_name',
                'application_afm',
                'application_phone',
                'application_email',
                'application_address',
                'application_postal_code',
            )
        }),
        ('🐾 Στοιχεία Κατοικίδιου (από Αίτηση)', {
            'fields': (
                'application_pet_name',
                'application_pet_type',
                'application_pet_breed',
                'application_pet_birthdate',
                'application_microchip',
            )
        }),
        ('💰 Τιμολόγηση (από Αίτηση)', {
            'fields': (
                'application_program',
                'application_annual_premium',
                'application_six_month_premium',
                'application_three_month_premium',
                'price_breakdown_display',
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
        try:
            if not obj:
                return '-'
            # Check if application exists and is not None
            if hasattr(obj, 'application') and obj.application:
                try:
                    url = reverse('admin:main_insuranceapplication_change', args=[obj.application.pk])
                    app_number = obj.application.application_number or obj.application.contract_number or f'ID: {obj.application.pk}'
                    return format_html('<a href="{}">{}</a>', url, app_number)
                except Exception as e:
                    
                    logger.error(f"Error creating application link: {e}")
                    return format_html('<span style="color: #dc3545;">Error: Application not found</span>')
        except Exception as e:
           
            logger.error(f"Error in application_link: {e}")
            return format_html('<span style="color: #dc3545;">Error</span>')
        return '-'
    application_link.short_description = 'Αίτηση'
    
    def program_display(self, obj):
        """Display program"""
        try:
            if not obj:
                return '-'
            programs = {
                'silver': 'Silver',
                'gold': 'Gold',
                'platinum': 'Platinum',
                'dynasty': 'Dynasty'
            }
            return programs.get(obj.program, obj.program or '-')
        except Exception as e:
            
            logger.error(f"Error in program_display: {e}")
            return '-'
    program_display.short_description = 'Πρόγραμμα'
    
    def payment_method_display(self, obj):
        """Display payment method"""
        try:
            if not obj:
                return '-'
            methods = {
                'card': 'Κάρτα',
                'bank_deposit': 'Τραπεζική Κατάθεση',
                'cash': 'Μετρητά'
            }
            return methods.get(obj.payment_method, obj.payment_method or '-')
        except Exception as e:
   
            logger.error(f"Error in payment_method_display: {e}")
            return '-'
    payment_method_display.short_description = 'Τρόπος Πληρωμής'
    
    def payment_frequency_display(self, obj):
        """Display payment frequency"""
        try:
            if not obj:
                return '-'
            frequencies = {
                'annual': 'Ετήσια',
                'six_month': 'Εξάμηνη',
                'three_month': 'Τριμηνιαία'
            }
            return frequencies.get(obj.payment_frequency, obj.payment_frequency or '-')
        except Exception as e:
       
            logger.error(f"Error in payment_frequency_display: {e}")
            return '-'
    payment_frequency_display.short_description = 'Συχνότητα'
    
    def breed_surcharge_display(self, obj):
        """Display breed surcharges"""
        try:
            if not obj:
                return '-'
            surcharges = []
            if obj.special_breed_5_percent:
                surcharges.append('5%')
            if obj.special_breed_20_percent:
                surcharges.append('20%')
            if surcharges:
                return format_html('<span style="color: #dc3545; font-weight: bold;">{}</span>', ' + '.join(surcharges))
            return format_html('<span style="color: #6c757d;">-</span>')
        except Exception as e:
 
            logger.error(f"Error in breed_surcharge_display: {e}")
            return format_html('<span style="color: #dc3545;">Error</span>')
    breed_surcharge_display.short_description = 'Επασφάλιστρο Ράτσας'
    
    # Application field display methods (read-only, from related InsuranceApplication)
    def application_contract_number(self, obj):
        """Display contract number from application"""
        try:
            if obj and obj.application:
                return obj.application.contract_number or '-'
        except:
            pass
        return '-'
    application_contract_number.short_description = 'Αριθμός Συμβολαίου'
    
    def application_receipt_number(self, obj):
        """Display receipt number from application"""
        try:
            if obj and obj.application:
                return obj.application.receipt_number or '-'
        except:
            pass
        return '-'
    application_receipt_number.short_description = 'Αριθμός Απόδειξης'
    
    def application_payment_code(self, obj):
        """Display payment code from application"""
        try:
            if obj and obj.application:
                return obj.application.payment_code or '-'
        except:
            pass
        return '-'
    application_payment_code.short_description = 'Κωδικός Πληρωμής'
    
    def application_full_name(self, obj):
        """Display full name from application"""
        try:
            if obj and obj.application:
                return obj.application.full_name or '-'
        except:
            pass
        return '-'
    application_full_name.short_description = 'Ονοματεπώνυμο'
    
    def application_phone(self, obj):
        """Display phone from application"""
        try:
            if obj and obj.application:
                return obj.application.phone or '-'
        except:
            pass
        return '-'
    application_phone.short_description = 'Τηλέφωνο'
    
    def application_email(self, obj):
        """Display email from application"""
        try:
            if obj and obj.application:
                return obj.application.email or '-'
        except:
            pass
        return '-'
    application_email.short_description = 'Email'
    
    def application_address(self, obj):
        """Display address from application"""
        try:
            if obj and obj.application:
                return obj.application.address or '-'
        except:
            pass
        return '-'
    application_address.short_description = 'Διεύθυνση'
    
    def application_postal_code(self, obj):
        """Display postal code from application"""
        try:
            if obj and obj.application:
                return obj.application.postal_code or '-'
        except:
            pass
        return '-'
    application_postal_code.short_description = 'Ταχυδρομικός Κώδικας'
    
    def application_afm(self, obj):
        """Display AFM from application"""
        try:
            if obj and obj.application:
                return obj.application.afm or '-'
        except:
            pass
        return '-'
    application_afm.short_description = 'Α.Φ.Μ.'
    
    def application_annual_premium(self, obj):
        """Display annual premium from application"""
        try:
            if obj and obj.application and obj.application.annual_premium:
                return f"{obj.application.annual_premium:.2f}€"
        except:
            pass
        return '-'
    application_annual_premium.short_description = 'Ετήσια Πληρωμή'
    
    def application_six_month_premium(self, obj):
        """Display six month premium from application"""
        try:
            if obj and obj.application and obj.application.six_month_premium:
                return f"{obj.application.six_month_premium:.2f}€"
        except:
            pass
        return '-'
    application_six_month_premium.short_description = 'Εξάμηνη Πληρωμή'
    
    def application_three_month_premium(self, obj):
        """Display three month premium from application"""
        try:
            if obj and obj.application and obj.application.three_month_premium:
                return f"{obj.application.three_month_premium:.2f}€"
        except:
            pass
        return '-'
    application_three_month_premium.short_description = 'Τριμηνιαία Πληρωμή'

    # ⚠️ WARNING:
    # This breakdown is for DISPLAY ONLY.
    # Final totals MUST always come from stored premiums.
    
    def price_breakdown_display(self, obj):
        """Display detailed price breakdown with add-ons and surcharges"""
        try:
            if not obj or not obj.application:
                return '-'
            
            app = obj.application
            questionnaire = obj
            
            # Get the base price from pricing table (without surcharges)
            # Use the same pricing table as fillpdf_utils.py
            pet_type = app.pet_type
            weight_category = app.pet_weight_category or ''
            program = app.program
            
            # EXACT pricing breakdown from the official table
            DOG_PRICING = {
                'silver': {
                    '10': {'final': 166.75},
                    '11-20': {'final': 207.20},
                    '21-40': {'final': 234.14},
                    '>40': {'final': 254.36}
                },
                'gold': {
                    '10': {'final': 234.14},
                    '11-20': {'final': 261.09},
                    '21-40': {'final': 288.05},
                    '>40': {'final': 308.26}
                },
                'platinum': {
                    '10': {'final': 368.92},
                    '11-20': {'final': 389.15},
                    '21-40': {'final': 409.36},
                    '>40': {'final': 436.32}
                }
            }
            
            CAT_PRICING = {
                'silver': {
                    '10': {'final': 113.81},
                    '11-20': {'final': 141.02}
                },
                'gold': {
                    '10': {'final': 168.22},
                    '11-20': {'final': 188.61}
                },
                'platinum': {
                    '10': {'final': 277.02},
                    '11-20': {'final': 311.02}
                }
            }
            
            # Map weight categories
            weight_mapping = {
                'up_10': '10',
                '10_25': '11-20', 
                '25_40': '21-40',
                'over_40': '>40'
            }
            
            # Get the correct pricing table
            pricing_table = DOG_PRICING if pet_type == 'dog' else CAT_PRICING
            mapped_weight = weight_mapping.get(weight_category, weight_category)
            
            # Get base price from table
            base_final_price = 0
            if program in pricing_table and mapped_weight in pricing_table[program]:
                base_final_price = pricing_table[program][mapped_weight]['final']
            
            if base_final_price == 0:
                # Fallback: reverse calculate from annual_premium
                # annual_premium already includes surcharges, so we need to reverse calculate
                stored_premium = float(app.annual_premium) if app.annual_premium else 0
                if stored_premium > 0:
                    # Estimate base by subtracting known add-ons
                    estimated_base = stored_premium
                    if questionnaire.additional_poisoning_coverage:
                        estimated_base -= get_poisoning_price(program, "annual")
                    if questionnaire.additional_blood_checkup:
                        estimated_base -= 28.00
                    # Reverse calculate breed surcharges (20% is applied after 5%, so reverse in reverse order)
                    if questionnaire.special_breed_20_percent:
                        estimated_base = estimated_base / 1.20
                    if questionnaire.special_breed_5_percent:
                        estimated_base = estimated_base / 1.05
                    base_final_price = estimated_base
            
            # Calculate breakdown - first calculate annual values
            total_annual = base_final_price
            
            # Breed surcharges (20% is applied on price AFTER 5% surcharge, not on base)
            surcharge_5_annual = 0
            surcharge_20_annual = 0
            if questionnaire.special_breed_5_percent:
                surcharge_5_annual = base_final_price * 0.05
                total_annual = total_annual * 1.05  # Apply 5% surcharge
            
            if questionnaire.special_breed_20_percent:
                # 20% is applied on the price after 5% surcharge (if applicable)
                surcharge_20_annual = total_annual * 0.20
                total_annual = total_annual * 1.20  # Apply 20% surcharge
            
            # Add-ons (annual values)
            annual_poisoning = 0
            annual_blood_checkup = 0
            
            if questionnaire.additional_poisoning_coverage:
                annual_poisoning = get_poisoning_price(program=program, payment_frequency="annual")
                total_annual += annual_poisoning
            
            if questionnaire.additional_blood_checkup:
                annual_blood_checkup = 28.00
                total_annual += annual_blood_checkup
            
            # Now apply payment frequency to get display values
            payment_freq = questionnaire.payment_frequency or "annual"
            
            if payment_freq == "six_month":
                # Scale base and surcharges with premium multiplier (52.5% of annual)
                premium_multiplier = 0.525
                # Scale add-ons with add-on multiplier (50% of annual)
                addon_multiplier = 0.5
                base_display = base_final_price * premium_multiplier
                surcharge_5_display = surcharge_5_annual * premium_multiplier
                surcharge_20_display = surcharge_20_annual * premium_multiplier
                poisoning_display = annual_poisoning * addon_multiplier
                blood_checkup_display = annual_blood_checkup * addon_multiplier
                frequency_label = "Εξάμηνη"
                total = float(app.six_month_premium or 0)
            elif payment_freq == "three_month":
                # Scale base and surcharges with premium multiplier (27.5% of annual)
                premium_multiplier = 0.275
                # Scale add-ons with add-on multiplier (25% of annual)
                addon_multiplier = 0.25
                base_display = base_final_price * premium_multiplier
                surcharge_5_display = surcharge_5_annual * premium_multiplier
                surcharge_20_display = surcharge_20_annual * premium_multiplier
                poisoning_display = annual_poisoning * addon_multiplier
                blood_checkup_display = annual_blood_checkup * addon_multiplier
                frequency_label = "Τριμηνιαία"
                total = float(app.three_month_premium or 0)
            else:
                # Annual - no scaling needed
                base_display = base_final_price
                surcharge_5_display = surcharge_5_annual
                surcharge_20_display = surcharge_20_annual
                poisoning_display = annual_poisoning
                blood_checkup_display = annual_blood_checkup
                frequency_label = "Ετήσια"
                total = float(app.annual_premium or 0)
            
            # Build breakdown with frequency-adjusted display values
            breakdown = [f"Βασική Τιμή: {base_display:.2f}€"]
            calculated_total = base_display
            
            if questionnaire.special_breed_5_percent:
                breakdown.append(f"+ Επασφάλιστρο 5%: {surcharge_5_display:.2f}€")
                calculated_total += surcharge_5_display
            if questionnaire.special_breed_20_percent:
                breakdown.append(f"+ Επασφάλιστρο 20%: {surcharge_20_display:.2f}€")
                calculated_total += surcharge_20_display
            if questionnaire.additional_poisoning_coverage:
                breakdown.append(f"+ Δηλητηρίαση: {poisoning_display:.2f}€")
                calculated_total += poisoning_display
            if questionnaire.additional_blood_checkup:
                breakdown.append(f"+ Αιματολογικό Check Up: {blood_checkup_display:.2f}€")
                calculated_total += blood_checkup_display
            
            # Round calculated total
            calculated_total = round(calculated_total, 2)

            # Check if stored premium matches calculated total
            stored_premium = total
            if abs(stored_premium - calculated_total) > 0.01 and stored_premium > 0:
                # Stored premium is outdated - automatically recalculate and update
                from .utils import recalculate_application_premium
                try:
                    recalculate_application_premium(app)
                    app.refresh_from_db()
                    # Get updated stored premium
                    if questionnaire.payment_frequency == "six_month":
                        stored_premium = float(app.six_month_premium or 0)
                    elif questionnaire.payment_frequency == "three_month":
                        stored_premium = float(app.three_month_premium or 0)
                    else:
                        stored_premium = float(app.annual_premium or 0)
                except Exception as e:
                    logger.warning(f"Could not auto-recalculate premium: {e}")
            
            breakdown.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            breakdown.append(f"ΣΥΝΟΛΟ ({frequency_label}): {calculated_total:.2f}€")

            
            return format_html('<br>'.join(breakdown))
        except Exception as e:
     
            logger.error(f"Error in price_breakdown_display: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return format_html('<span style="color: #dc3545;">Error: {}</span>'.format(str(e)))
    price_breakdown_display.short_description = 'Ανάλυση Τιμής'
    
    def application_program(self, obj):
        """Display program from application"""
        try:
            if obj and obj.application:
                program_map = {
                    'silver': 'Ασημένιο',
                    'gold': 'Χρυσό',
                    'platinum': 'Πλατινένιο',
                    'dynasty': 'Dynasty'
                }
                return program_map.get(obj.application.program, obj.application.program) or '-'
        except:
            pass
        return '-'
    application_program.short_description = 'Πρόγραμμα (από Αίτηση)'
    
    def application_pet_name(self, obj):
        """Display pet name from application"""
        try:
            if obj and obj.application:
                return obj.application.pet_name or '-'
        except:
            pass
        return '-'
    application_pet_name.short_description = 'Όνομα Κατοικίδιου'
    
    def application_pet_type(self, obj):
        """Display pet type from application"""
        try:
            if obj and obj.application:
                pet_type_map = {'dog': 'Σκύλος', 'cat': 'Γάτα'}
                return pet_type_map.get(obj.application.pet_type, obj.application.pet_type) or '-'
        except:
            pass
        return '-'
    application_pet_type.short_description = 'Είδος'
    
    def application_pet_breed(self, obj):
        """Display pet breed from application"""
        try:
            if obj and obj.application:
                return obj.application.pet_breed or '-'
        except:
            pass
        return '-'
    application_pet_breed.short_description = 'Ράτσα'
    
    def application_pet_birthdate(self, obj):
        """Display pet birthdate from application"""
        try:
            if obj and obj.application and obj.application.pet_birthdate:
                return obj.application.pet_birthdate.strftime('%d/%m/%Y')
        except:
            pass
        return '-'
    application_pet_birthdate.short_description = 'Ημερομηνία Γέννησης'
    
    def application_microchip(self, obj):
        """Display microchip number from application"""
        try:
            if obj and obj.application:
                return obj.application.microchip_number or '-'
        except:
            pass
        return '-'
    application_microchip.short_description = 'Αριθμός Microchip'
    
    def save_model(self, request, obj, form, change):
        """Override save to automatically regenerate contract when questionnaire fields affecting pricing change"""
        if change and obj.application:  # Only check for changes on existing questionnaires with applications
            # Get the original object from database
            original_obj = Questionnaire.objects.get(pk=obj.pk)
            
            # Define questionnaire fields that affect contract pricing/content
            contract_relevant_fields = [
                # Breed surcharges (affect pricing)
                'special_breed_5_percent', 'special_breed_20_percent',
                # Add-ons (affect pricing)
                'additional_poisoning_coverage', 'additional_blood_checkup',
                # Program selection (affects pricing)
                'program',
                # Pet information that might affect contract
                'pet_colors', 'pet_weight', 'is_purebred', 'is_mixed', 'is_crossbreed',
                # Health information that might be in contract
                'is_healthy', 'has_injury_illness_3_years', 'has_surgical_procedure',
                'has_examination_findings', 'is_sterilized',
                # Payment details
                'payment_method', 'payment_frequency',
                # Desired start date
                'desired_start_date'
            ]
            
            # Check if any contract-relevant field has changed
            fields_changed = False
            for field_name in contract_relevant_fields:
                original_value = getattr(original_obj, field_name, None)
                new_value = getattr(obj, field_name, None)
                if original_value != new_value:
                    fields_changed = True
                    break
            
            # Save the questionnaire first
            super().save_model(request, obj, form, change)
            
            # Regenerate contract if relevant fields changed and application has a contract
            if fields_changed and obj.application and hasattr(obj.application, 'contract_generated') and obj.application.contract_generated:
              
                logger.info(f"Questionnaire fields changed for application {obj.application.id}, regenerating contract...")
                
                try:
                    from .utils import generate_contract_pdf
                    from django.contrib import messages
                    
                    # Refresh application to get latest data
                    application = obj.application
                    
                    # Recalculate premium if pricing-related fields changed
                    pricing_fields = ['special_breed_5_percent', 'special_breed_20_percent', 
                                    'additional_poisoning_coverage', 'additional_blood_checkup', 'program']
                    pricing_changed = any(
                        getattr(original_obj, field, None) != getattr(obj, field, None)
                        for field in pricing_fields
                    )
                    
                    if pricing_changed:
                        from .utils import recalculate_application_premium
                        logger.info(f"Pricing fields changed, recalculating premium for application {application.id}")
                        recalculate_application_premium(application)
                        # Refresh application after recalculation
                        application.refresh_from_db()

                        application.save(update_fields=[
                        'annual_premium',
                        'six_month_premium',
                        'three_month_premium'
                    ])

                    
                    # Generate new contract (will have unique timestamp in filename)
                    pdf_paths = generate_contract_pdf(application)

                                        
                    if pdf_paths and len(pdf_paths) > 0:
                        # Update with new contract path (always a list)
                        application.contract_pdf_path = pdf_paths[0]  # Store first contract path
                        application.contract_generated = True
                        application.save(update_fields=['contract_pdf_path', 'contract_generated'])
                        
                        logger.info(f"Contract regenerated successfully for application {application.id} due to questionnaire changes")
                        try:
                            messages.success(request, 'Το συμβόλαιο αναδημιουργήθηκε αυτόματα λόγω αλλαγών στο ερωτηματολόγιο.')
                        except:
                            # Messages middleware not available (e.g., in tests)
                            pass
                except Exception as e:
                
                    logger.error(f"Error regenerating contract for application {obj.application.id}: {e}")
                    import traceback
                    logger.error(traceback.format_exc())
                    try:
                        messages.error(request, f'Σφάλμα κατά την αναδημιουργία του συμβολαίου: {str(e)}')
                    except:
                        # Messages middleware not available (e.g., in tests)
                        pass
        else:
            # New questionnaire or no application - just save normally
            super().save_model(request, obj, form, change)
    
    def has_add_permission(self, request):
        return True
    

