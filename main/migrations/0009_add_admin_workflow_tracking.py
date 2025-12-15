# Generated manually for admin workflow tracking

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0008_insuranceapplication_approved_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='insuranceapplication',
            name='assigned_to',
            field=models.ForeignKey(blank=True, help_text='Admin currently working on this application', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_applications', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='insuranceapplication',
            name='section_admin_approved',
            field=models.BooleanField(default=False, help_text='Διοικητικά Στοιχεία - Εγκρίθηκε'),
        ),
        migrations.AddField(
            model_name='insuranceapplication',
            name='section_admin_rejected',
            field=models.BooleanField(default=False, help_text='Διοικητικά Στοιχεία - Απορρίφθηκε'),
        ),
        migrations.AddField(
            model_name='insuranceapplication',
            name='section_affiliate_approved',
            field=models.BooleanField(default=False, help_text='Κωδικός Συνεργάτη - Εγκρίθηκε'),
        ),
        migrations.AddField(
            model_name='insuranceapplication',
            name='section_affiliate_rejected',
            field=models.BooleanField(default=False, help_text='Κωδικός Συνεργάτη - Απορρίφθηκε'),
        ),
        migrations.AddField(
            model_name='insuranceapplication',
            name='section_customer_approved',
            field=models.BooleanField(default=False, help_text='Στοιχεία Πελάτη - Εγκρίθηκε'),
        ),
        migrations.AddField(
            model_name='insuranceapplication',
            name='section_customer_rejected',
            field=models.BooleanField(default=False, help_text='Στοιχεία Πελάτη - Απορρίφθηκε'),
        ),
        migrations.AddField(
            model_name='insuranceapplication',
            name='section_dates_approved',
            field=models.BooleanField(default=False, help_text='Ημερομηνίες - Εγκρίθηκε'),
        ),
        migrations.AddField(
            model_name='insuranceapplication',
            name='section_dates_rejected',
            field=models.BooleanField(default=False, help_text='Ημερομηνίες - Απορρίφθηκε'),
        ),
        migrations.AddField(
            model_name='insuranceapplication',
            name='section_insurance_approved',
            field=models.BooleanField(default=False, help_text='Στοιχεία Ασφάλισης - Εγκρίθηκε'),
        ),
        migrations.AddField(
            model_name='insuranceapplication',
            name='section_insurance_rejected',
            field=models.BooleanField(default=False, help_text='Στοιχεία Ασφάλισης - Απορρίφθηκε'),
        ),
        migrations.AddField(
            model_name='insuranceapplication',
            name='section_pet1_approved',
            field=models.BooleanField(default=False, help_text='Στοιχεία 1ου Κατοικιδίου - Εγκρίθηκε'),
        ),
        migrations.AddField(
            model_name='insuranceapplication',
            name='section_pet1_rejected',
            field=models.BooleanField(default=False, help_text='Στοιχεία 1ου Κατοικιδίου - Απορρίφθηκε'),
        ),
        migrations.AddField(
            model_name='insuranceapplication',
            name='section_pet2_approved',
            field=models.BooleanField(default=False, help_text='Στοιχεία 2ου Κατοικιδίου - Εγκρίθηκε'),
        ),
        migrations.AddField(
            model_name='insuranceapplication',
            name='section_pet2_rejected',
            field=models.BooleanField(default=False, help_text='Στοιχεία 2ου Κατοικιδίου - Απορρίφθηκε'),
        ),
        migrations.AddField(
            model_name='insuranceapplication',
            name='section_questionnaire_approved',
            field=models.BooleanField(default=False, help_text='Ερωτηματολόγιο - Εγκρίθηκε'),
        ),
        migrations.AddField(
            model_name='insuranceapplication',
            name='section_questionnaire_rejected',
            field=models.BooleanField(default=False, help_text='Ερωτηματολόγιο - Απορρίφθηκε'),
        ),
    ]

