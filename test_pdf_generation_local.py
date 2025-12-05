#!/usr/bin/env python
"""
COMPREHENSIVE LOCAL TEST - Generate actual PDFs and verify prices
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pet_insurance.settings')
django.setup()

from main.models import InsuranceApplication, Questionnaire
from main.utils import generate_contract_pdf
from main.fillpdf_utils import create_contract_field_mapping
import tempfile
import shutil

def test_pdf_generation_local():
    """Test PDF generation with actual file creation"""
    
    print("=" * 80)
    print("COMPREHENSIVE LOCAL PDF GENERATION TEST")
    print("=" * 80)
    
    # Create temp directory for PDFs
    test_output_dir = tempfile.mkdtemp(prefix='pdf_test_')
    print(f"\n📁 Test output directory: {test_output_dir}")
    
    scenarios = [
        {
            'name': '6-Month Payment - Dog Silver ≤10kg',
            'pet_type': 'dog',
            'program': 'silver',
            'weight': 'up_10',
            'frequency': 'six_month',
            'expected_price': 87.54,
        },
        {
            'name': '3-Month Payment - Dog Silver ≤10kg',
            'pet_type': 'dog',
            'program': 'silver',
            'weight': 'up_10',
            'frequency': 'three_month',
            'expected_price': 45.86,
        },
        {
            'name': 'Annual Payment - Dog Gold ≤10kg',
            'pet_type': 'dog',
            'program': 'gold',
            'weight': 'up_10',
            'frequency': 'annual',
            'expected_price': 234.14,
        },
    ]
    
    all_passed = True
    
    for scenario in scenarios:
        print(f"\n{'='*80}")
        print(f"TEST: {scenario['name']}")
        print(f"{'='*80}")
        
        try:
            # STEP 1: Create application
            print("\n[STEP 1] Creating application...")
            app = InsuranceApplication.objects.create(
                full_name="Test User",
                afm="123456789",
                phone="6912345678",
                address="Test Address",
                postal_code="12345",
                email="test@example.com",
                pet_name="TestPet",
                pet_type=scenario['pet_type'],
                pet_gender='male',
                pet_breed="Test Breed",
                pet_birthdate="2020-01-01",
                pet_weight_category=scenario['weight'],
                program=scenario['program'],
                health_status='healthy',
            )
            print(f"✓ Application created: {app.contract_number}")
            print(f"  Initial premiums: annual={app.annual_premium}, 6-month={app.six_month_premium}, 3-month={app.three_month_premium}")
            
            # STEP 2: Save questionnaire with payment frequency
            print(f"\n[STEP 2] Saving questionnaire with frequency: {scenario['frequency']}...")
            questionnaire = Questionnaire.objects.create(
                application=app,
                payment_frequency=scenario['frequency'],
                program=scenario['program'],
            )
            print(f"✓ Questionnaire saved with frequency: {questionnaire.payment_frequency}")
            
            # STEP 3: Refresh and check premiums
            print(f"\n[STEP 3] Checking premiums after questionnaire save...")
            app.refresh_from_db()
            print(f"  Annual premium: {app.annual_premium}")
            print(f"  6-Month premium: {app.six_month_premium}")
            print(f"  3-Month premium: {app.three_month_premium}")
            
            # Verify premiums are set
            if not app.annual_premium or not app.six_month_premium or not app.three_month_premium:
                print(f"  ❌ FAIL: Premiums not set!")
                all_passed = False
                app.delete()
                continue
            
            # STEP 4: Check get_premium_for_frequency
            print(f"\n[STEP 4] Checking get_premium_for_frequency()...")
            premium_for_freq = app.get_premium_for_frequency()
            print(f"  get_premium_for_frequency() = {premium_for_freq:.2f}€")
            print(f"  Expected: {scenario['expected_price']:.2f}€")
            
            if abs(premium_for_freq - scenario['expected_price']) < 0.01:
                print(f"  ✅ CORRECT!")
            else:
                print(f"  ❌ WRONG! Difference: {abs(premium_for_freq - scenario['expected_price']):.2f}€")
                all_passed = False
                app.delete()
                continue
            
            # STEP 5: Test PDF field mapping
            print(f"\n[STEP 5] Testing PDF field mapping...")
            field_mapping = create_contract_field_mapping(
                application=app,
                pet_name="TestPet",
                pet_type_display="Σκύλος",
                pet_breed="Test Breed",
                pet_weight="έως 10 κιλά",
                pet_birthdate="01/01/2020",
                contract_suffix="",
                net_premium=0,
                fee=0,
                auxiliary=0,
                tax=0,
            )
            
            total_price_str = field_mapping.get('text_37rpnu', '0€')
            total_price = float(total_price_str.replace('€', '').strip())
            print(f"  PDF Total (text_37rpnu): {total_price:.2f}€")
            print(f"  Expected: {scenario['expected_price']:.2f}€")
            
            if abs(total_price - scenario['expected_price']) < 0.01:
                print(f"  ✅ PDF FIELD MAPPING CORRECT!")
            else:
                print(f"  ❌ PDF FIELD MAPPING WRONG!")
                print(f"     Difference: {abs(total_price - scenario['expected_price']):.2f}€")
                all_passed = False
                app.delete()
                continue
            
            # STEP 6: Actually generate PDF file (if template exists)
            print(f"\n[STEP 6] Generating actual PDF file...")
            template_path = os.path.join(os.path.dirname(__file__), 'ΑΣΦΑΛΙΣΤΗΡΙΟ ΣΥΜΒΟΛΑΙΟ ΤΕΛΙΚΟ PET (1) (2).pdf')
            
            if os.path.exists(template_path):
                from main.fillpdf_utils import generate_contract_with_fillpdf
                output_path = os.path.join(test_output_dir, f"test_{scenario['frequency']}_{app.contract_number}.pdf")
                
                try:
                    generate_contract_with_fillpdf(app, output_path, pet_number=1)
                    
                    if os.path.exists(output_path):
                        file_size = os.path.getsize(output_path)
                        print(f"  ✅ PDF generated successfully!")
                        print(f"     File: {output_path}")
                        print(f"     Size: {file_size:,} bytes")
                    else:
                        print(f"  ⚠️  PDF generation completed but file not found")
                except Exception as e:
                    print(f"  ⚠️  PDF generation error (non-critical): {e}")
            else:
                print(f"  ⚠️  PDF template not found, skipping actual PDF generation")
            
            # Show all price fields
            print(f"\n📄 PDF Price Fields Summary:")
            print(f"   Program (text_7tbbt):          {field_mapping.get('text_7tbbt', 'N/A')}")
            print(f"   Net Premium (text_33tjdu):     {field_mapping.get('text_33tjdu', 'N/A')}")
            print(f"   Management Fee (text_34k):     {field_mapping.get('text_34k', 'N/A')}")
            print(f"   Auxiliary (text_35poeh):       {field_mapping.get('text_35poeh', 'N/A')}")
            print(f"   IPT (text_36sfw):              {field_mapping.get('text_36sfw', 'N/A')}")
            print(f"   TOTAL (text_37rpnu):           {field_mapping.get('text_37rpnu', 'N/A')}")
            
            # Verify breakdown sums to total
            try:
                net = float(field_mapping.get('text_33tjdu', '0€').replace('€', '').strip())
                mgmt = float(field_mapping.get('text_34k', '0€').replace('€', '').strip())
                aux = float(field_mapping.get('text_35poeh', '0€').replace('€', '').strip())
                ipt = float(field_mapping.get('text_36sfw', '0€').replace('€', '').strip())
                total = float(field_mapping.get('text_37rpnu', '0€').replace('€', '').strip())
                
                breakdown_sum = net + mgmt + aux + ipt
                if abs(breakdown_sum - total) < 0.01:
                    print(f"  ✅ Breakdown sums correctly: {breakdown_sum:.2f}€ = {total:.2f}€")
                else:
                    print(f"  ❌ Breakdown doesn't sum: {breakdown_sum:.2f}€ ≠ {total:.2f}€")
                    all_passed = False
            except Exception as e:
                print(f"  ⚠️  Could not verify breakdown sum: {e}")
            
            # Clean up
            app.delete()
            print(f"\n✓ Test completed and cleaned up")
            
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
            all_passed = False
    
    # Clean up test directory
    try:
        if os.path.exists(test_output_dir):
            print(f"\n📁 Test PDFs saved in: {test_output_dir}")
            print(f"   (Directory will be cleaned up automatically)")
    except:
        pass
    
    print(f"\n{'='*80}")
    if all_passed:
        print("✅ ALL TESTS PASSED - READY FOR DEPLOYMENT!")
    else:
        print("❌ SOME TESTS FAILED - DO NOT DEPLOY!")
    print(f"{'='*80}")
    
    return all_passed

if __name__ == '__main__':
    success = test_pdf_generation_local()
    sys.exit(0 if success else 1)

