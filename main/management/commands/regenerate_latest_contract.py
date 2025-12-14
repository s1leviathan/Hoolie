from django.core.management.base import BaseCommand
from main.models import InsuranceApplication
from main.utils import generate_contract_pdf, recalculate_application_premium


class Command(BaseCommand):
    help = 'Regenerate the latest contract to test changes'

    def handle(self, *args, **options):
        app = InsuranceApplication.objects.order_by('-created_at').first()
        
        if not app:
            self.stdout.write(self.style.ERROR('No applications found'))
            return
        
        self.stdout.write(f"Found contract: {app.contract_number}")
        
        if not app.questionnaire:
            self.stdout.write(self.style.ERROR('No questionnaire found'))
            return
        
        q = app.questionnaire
        self.stdout.write(f"Payment Frequency: {q.payment_frequency}")
        self.stdout.write(f"Poisoning Coverage: {q.additional_poisoning_coverage}")
        self.stdout.write(f"Blood Checkup: {q.additional_blood_checkup}")
        
        self.stdout.write(f"\nCurrent Premiums:")
        self.stdout.write(f"  Annual: {app.annual_premium}")
        self.stdout.write(f"  6-Month: {app.six_month_premium}")
        self.stdout.write(f"  3-Month: {app.three_month_premium}")
        
        self.stdout.write(f"\nRecalculating premiums...")
        recalculate_application_premium(app)
        app.refresh_from_db()
        
        self.stdout.write(f"\nUpdated Premiums:")
        self.stdout.write(f"  Annual: {app.annual_premium}")
        self.stdout.write(f"  6-Month: {app.six_month_premium}")
        self.stdout.write(f"  3-Month: {app.three_month_premium}")
        
        self.stdout.write(f"\nRegenerating contract PDF...")
        try:
            result = generate_contract_pdf(app)
            app.refresh_from_db()
            
            if isinstance(result, list):
                self.stdout.write(self.style.SUCCESS(f'Generated {len(result)} contract(s)'))
                for path in result:
                    self.stdout.write(f"  - {path}")
            else:
                self.stdout.write(self.style.SUCCESS(f'Contract generated: {result}'))
            
            self.stdout.write(f"\nContract PDF path: {app.contract_pdf_path}")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))
            import traceback
            traceback.print_exc()

