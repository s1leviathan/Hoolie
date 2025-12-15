"""
Django management command to check font sizes of all PDF contract form fields
"""
from django.core.management.base import BaseCommand
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Check font sizes of all PDF contract form fields'

    def handle(self, *args, **options):
        template_path = os.path.join(
            settings.BASE_DIR,
            'ΑΣΦΑΛΙΣΤΗΡΙΟ ΣΥΜΒΟΛΑΙΟ ΤΕΛΙΚΟ PET (1) (2).pdf'
        )
        
        if not os.path.exists(template_path):
            self.stdout.write(self.style.ERROR(f"Template not found: {template_path}"))
            return
        
        try:
            import fitz  # PyMuPDF
            
            doc = fitz.open(template_path)
            self.stdout.write(f"\n{'='*80}")
            self.stdout.write(f"📄 PDF Template: {os.path.basename(template_path)}")
            self.stdout.write(f"{'='*80}\n")
            
            field_info = []
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                widgets = page.widgets()
                
                for widget in widgets:
                    if widget.field_type == fitz.PDF_WIDGET_TYPE_TEXT:
                        field_name = widget.field_name
                        
                        # Try to get font size from default appearance (DA)
                        font_size = "Unknown"
                        font_name = "Unknown"
                        
                        try:
                            # Access widget's annotation object to get underlying PDF object
                            annot = widget._annot
                            if annot:
                                # Get the annotation's dictionary
                                annot_dict = annot.get_dict()
                                
                                # Get DA (default appearance) string - this contains font info
                                da_string = annot_dict.get("DA", "")
                                
                                # If not found in annotation, try parent field
                                if not da_string:
                                    try:
                                        # Get the form field (parent)
                                        field = doc.get_field(field_name)
                                        if field and hasattr(field, 'get'):
                                            field_dict = field.get("field", {})
                                            da_string = field_dict.get("DA", "")
                                    except:
                                        pass
                                
                                if da_string:
                                    # DA format is like: "/Helvetica 10 Tf" or "/Arial 12 Tf 0.0 0.0 0.0 rg"
                                    import re
                                    # Match font name and size: "/FontName Size Tf"
                                    match = re.search(r'/([A-Za-z0-9\-_]+)\s+(\d+(?:\.\d+)?)\s+Tf', str(da_string))
                                    if match:
                                        font_name = match.group(1)
                                        font_size = match.group(2)
                                    else:
                                        # Try alternative pattern - just size
                                        match = re.search(r'(\d+(?:\.\d+)?)\s+Tf', str(da_string))
                                        if match:
                                            font_size = match.group(1)
                                        
                                        # Try to find font name separately
                                        match = re.search(r'/([A-Za-z0-9\-_]+)', str(da_string))
                                        if match:
                                            font_name = match.group(1)
                                else:
                                    font_size = "No DA found"
                        except Exception as e:
                            font_size = f"Error: {str(e)[:30]}"
                        
                        field_info.append({
                            'field_name': field_name,
                            'font_name': font_name,
                            'font_size': font_size,
                            'page': page_num + 1
                        })
            
            doc.close()
            
            # Sort by field name
            field_info.sort(key=lambda x: x['field_name'])
            
            # Display results
            self.stdout.write(f"{'Field Name':<25} {'Font Name':<20} {'Font Size':<12} {'Page'}")
            self.stdout.write("-" * 80)
            
            for info in field_info:
                self.stdout.write(
                    f"{info['field_name']:<25} {info['font_name']:<20} {info['font_size']:<12} {info['page']}"
                )
            
            self.stdout.write(f"\n{'='*80}")
            self.stdout.write(f"Total text fields found: {len(field_info)}")
            self.stdout.write(f"{'='*80}\n")
            
        except ImportError:
            self.stdout.write(self.style.ERROR("PyMuPDF (fitz) not available. Install with: pip install pymupdf"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error reading PDF: {e}"))
            import traceback
            self.stdout.write(traceback.format_exc())

