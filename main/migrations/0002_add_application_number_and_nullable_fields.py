# Generated manually for application_number and nullable field updates

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        # Add application_number field
        migrations.AddField(
            model_name='insuranceapplication',
            name='application_number',
            field=models.CharField(blank=True, help_text='Application number like HPI10001', max_length=20, null=True, unique=True),
        ),
        # Add submission_date field with default for existing rows
        migrations.AddField(
            model_name='insuranceapplication',
            name='submission_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
        ),
        # Note: PaymentTransaction fields will be handled when that model is created
        # If PaymentTransaction already exists, uncomment these:
        # migrations.AlterField(
        #     model_name='paymenttransaction',
        #     name='order_code',
        #     field=models.CharField(blank=True, db_index=True, max_length=100, null=True, unique=True),
        # ),
        # migrations.AlterField(
        #     model_name='paymenttransaction',
        #     name='amount',
        #     field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        # ),
        # migrations.AlterField(
        #     model_name='paymenttransaction',
        #     name='payment_method',
        #     field=models.CharField(blank=True, default='viva_wallet', max_length=50),
        # ),
    ]

