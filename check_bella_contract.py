#!/usr/bin/env python
"""Check the latest Bella contract for encoding/truncation issues"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hoolie_pet_insurance.settings')
django.setup()

from main.models import InsuranceApplication
from main.fillpdf_utils import create_contract_field_mapping
from main.utils import get_pricing_values

# Find Bella's contract
app = InsuranceApplication.objects.filter(pet_name__icontains='Bella').order_by('-created_at').first()

if not app:
    print("❌ No contract found for 'Bella'")
    # Try latest contract
    app = InsuranceApplication.objects.filter(contract_generated=True).order_by('-created_at').first()
    if app:
        print(f"📄 Using latest contract instead: {app.pet_name}")

if app:
    print(f"\n{'='*80}")
    print(f"📋 Contract: {app.contract_number}")
    print(f"🐾 Pet: {app.pet_name}")
    print(f"📅 Created: {app.created_at}")
    print(f"📄 PDF Path: {app.contract_pdf_path}")
    print(f"{'='*80}\n")
    
    # Get pricing
    from main.fillpdf_utils import normalize_weight
    weight = normalize_weight(str(app.pet_weight_category))
    net, fee, ipt, gross = get_pricing_values(
        app, app.pet_type, weight, app.program, 
        app.get_payment_frequency() or "annual"
    )
    
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
    
    print("📝 PDF FIELD VALUES:\n")
    for field_name, field_value in sorted(field_mapping.items()):
        if field_name.startswith('text_'):
            # Check for potential issues
            value_str = str(field_value)
            issues = []
            
            # Check length
            if len(value_str) > 50:
                issues.append(f"⚠️ LONG ({len(value_str)} chars)")
            
            # Check for encoding issues
            try:
                value_str.encode('utf-8')
            except UnicodeEncodeError:
                issues.append("❌ ENCODING ERROR")
            
            # Check for cut words (ends with incomplete word)
            if value_str and ' ' in value_str and not value_str.endswith(' '):
                last_word = value_str.split()[-1]
                if len(last_word) < 3:  # Very short last word might indicate truncation
                    issues.append("⚠️ POSSIBLE TRUNCATION")
            
            issue_str = " | ".join(issues) if issues else "✅"
            print(f"  {field_name:20} = {value_str[:60]:60} {issue_str}")
            if len(value_str) > 60:
                print(f"  {'':20}   ... ({len(value_str)} total chars)")
    
    print(f"\n{'='*80}")
    print("🔍 CHECKING FOR COMMON ISSUES:\n")
    
    # Check specific fields that commonly have issues
    checks = {
        'text_3ksjz': 'Full Name',
        'text_11qthp': 'Address',
        'text_14rclu': 'Pet Name',
        'text_16jfkm': 'Pet Breed',
        'text_7tbbt': 'Program + Frequency',
        'text_30vzyv': 'Surcharges',
        'text_31mdpf': 'Poisoning Add-on',
        'text_32crsg': 'Blood Checkup Add-on',
    }
    
    for field, label in checks.items():
        value = field_mapping.get(field, '')
        if value:
            print(f"  {label:25} ({field:15}): {value}")
            # Check for Greek characters
            has_greek = any('\u0370' <= char <= '\u03FF' for char in str(value))
            if has_greek:
                print(f"    {'':25} ✓ Contains Greek characters")
        else:
            print(f"  {label:25} ({field:15}): (empty)")
    
    print(f"\n{'='*80}")

else:
    print("❌ No contracts found")

