import os
import zipfile
from datetime import date
from io import BytesIO

from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand
from main.models import InsuranceApplication


class Command(BaseCommand):
    help = "Export all contracts generated today into a ZIP file."

    def handle(self, *args, **kwargs):
        today = date.today()

        # Filter applications with contracts generated today
        applications = InsuranceApplication.objects.filter(
            contract_generated=True,
            updated_at__date=today
        )

        if not applications.exists():
            self.stdout.write(self.style.WARNING("No contracts generated today."))
            return

        zip_filename = f"contracts_export_{today}.zip"
        zip_buffer = BytesIO()

        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for app in applications:
                pdf_path = app.contract_pdf_path
                if pdf_path and default_storage.exists(pdf_path):
                    with default_storage.open(pdf_path, "rb") as pdf_file:
                        pdf_bytes = pdf_file.read()
                        file_name = f"{app.contract_number}.pdf"
                        zip_file.writestr(file_name, pdf_bytes)

        # Save the ZIP file in MEDIA_ROOT/exports/
        export_dir = "exports/contracts/"
        if not default_storage.exists(export_dir):
            default_storage.save(export_dir + "init.txt", ContentFile(""))

        final_zip_path = export_dir + zip_filename
        default_storage.save(final_zip_path, zip_buffer)

        self.stdout.write(self.style.SUCCESS(f"Contracts exported to: {final_zip_path}"))
