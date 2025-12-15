from django.core.management.base import BaseCommand
from main.models import InsuranceApplication
from main.fillpdf_utils import create_contract_field_mapping, get_pricing_values, normalize_weight


class Command(BaseCommand):
    help = 'Check contract PDF fields for encoding/truncation issues'

    def handle(self, *args, **options):
        # Find Bella's contract
        app = InsuranceApplication.objects.filter(pet_name__icontains='Bella').order_by('-created_at').first()
        
        if not app:
            self.stdout.write(self.style.WARNING("No contract found for 'Bella'"))
            app = InsuranceApplication.objects.filter(contract_generated=True).order_by('-created_at').first()
            if app:
                self.stdout.write(f"Using latest contract: {app.pet_name}")
        
        if not app:
            self.stdout.write(self.style.ERROR("No contracts found"))
            return
        
        self.stdout.write(f"\n{'='*80}")
        self.stdout.write(f"Contract: {app.contract_number}")
        self.stdout.write(f"Pet: {app.pet_name}")
        self.stdout.write(f"PDF Path: {app.contract_pdf_path}")
        self.stdout.write(f"{'='*80}\n")
        
        # Get pricing with correct frequency key
        weight = normalize_weight(str(app.pet_weight_category))
        payment_freq = app.get_payment_frequency() or "annual"
        freq_map = {"annual": "annual", "six_month": "6m", "three_month": "3m"}
        freq_key = freq_map.get(payment_freq, "annual")
        
        try:
            net, fee, ipt, gross = get_pricing_values(
                app, app.pet_type, weight, app.program, freq_key
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error getting pricing: {e}"))
            return
        
        # Create field mapping
        field_mapping = create_contract_field_mapping(
            application=app,
            pet_name=app.pet_name or "",
            pet_type_display=app.get_pet_type_display_greek(),
            pet_breed=app.pet_breed or "",
            pet_weight=app.get_weight_display(weight) if weight else "",
            pet_birthdate=app.pet_birthdate.strftime('%d/%m/%Y') if app.pet_birthdate else "",
            contract_suffix="",
            net_premium=net,
            fee=fee,
            ipt=ipt,
            gross=gross
        )
        
        self.stdout.write("\n📝 PDF FIELD VALUES:\n")
        for field_name, field_value in sorted(field_mapping.items()):
            if field_name.startswith('text_'):
                value_str = str(field_value)
                issues = []
                
                if len(value_str) > 50:
                    issues.append(f"LONG ({len(value_str)} chars)")
                
                try:
                    value_str.encode('utf-8')
                except UnicodeEncodeError:
                    issues.append("ENCODING ERROR")
                
                issue_str = " | ".join(issues) if issues else "OK"
                self.stdout.write(f"  {field_name:20} = {value_str[:70]:70} [{issue_str}]")
                if len(value_str) > 70:
                    self.stdout.write(f"    {'':20}   ... ({len(value_str)} total chars)")
        
        self.stdout.write(f"\n{'='*80}")
        self.stdout.write("🔍 KEY FIELDS:\n")
        
        key_fields = {
            'text_3ksjz': 'Full Name',
            'text_11qthp': 'Address',
            'text_14rclu': 'Pet Name',
            'text_16jfkm': 'Pet Breed',
            'text_7tbbt': 'Program + Frequency',
            'text_30vzyv': 'Surcharges',
            'text_31mdpf': 'Poisoning Add-on',
            'text_32crsg': 'Blood Checkup Add-on',
        }
        
        for field, label in key_fields.items():
            value = field_mapping.get(field, '')
            self.stdout.write(f"  {label:25} ({field:15}): {value}")
        
        self.stdout.write(f"\n{'='*80}")

