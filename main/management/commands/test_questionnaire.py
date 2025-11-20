"""
Django management command to test questionnaire saving and retrieval
"""
from django.core.management.base import BaseCommand
from main.models import InsuranceApplication, Questionnaire
from django.utils import timezone
from datetime import date
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Test questionnaire saving and retrieval'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🧪 Testing Questionnaire Functionality...\n'))
        
        # Check existing questionnaires
        total_questionnaires = Questionnaire.objects.count()
        questionnaires_with_app = Questionnaire.objects.filter(application__isnull=False).count()
        questionnaires_without_app = Questionnaire.objects.filter(application__isnull=True).count()
        
        self.stdout.write(f'📊 Statistics:')
        self.stdout.write(f'  - Total Questionnaires: {total_questionnaires}')
        self.stdout.write(f'  - With Application: {questionnaires_with_app}')
        self.stdout.write(f'  - Without Application: {questionnaires_without_app}\n')
        
        # Check recent applications and their questionnaires
        recent_apps = InsuranceApplication.objects.order_by('-created_at')[:10]
        
        self.stdout.write(f'📋 Recent Applications (last 10):')
        for app in recent_apps:
            has_questionnaire = hasattr(app, 'questionnaire') and app.questionnaire is not None
            questionnaire_id = app.questionnaire.id if has_questionnaire else None
            
            status = '✅' if has_questionnaire else '❌'
            self.stdout.write(
                f'  {status} Application {app.application_number or app.contract_number} '
                f'(ID: {app.id}) - Questionnaire: {questionnaire_id or "NONE"}'
            )
            
            if has_questionnaire:
                q = app.questionnaire
                # Check if questionnaire has data
                has_data = (
                    q.is_healthy is not None or
                    q.program or
                    q.payment_frequency or
                    q.has_other_insured_pet or
                    q.has_been_denied_insurance
                )
                data_status = '📝 Has Data' if has_data else '⚠️ Empty'
                self.stdout.write(f'      {data_status}')
        
        # Test creating a questionnaire for an application without one
        apps_without_questionnaire = InsuranceApplication.objects.filter(questionnaire__isnull=True)[:5]
        
        if apps_without_questionnaire.exists():
            self.stdout.write(f'\n⚠️  Found {apps_without_questionnaire.count()} applications without questionnaire')
            self.stdout.write('   Creating empty questionnaires for them...')
            
            created_count = 0
            for app in apps_without_questionnaire:
                try:
                    questionnaire, created = Questionnaire.objects.get_or_create(application=app)
                    if created:
                        created_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'  ✅ Created questionnaire (ID: {questionnaire.id}) for application {app.application_number or app.contract_number}'
                            )
                        )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(
                            f'  ❌ Failed to create questionnaire for application {app.id}: {e}'
                        )
                    )
            
            if created_count > 0:
                self.stdout.write(
                    self.style.SUCCESS(f'\n✅ Successfully created {created_count} questionnaires')
                )
        else:
            self.stdout.write(self.style.SUCCESS('\n✅ All applications have questionnaires!'))
        
        # Final statistics
        final_total = Questionnaire.objects.count()
        final_with_app = Questionnaire.objects.filter(application__isnull=False).count()
        
        self.stdout.write(f'\n📊 Final Statistics:')
        self.stdout.write(f'  - Total Questionnaires: {final_total}')
        self.stdout.write(f'  - With Application: {final_with_app}')
        
        # Check for questionnaires with data
        questionnaires_with_data = Questionnaire.objects.filter(
            application__isnull=False
        ).exclude(
            is_healthy__isnull=True,
            program__isnull=True,
            payment_frequency__isnull=True
        ).count()
        
        self.stdout.write(f'  - With Data: {questionnaires_with_data}')
        
        self.stdout.write(self.style.SUCCESS('\n✅ Test completed!'))

