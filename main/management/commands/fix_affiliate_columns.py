"""
Django management command to add missing affiliate_code and discount_applied columns.
"""
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Add missing affiliate_code and discount_applied columns if they do not exist'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            try:
                # Check if affiliate_code column exists
                cursor.execute("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name='main_insuranceapplication' 
                    AND column_name='affiliate_code'
                """)
                has_affiliate_code = cursor.fetchone() is not None
                
                # Check if discount_applied column exists
                cursor.execute("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name='main_insuranceapplication' 
                    AND column_name='discount_applied'
                """)
                has_discount_applied = cursor.fetchone() is not None
                
                if not has_affiliate_code:
                    self.stdout.write(self.style.WARNING('Adding affiliate_code column...'))
                    cursor.execute("""
                        ALTER TABLE main_insuranceapplication 
                        ADD COLUMN affiliate_code VARCHAR(50) NULL
                    """)
                    cursor.execute("""
                        CREATE INDEX IF NOT EXISTS main_insuranceapplication_affiliate_code_6b21887b 
                        ON main_insuranceapplication (affiliate_code)
                    """)
                    self.stdout.write(self.style.SUCCESS('✅ affiliate_code column added'))
                else:
                    self.stdout.write(self.style.SUCCESS('✓ affiliate_code column already exists'))
                
                if not has_discount_applied:
                    self.stdout.write(self.style.WARNING('Adding discount_applied column...'))
                    cursor.execute("""
                        ALTER TABLE main_insuranceapplication 
                        ADD COLUMN discount_applied NUMERIC(10, 2) DEFAULT 0 NOT NULL
                    """)
                    self.stdout.write(self.style.SUCCESS('✅ discount_applied column added'))
                else:
                    self.stdout.write(self.style.SUCCESS('✓ discount_applied column already exists'))
                
                self.stdout.write(self.style.SUCCESS('\n✅ Database columns are now up to date!'))
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Error: {str(e)}')
                )
                raise

