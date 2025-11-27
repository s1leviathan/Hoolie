import os
from datetime import datetime
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

def generate_contract_pdf(application):
    """Generate insurance contract PDF(s) using fillpdf library and save to S3/local storage"""
    
    # Refresh application from database to ensure questionnaire relationship is loaded
    from .models import InsuranceApplication
    application = InsuranceApplication.objects.select_related('questionnaire').get(pk=application.pk)
    
    # Use temporary directory for PDF generation (will be uploaded to S3)
    import tempfile
    temp_dir = tempfile.mkdtemp()
    
    try:
        # If there are two pets, generate separate contracts
        if application.has_second_pet and application.second_pet_name:
            print(f"🐾 Generating separate contracts for two pets...")
            
            # Generate contract for first pet
            filename1 = f"contract_{application.contract_number}_pet1_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            temp_filepath1 = os.path.join(temp_dir, filename1)
            
            # Generate contract for second pet  
            filename2 = f"contract_{application.contract_number}_pet2_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            temp_filepath2 = os.path.join(temp_dir, filename2)
            
            # Use fillpdf library to generate PDFs
            from .fillpdf_utils import generate_contract_with_fillpdf
            contract1_path = generate_contract_with_fillpdf(application, temp_filepath1, pet_number=1)
            contract2_path = generate_contract_with_fillpdf(application, temp_filepath2, pet_number=2)
            
            # Upload to S3/local storage
            s3_paths = []
            for temp_path, filename in [(contract1_path, filename1), (contract2_path, filename2)]:
                if os.path.exists(temp_path):
                    s3_key = f'contracts/{filename}'
                    with open(temp_path, 'rb') as f:
                        saved_path = default_storage.save(s3_key, ContentFile(f.read()))
                        s3_paths.append(saved_path)
            
            return s3_paths
        
        else:
            # Single pet contract
            print(f"🐾 Generating contract for single pet...")
            filename = f"contract_{application.contract_number}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            temp_filepath = os.path.join(temp_dir, filename)
            
            # Use fillpdf library to generate PDF
            from .fillpdf_utils import generate_contract_with_fillpdf
            contract_path = generate_contract_with_fillpdf(application, temp_filepath, pet_number=1)
            
            # Upload to S3/local storage
            if os.path.exists(contract_path):
                s3_key = f'contracts/{filename}'
                with open(contract_path, 'rb') as f:
                    saved_path = default_storage.save(s3_key, ContentFile(f.read()))
                    return [saved_path]
            
            return []
    finally:
        # Clean up temporary directory
        import shutil
        try:
            shutil.rmtree(temp_dir)
        except:
            pass


