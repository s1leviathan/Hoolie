"""
Django management command to verify that PDF contract has uniform font sizes
Actually analyzes the PDF to check font properties
"""
from django.core.management.base import BaseCommand
from django.conf import settings
from main.models import InsuranceApplication
from main.utils import generate_contract_pdf
import os
import tempfile

class Command(BaseCommand):
    help = 'Verify that generated PDF contract has uniform font sizes across all fields'

    def handle(self, *args, **options):
        # Find the latest application
        latest_app = InsuranceApplication.objects.order_by('-created_at').first()
        
        if not latest_app:
            self.stdout.write(self.style.ERROR("No InsuranceApplication found."))
            return
        
        self.stdout.write(f"\n{'='*80}")
        self.stdout.write(f"🔍 VERIFYING UNIFORM FONT SIZES IN PDF")
        self.stdout.write(f"{'='*80}\n")
        self.stdout.write(f"Application ID: {latest_app.id}")
        self.stdout.write(f"Contract Number: {latest_app.contract_number or 'N/A'}\n")
        
        # Generate the contract PDF
        self.stdout.write("📄 Generating contract PDF...")
        try:
            pdf_paths = generate_contract_pdf(latest_app)
            if isinstance(pdf_paths, list):
                pdf_path = pdf_paths[0]
            else:
                pdf_path = pdf_paths
            
            self.stdout.write(self.style.SUCCESS(f"✓ PDF generated: {pdf_path}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"✗ Error generating PDF: {e}"))
            import traceback
            self.stdout.write(traceback.format_exc())
            return
        
        # Check if PDF exists (might be in S3 or local storage)
        from django.core.files.storage import default_storage
        if default_storage.exists(pdf_path):
            # Download from S3 if needed
            with default_storage.open(pdf_path, 'rb') as f:
                pdf_content = f.read()
                # Save to temp file for analysis
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
                    tmp.write(pdf_content)
                    tmp_path = tmp.name
        elif os.path.exists(pdf_path):
            tmp_path = pdf_path
        else:
            self.stdout.write(self.style.ERROR(f"✗ PDF file not found: {pdf_path}"))
            return
        
        # Analyze font sizes in the PDF
        self.stdout.write(f"\n{'='*80}")
        self.stdout.write("🔬 ANALYZING PDF FONT SIZES")
        self.stdout.write(f"{'='*80}\n")
        
        try:
            import fitz  # PyMuPDF
            
            doc = fitz.open(tmp_path)
            
            # Check if PDF is flattened (no form fields = flattened)
            has_form_fields = False
            total_widgets = 0
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                widgets = page.widgets()
                if widgets:
                    has_form_fields = True
                    total_widgets += len(widgets)
            
            # Extract text and analyze font properties
            font_sizes_found = {}
            text_blocks = []
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                # Get text with font information
                text_dict = page.get_text("dict")
                
                for block in text_dict.get("blocks", []):
                    if "lines" in block:
                        for line in block["lines"]:
                            for span in line.get("spans", []):
                                font_size = span.get("size", 0)
                                font_name = span.get("font", "unknown")
                                text_content = span.get("text", "")
                                
                                if font_size > 0:
                                    key = f"{font_name}_{font_size}"
                                    if key not in font_sizes_found:
                                        font_sizes_found[key] = {
                                            'font': font_name,
                                            'size': font_size,
                                            'count': 0,
                                            'samples': []
                                        }
                                    font_sizes_found[key]['count'] += 1
                                    if len(font_sizes_found[key]['samples']) < 5:
                                        font_sizes_found[key]['samples'].append(text_content[:30])
                                    
                                    text_blocks.append({
                                        'font': font_name,
                                        'size': font_size,
                                        'text': text_content[:50]
                                    })
            
            doc.close()
            
            # Clean up temp file
            if tmp_path != pdf_path and os.path.exists(tmp_path):
                os.unlink(tmp_path)
            
            # Report results
            self.stdout.write(f"{'Font Name':<30} {'Size (pt)':<12} {'Occurrences':<15} {'Sample Text'}")
            self.stdout.write("-" * 100)
            
            unique_sizes = set()
            for key, info in sorted(font_sizes_found.items(), key=lambda x: x[1]['size']):
                unique_sizes.add(info['size'])
                sample = info['samples'][0] if info['samples'] else ""
                self.stdout.write(
                    f"{info['font'][:28]:<30} {info['size']:<12.1f} {info['count']:<15} {sample[:40]}"
                )
            
            self.stdout.write(f"\n{'='*80}")
            self.stdout.write("📊 SUMMARY")
            self.stdout.write(f"{'='*80}\n")
            
            self.stdout.write(f"Total text blocks analyzed: {len(text_blocks)}")
            self.stdout.write(f"Unique font sizes found: {sorted(unique_sizes)}")
            self.stdout.write(f"Unique font/size combinations: {len(font_sizes_found)}")
            self.stdout.write(f"PDF has form fields: {has_form_fields} (should be False if flattened)")
            self.stdout.write(f"Total widgets: {total_widgets} (should be 0 if flattened)\n")
            
            # Determine if fonts are uniform
            if not has_form_fields and total_widgets == 0:
                self.stdout.write(self.style.SUCCESS("✅ PDF IS FLATTENED (no form fields)"))
            else:
                self.stdout.write(self.style.WARNING(f"⚠️  PDF still has {total_widgets} form fields (not fully flattened)"))
            
            if len(unique_sizes) <= 2:
                # Allow for slight variations (e.g., headers vs body)
                sizes_list = sorted(unique_sizes)
                if len(sizes_list) == 1:
                    self.stdout.write(self.style.SUCCESS(f"✅ PERFECT: All text uses uniform {sizes_list[0]}pt font size!"))
                elif len(sizes_list) == 2:
                    diff = abs(sizes_list[1] - sizes_list[0])
                    if diff <= 2:
                        self.stdout.write(self.style.SUCCESS(f"✅ GOOD: Font sizes are very similar ({sizes_list[0]}pt and {sizes_list[1]}pt, diff={diff:.1f}pt)"))
                    else:
                        self.stdout.write(self.style.WARNING(f"⚠️  Font sizes differ: {sizes_list[0]}pt and {sizes_list[1]}pt (diff={diff:.1f}pt)"))
            else:
                self.stdout.write(self.style.ERROR(f"❌ FAILURE: Found {len(unique_sizes)} different font sizes: {sorted(unique_sizes)}"))
                self.stdout.write(self.style.ERROR("   Font sizes are NOT uniform!"))
            
            self.stdout.write(f"\n{'='*80}\n")
            
        except ImportError:
            self.stdout.write(self.style.ERROR("PyMuPDF (fitz) not available. Cannot analyze font sizes."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error analyzing PDF: {e}"))
            import traceback
            self.stdout.write(traceback.format_exc())

