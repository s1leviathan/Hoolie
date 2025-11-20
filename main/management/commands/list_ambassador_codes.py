"""
Django management command to list all ambassador/partner codes
"""
from django.core.management.base import BaseCommand
from main.models import AmbassadorCode

class Command(BaseCommand):
    help = 'List all ambassador/partner codes'

    def handle(self, *args, **options):
        codes = AmbassadorCode.objects.all().order_by('code')
        
        self.stdout.write(self.style.SUCCESS('\n📋 Ambassador/Partner Codes:\n'))
        
        if codes.exists():
            for code in codes:
                discount_info = f"{code.discount_percentage}%" if code.discount_percentage > 0 else f"{code.discount_amount}€"
                uses_info = f"{code.current_uses}/{code.max_uses}" if code.max_uses else f"{code.current_uses}/∞"
                status = "✅ Active" if code.is_active else "❌ Inactive"
                
                self.stdout.write(
                    f'  • {self.style.SUCCESS(code.code)} - {code.name}'
                )
                self.stdout.write(
                    f'    Type: {code.get_code_type_display()} | '
                    f'Discount: {discount_info} | '
                    f'Uses: {uses_info} | '
                    f'{status}'
                )
                if code.description:
                    self.stdout.write(f'    Description: {code.description}')
                self.stdout.write('')
            
            self.stdout.write(self.style.SUCCESS(f'\n✅ Total: {codes.count()} codes\n'))
        else:
            self.stdout.write(self.style.WARNING('  No codes found.\n'))

