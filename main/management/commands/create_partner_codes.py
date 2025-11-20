from django.core.management.base import BaseCommand
from main.models import AmbassadorCode
from django.utils import timezone


class Command(BaseCommand):
    help = 'Create promo codes for partners'

    def handle(self, *args, **options):
        partners = [
            {
                'name': 'Μαργαρίτα Δημητριάδου',
                'email': 'magie@pos-creation.com',
                'code': 'MARGARITA2024',
                'discount_percentage': 10.00,
            },
            {
                'name': 'Δέσποινα Ευθυμίου',
                'email': 'anatomy.diaries@gmail.com',
                'code': 'DESPOINA2024',
                'discount_percentage': 10.00,
            },
            {
                'name': 'Βεληβασάκης Κωνσταντίνος',
                'email': 'newlifeins@hotmail.gr',
                'code': 'VELIVASAKIS2024',
                'discount_percentage': 10.00,
            },
            {
                'name': 'Λουίζος Κωνσταντίνος',
                'email': 'konlouizos@gmail.com',
                'code': 'LOUIZOS2024',
                'discount_percentage': 10.00,
            },
            {
                'name': 'Ηλίας Παυλής',
                'email': 'pavlis@insurance4you.gr',
                'code': 'PAVLIS2024',
                'discount_percentage': 10.00,
            },
        ]
        
        created_count = 0
        updated_count = 0
        
        for partner in partners:
            code_obj, created = AmbassadorCode.objects.get_or_create(
                code=partner['code'],
                defaults={
                    'code_type': 'partner',
                    'name': partner['name'],
                    'description': f'Promo code for {partner["name"]} ({partner["email"]})',
                    'discount_percentage': partner['discount_percentage'],
                    'discount_amount': 0,
                    'max_discount': None,
                    'max_uses': None,  # Unlimited uses
                    'current_uses': 0,
                    'is_active': True,
                    'valid_from': None,
                    'valid_until': None,  # No expiry
                    'created_by': 'Management Command',
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created code: {partner["code"]} for {partner["name"]}')
                )
            else:
                # Update existing code to ensure it's active and valid
                code_obj.is_active = True
                code_obj.discount_percentage = partner['discount_percentage']
                code_obj.valid_until = None
                code_obj.max_uses = None
                code_obj.save()
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'↻ Updated code: {partner["code"]} for {partner["name"]}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✓ Successfully processed {len(partners)} partner codes:\n'
                f'  - Created: {created_count}\n'
                f'  - Updated: {updated_count}'
            )
        )
        
        # Print all codes for reference
        self.stdout.write('\n📋 Partner Codes:')
        for partner in partners:
            self.stdout.write(f'  • {partner["code"]} - {partner["name"]} ({partner["email"]})')

