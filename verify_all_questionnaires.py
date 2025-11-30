"""
Verify all questionnaires in the database and show their data
"""
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pet_insurance.settings')
django.setup()

from main.models import Questionnaire

def verify_all():
    print("=" * 80)
    print("VERIFYING ALL QUESTIONNAIRES IN DATABASE")
    print("=" * 80)
    
    questionnaires = Questionnaire.objects.all().order_by('-id')
    print(f"\nTotal questionnaires: {questionnaires.count()}")
    
    for q in questionnaires:
        print(f"\n{'='*80}")
        print(f"Questionnaire ID: {q.id}")
        print(f"Application: {q.application}")
        print(f"Created: {q.created_at}")
        print(f"\nKey Fields:")
        print(f"  program: {q.program}")
        print(f"  payment_method: {q.payment_method}")
        print(f"  payment_frequency: {q.payment_frequency}")
        print(f"  additional_poisoning_coverage: {q.additional_poisoning_coverage}")
        print(f"  additional_blood_checkup: {q.additional_blood_checkup}")
        print(f"  has_other_insured_pet: {q.has_other_insured_pet}")
        print(f"  pet_colors: {q.pet_colors}")
        print(f"  pet_weight: {q.pet_weight}")
        print(f"  is_purebred: {q.is_purebred}")
        print(f"  is_healthy: {q.is_healthy}")
        print(f"  consent_terms_conditions: {q.consent_terms_conditions}")
        
        # Count populated fields
        populated = 0
        empty = 0
        for field in q._meta.get_fields():
            if field.name in ['id', 'application', 'created_at', 'updated_at']:
                continue
            try:
                value = getattr(q, field.name)
                if value is None or value == '' or (hasattr(field, 'default') and value == field.default):
                    empty += 1
                else:
                    populated += 1
            except:
                pass
        
        print(f"\n  Populated fields: {populated}")
        print(f"  Empty fields: {empty}")

if __name__ == '__main__':
    verify_all()


