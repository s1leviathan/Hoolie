"""
Django management command to test font normalization in PDF contracts
Generates a test contract and verifies all fields have uniform font sizes
"""
from django.core.management.base import BaseCommand
from django.conf import settings
from main.models import InsuranceApplication
from main.utils import generate_contract_pdf
import os
import re

class Command(BaseCommand):
    help = 'Test font normalization: Generate a contract and verify all fields have uniform font sizes'

    def handle(self, *args, **options):
        # Find the latest application or create a test one
        latest_app = InsuranceApplication.objects.order_by('-created_at').first()
        
        if not latest_app:
            self.stdout.write(self.style.ERROR("No InsuranceApplication found to test with."))
            return
        
        self.stdout.write(f"\n{'='*80}")
        self.stdout.write(f"🧪 TESTING FONT NORMALIZATION")
        self.stdout.write(f"{'='*80}\n")
        self.stdout.write(f"Using Application ID: {latest_app.id}")
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
        
        # Check if PDF exists
        if not os.path.exists(pdf_path):
            self.stdout.write(self.style.ERROR(f"✗ PDF file not found at: {pdf_path}"))
            return
        
        # Analyze font sizes in the PDF
        self.stdout.write(f"\n{'='*80}")
        self.stdout.write("🔍 ANALYZING FONT SIZES")
        self.stdout.write(f"{'='*80}\n")
        
        try:
            import fitz  # PyMuPDF
            
            doc = fitz.open(pdf_path)
            field_font_sizes = {}
            all_sizes = []
            issues = []
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                widgets = page.widgets()
                
                for widget in widgets:
                    if widget.field_type == fitz.PDF_WIDGET_TYPE_TEXT:
                        field_name = widget.field_name
                        font_size = None
                        font_name = None
                        
                        try:
                            # Try to read the DA (default appearance) string
                            annot = widget._annot
                            if annot:
                                annot_dict = annot.get_dict()
                                da_string = annot_dict.get("DA", "")
                                
                                if da_string:
                                    # Parse DA string: "/FontName Size Tf"
                                    match = re.search(r'/([A-Za-z0-9\-_]+)\s+(\d+(?:\.\d+)?)\s+Tf', str(da_string))
                                    if match:
                                        font_name = match.group(1)
                                        font_size = float(match.group(2))
                                        all_sizes.append(font_size)
                                        field_font_sizes[field_name] = {
                                            'font_name': font_name,
                                            'font_size': font_size,
                                            'page': page_num + 1
                                        }
                        except Exception as e:
                            issues.append(f"{field_name}: Error reading font - {str(e)[:50]}")
            
            doc.close()
            
            # Report results
            if field_font_sizes:
                self.stdout.write(f"{'Field Name':<25} {'Font Name':<20} {'Font Size':<12} {'Page'}")
                self.stdout.write("-" * 80)
                
                unique_sizes = set([info['font_size'] for info in field_font_sizes.values()])
                unique_fonts = set([info['font_name'] for info in field_font_sizes.values()])
                
                for field_name, info in sorted(field_font_sizes.items()):
                    size_str = f"{info['font_size']}"
                    if info['font_size'] != 10.0:
                        size_str += " ⚠️"
                    self.stdout.write(
                        f"{field_name:<25} {info['font_name']:<20} {size_str:<12} {info['page']}"
                    )
                
                self.stdout.write(f"\n{'='*80}")
                self.stdout.write("📊 SUMMARY")
                self.stdout.write(f"{'='*80}\n")
                
                self.stdout.write(f"Total text fields analyzed: {len(field_font_sizes)}")
                self.stdout.write(f"Unique font sizes found: {sorted(unique_sizes)}")
                self.stdout.write(f"Unique font names found: {sorted(unique_fonts)}")
                
                # Check for consistency
                if len(unique_sizes) == 1:
                    uniform_size = list(unique_sizes)[0]
                    if uniform_size == 10.0:
                        self.stdout.write(self.style.SUCCESS(f"\n✅ SUCCESS: All fields use uniform 10pt font size!"))
                    else:
                        self.stdout.write(self.style.WARNING(f"\n⚠️  WARNING: All fields use uniform {uniform_size}pt, but expected 10pt"))
                else:
                    self.stdout.write(self.style.ERROR(f"\n❌ FAILURE: Found {len(unique_sizes)} different font sizes: {sorted(unique_sizes)}"))
                    self.stdout.write(self.style.ERROR("   Font sizes are NOT uniform!"))
                
                if len(unique_fonts) == 1:
                    uniform_font = list(unique_fonts)[0]
                    self.stdout.write(self.style.SUCCESS(f"✅ All fields use uniform font: {uniform_font}"))
                else:
                    self.stdout.write(self.style.WARNING(f"⚠️  Multiple fonts found: {sorted(unique_fonts)}"))
                
                if issues:
                    self.stdout.write(f"\n⚠️  Issues found ({len(issues)}):")
                    for issue in issues[:5]:  # Show first 5 issues
                        self.stdout.write(f"   - {issue}")
                    if len(issues) > 5:
                        self.stdout.write(f"   ... and {len(issues) - 5} more")
            else:
                self.stdout.write(self.style.WARNING("⚠️  No font size information could be extracted from PDF fields"))
                if issues:
                    self.stdout.write(f"\nErrors encountered:")
                    for issue in issues[:10]:
                        self.stdout.write(f"   - {issue}")
            
            self.stdout.write(f"\n{'='*80}\n")
            
        except ImportError:
            self.stdout.write(self.style.ERROR("PyMuPDF (fitz) not available. Cannot analyze font sizes."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error analyzing PDF: {e}"))
            import traceback
            self.stdout.write(traceback.format_exc())

