import qrcode
import io
import base64
from PIL import Image, ImageDraw, ImageFont
from django.conf import settings
from django.urls import reverse
import os

class QRCodeGenerator:
    """Generate various types of QR codes for the insurance system"""
    
    def __init__(self):
        self.brand_color = '#5ac8bd'  # Your brand color
        
    def generate_payment_qr(self, order_code, amount=None):
        """Generate QR code for Viva Wallet payment"""
        # Determine environment
        is_production = getattr(settings, 'VIVA_WALLET_PRODUCTION', False)
        
        if is_production:
            base_url = "https://www.vivapayments.com/web/checkout"
        else:
            base_url = "https://demo.vivapayments.com/web/checkout"
        
        # Build payment URL with brand color
        payment_url = f"{base_url}?ref={order_code}&color=5ac8bd"
        
        return self._generate_qr_code(
            data=payment_url,
            title="Scan to Pay",
            subtitle=f"Amount: {amount}€" if amount else None
        )
    
    def generate_contract_qr(self, application):
        """Generate QR code for contract information/verification"""
        # Create a verification URL (you'll need to create this view)
        contract_url = f"{settings.SITE_URL}/contract/verify/{application.contract_number}/"
        
        return self._generate_qr_code(
            data=contract_url,
            title="Contract Verification",
            subtitle=f"Contract: {application.contract_number}"
        )
    
    def generate_terms_qr(self):
        """Generate QR code for insurance terms and conditions"""
        terms_url = f"{settings.SITE_URL}/terms-and-conditions/"
        
        return self._generate_qr_code(
            data=terms_url,
            title="Terms & Conditions",
            subtitle="Scan to read full terms"
        )
    
    def generate_customer_portal_qr(self, application):
        """Generate QR code for customer portal access"""
        portal_url = f"{settings.SITE_URL}/customer/portal/{application.contract_number}/"
        
        return self._generate_qr_code(
            data=portal_url,
            title="Customer Portal",
            subtitle="Manage your policy"
        )
    
    def _generate_qr_code(self, data, title=None, subtitle=None, logo_path=None):
        """Generate QR code with optional branding"""
        # Create QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        # Create QR code image
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        # If we want to add branding (title, subtitle, logo)
        if title or subtitle or logo_path:
            qr_img = self._add_branding(qr_img, title, subtitle, logo_path)
        
        # Convert to base64 for easy embedding in HTML
        buffer = io.BytesIO()
        qr_img.save(buffer, format='PNG')
        buffer.seek(0)
        
        qr_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        return {
            'qr_code_base64': qr_base64,
            'qr_code_data_url': f"data:image/png;base64,{qr_base64}",
            'raw_data': data
        }
    
    def _add_branding(self, qr_img, title=None, subtitle=None, logo_path=None):
        """Add title, subtitle, and logo to QR code"""
        # Calculate dimensions
        qr_width, qr_height = qr_img.size
        
        # Add padding for text
        padding_top = 60 if title else 0
        padding_bottom = 40 if subtitle else 0
        
        # Create new image with padding
        new_height = qr_height + padding_top + padding_bottom
        new_img = Image.new('RGB', (qr_width, new_height), 'white')
        
        # Paste QR code
        new_img.paste(qr_img, (0, padding_top))
        
        # Add text
        draw = ImageDraw.Draw(new_img)
        
        try:
            # Try to use a nice font
            title_font = ImageFont.truetype("arial.ttf", 16)
            subtitle_font = ImageFont.truetype("arial.ttf", 12)
        except:
            # Fallback to default font
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
        
        if title:
            # Calculate text position (centered)
            title_bbox = draw.textbbox((0, 0), title, font=title_font)
            title_width = title_bbox[2] - title_bbox[0]
            title_x = (qr_width - title_width) // 2
            draw.text((title_x, 10), title, fill='black', font=title_font)
        
        if subtitle:
            subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
            subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
            subtitle_x = (qr_width - subtitle_width) // 2
            draw.text((subtitle_x, qr_height + padding_top + 10), subtitle, fill='gray', font=subtitle_font)
        
        # Add logo in center of QR code (optional)
        if logo_path and os.path.exists(logo_path):
            try:
                logo = Image.open(logo_path)
                # Resize logo to fit in center (about 1/5 of QR code size)
                logo_size = qr_width // 5
                logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
                
                # Calculate position (center of QR code)
                logo_x = (qr_width - logo_size) // 2
                logo_y = padding_top + (qr_height - logo_size) // 2
                
                # Create a white background for the logo
                logo_bg = Image.new('RGB', (logo_size + 10, logo_size + 10), 'white')
                logo_bg.paste(logo, (5, 5))
                
                new_img.paste(logo_bg, (logo_x - 5, logo_y - 5))
            except Exception as e:
                print(f"Could not add logo: {e}")
        
        return new_img

# Utility functions for easy use in views
def generate_payment_qr_for_application(application, order_code):
    """Generate payment QR code for an insurance application"""
    generator = QRCodeGenerator()
    return generator.generate_payment_qr(order_code, application.annual_premium)

def generate_contract_verification_qr(application):
    """Generate contract verification QR code"""
    generator = QRCodeGenerator()
    return generator.generate_contract_qr(application)

def generate_terms_qr():
    """Generate terms and conditions QR code"""
    generator = QRCodeGenerator()
    return generator.generate_terms_qr()



