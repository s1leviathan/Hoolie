import os
from datetime import datetime
from django.conf import settings

def generate_contract_pdf(application):
    """Generate insurance contract PDF(s) using fillpdf library"""
    
    # Create contracts directory if it doesn't exist
    contracts_dir = os.path.join(settings.MEDIA_ROOT, 'contracts')
    os.makedirs(contracts_dir, exist_ok=True)
    
    # If there are two pets, generate separate contracts
    if application.has_second_pet and application.second_pet_name:
        print(f"🐾 Generating separate contracts for two pets...")
        
        # Generate contract for first pet
        filename1 = f"contract_{application.contract_number}_pet1_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath1 = os.path.join(contracts_dir, filename1)
        
        # Generate contract for second pet  
        filename2 = f"contract_{application.contract_number}_pet2_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath2 = os.path.join(contracts_dir, filename2)
        
        # Use fillpdf library (the only working method)
        from .fillpdf_utils import generate_contract_with_fillpdf
        contract1_path = generate_contract_with_fillpdf(application, filepath1, pet_number=1)
        contract2_path = generate_contract_with_fillpdf(application, filepath2, pet_number=2)
        return [contract1_path, contract2_path]
    
    else:
        # Single pet contract
        print(f"🐾 Generating contract for single pet...")
        filename = f"contract_{application.contract_number}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(contracts_dir, filename)
        
        # Use fillpdf library (the only working method)
        from .fillpdf_utils import generate_contract_with_fillpdf
        contract_path = generate_contract_with_fillpdf(application, filepath, pet_number=1)
        return [contract_path]


