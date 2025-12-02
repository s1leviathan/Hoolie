"""
Test script to verify all questionnaire fields are saved correctly
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pet_insurance.settings')
django.setup()

from main.models import Questionnaire, InsuranceApplication
from django.utils import timezone
from datetime import date

def test_questionnaire_fields():
    """Test that all questionnaire fields can be saved and retrieved"""
    
    print("=" * 80)
    print("TESTING QUESTIONNAIRE FIELDS")
    print("=" * 80)
    
    # Get all Questionnaire model fields
    from django.db import models
    questionnaire_fields = [f.name for f in Questionnaire._meta.get_fields() if isinstance(f, models.Field)]
    
    # Remove relationship fields and auto fields
    excluded_fields = ['id', 'application', 'created_at', 'updated_at']
    testable_fields = [f for f in questionnaire_fields if f not in excluded_fields]
    
    print(f"\nFound {len(testable_fields)} testable fields in Questionnaire model:")
    for i, field in enumerate(testable_fields, 1):
        print(f"  {i:2d}. {field}")
    
    # Use existing application or create minimal one
    print("\n" + "-" * 80)
    print("Finding or creating test application...")
    
    # Try to get an existing application
    test_app = InsuranceApplication.objects.first()
    
    if not test_app:
        # Create minimal application with all required fields
        from django.db import connection
        notnull_cols = {}
        with connection.cursor() as cursor:
            vendor = connection.vendor
            if vendor == 'sqlite':
                cursor.execute("PRAGMA table_info(main_insuranceapplication)")
                table_info = cursor.fetchall()
                notnull_cols = {row[1]: row[3] == 1 for row in table_info}
            elif vendor == 'postgresql':
                cursor.execute("""
                    SELECT column_name, is_nullable
                    FROM information_schema.columns
                    WHERE table_name = 'main_insuranceapplication'
                """)
                table_info = cursor.fetchall()
                notnull_cols = {row[0]: row[1] == 'NO' for row in table_info}
            else:
                # Fallback: assume no legacy columns
                notnull_cols = {}
        
        # Build minimal required fields
        required_fields = {
            'full_name': "Test User",
            'email': "test@example.com",
            'phone': "1234567890",
            'afm': "123456789",
            'address': "Test Address",
            'postal_code': "12345",
            'pet_name': "Test Pet",
            'pet_type': "dog",
            'pet_gender': "male",
            'pet_breed': "Test Breed",
            'pet_birthdate': date(2020, 1, 1),
            'pet_weight_category': "10_25",
            'program': "gold",
            'annual_premium': 300.00,
            'status': "pending",
        }
        
        # Add required NOT NULL fields based on database schema
        if notnull_cols.get('microchip_number', False):
            required_fields['microchip_number'] = ""
        if notnull_cols.get('second_pet_name', False):
            required_fields['has_second_pet'] = False
            required_fields['second_pet_name'] = ""
            required_fields['second_pet_type'] = "dog"
            required_fields['second_pet_gender'] = "male"
            required_fields['second_pet_breed'] = ""
            required_fields['second_pet_weight_category'] = "10_25"
            required_fields['second_pet_health_status'] = ""
        if notnull_cols.get('second_pet_health_conditions', False):
            required_fields['second_pet_health_conditions'] = ""
        if notnull_cols.get('contract_pdf_path', False):
            required_fields['contract_pdf_path'] = ""
        
        test_app = InsuranceApplication.objects.create(**required_fields)
        print(f"✓ Created test application: {test_app.id} ({test_app.contract_number})")
    else:
        print(f"✓ Using existing application: {test_app.id} ({test_app.contract_number})")
    
    # Create test data for all fields
    print("\n" + "-" * 80)
    print("Creating questionnaire with all fields...")
    
    test_data = {
        'application': test_app,
        'has_other_insured_pet': True,
        'has_been_denied_insurance': False,
        'has_special_terms_imposed': False,
        'pet_colors': 'Brown, White',
        'pet_weight': '11-20 κιλά',
        'is_purebred': True,
        'is_mixed': False,
        'is_crossbreed': False,
        'special_breed_5_percent': False,
        'special_breed_20_percent': False,
        'is_healthy': True,
        'is_healthy_details': '',
        'has_injury_illness_3_years': False,
        'has_injury_illness_details': '',
        'has_surgical_procedure': False,
        'has_surgical_procedure_details': '',
        'has_examination_findings': False,
        'has_examination_findings_details': '',
        'is_sterilized': True,
        'is_vaccinated_leishmaniasis': True,
        'follows_vaccination_program': True,
        'follows_vaccination_program_details': '',
        'has_hereditary_disease': False,
        'has_hereditary_disease_details': '',
        'program': 'gold',
        'additional_poisoning_coverage': True,
        'additional_blood_checkup': True,
        'desired_start_date': date(2025, 2, 1),
        'payment_method': 'card',
        'payment_frequency': 'annual',
        'consent_terms_conditions': True,
        'consent_info_document': True,
        'consent_email_notifications': True,
        'consent_marketing': False,
        'consent_data_processing': True,
        'consent_pet_gov_platform': True,
    }
    
    # Create questionnaire
    questionnaire = Questionnaire.objects.create(**test_data)
    print(f"✓ Created questionnaire: {questionnaire.id}")
    
    # Verify all fields are saved
    print("\n" + "-" * 80)
    print("Verifying all fields are saved correctly...")
    
    missing_fields = []
    empty_fields = []
    populated_fields = []
    
    for field_name in testable_fields:
        value = getattr(questionnaire, field_name, None)
        
        # Check if field exists
        if not hasattr(questionnaire, field_name):
            missing_fields.append(field_name)
            continue
        
        # Check if field has expected value
        if field_name in test_data:
            expected = test_data[field_name]
            if value != expected:
                print(f"  ⚠ {field_name}: Expected '{expected}', Got '{value}'")
            else:
                populated_fields.append(field_name)
        else:
            # Field not in test data, check if it has a default value
            field = Questionnaire._meta.get_field(field_name)
            if hasattr(field, 'default') and field.default != models.NOT_PROVIDED:
                if value == field.default:
                    populated_fields.append(field_name)
                else:
                    empty_fields.append(field_name)
            elif value is None or value == '' or value == False:
                empty_fields.append(field_name)
            else:
                populated_fields.append(field_name)
    
    # Print results
    print(f"\n✓ Populated fields ({len(populated_fields)}):")
    for field in populated_fields:
        value = getattr(questionnaire, field, None)
        print(f"    - {field}: {value}")
    
    if empty_fields:
        print(f"\n⚠ Empty/Default fields ({len(empty_fields)}):")
        for field in empty_fields:
            value = getattr(questionnaire, field, None)
            print(f"    - {field}: {value}")
    
    if missing_fields:
        print(f"\n❌ Missing fields ({len(missing_fields)}):")
        for field in missing_fields:
            print(f"    - {field}")
    
    # Check admin fieldsets
    print("\n" + "-" * 80)
    print("Checking admin configuration...")
    
    from main.admin import QuestionnaireAdmin
    admin = QuestionnaireAdmin(Questionnaire, None)
    
    # Get all fields from fieldsets
    admin_fields = []
    if hasattr(admin, 'fieldsets'):
        for name, options in admin.fieldsets:
            if 'fields' in options:
                admin_fields.extend(options['fields'])
    
    # Check if all model fields are in admin
    admin_missing = [f for f in testable_fields if f not in admin_fields]
    
    if admin_missing:
        print(f"\n⚠ Fields not in admin fieldsets ({len(admin_missing)}):")
        for field in admin_missing:
            print(f"    - {field}")
    else:
        print("✓ All fields are in admin fieldsets")
    
    # Final summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"Total model fields: {len(testable_fields)}")
    print(f"Populated fields: {len(populated_fields)}")
    print(f"Empty/Default fields: {len(empty_fields)}")
    print(f"Missing fields: {len(missing_fields)}")
    print(f"Fields in admin: {len(admin_fields)}")
    print(f"Fields missing from admin: {len(admin_missing)}")
    
    if missing_fields or admin_missing:
        print("\n❌ TEST FAILED - Some fields are missing")
        return False
    else:
        print("\n✓ TEST PASSED - All fields are present and accessible")
        return True

if __name__ == '__main__':
    try:
        success = test_questionnaire_fields()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

