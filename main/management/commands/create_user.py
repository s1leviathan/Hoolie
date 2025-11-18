"""
Django management command to create a user account.
Usage: python manage.py create_user --username <username> --email <email> --password <password> [--superuser]
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()


class Command(BaseCommand):
    help = 'Create a user account (regular or superuser)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            required=True,
            help='Username for the new user'
        )
        parser.add_argument(
            '--email',
            type=str,
            required=True,
            help='Email address for the new user'
        )
        parser.add_argument(
            '--password',
            type=str,
            required=True,
            help='Password for the new user'
        )
        parser.add_argument(
            '--superuser',
            action='store_true',
            help='Create a superuser account (admin access)'
        )

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']
        is_superuser = options['superuser']

        try:
            # Check if user already exists
            if User.objects.filter(username=username).exists():
                self.stdout.write(
                    self.style.WARNING(f'User "{username}" already exists.')
                )
                return

            if User.objects.filter(email=email).exists():
                self.stdout.write(
                    self.style.WARNING(f'User with email "{email}" already exists.')
                )
                return

            # Create the user
            if is_superuser:
                user = User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password
                )
                user_type = 'superuser'
            else:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
                user_type = 'user'

            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created {user_type} account:\n'
                    f'  Username: {user.username}\n'
                    f'  Email: {user.email}\n'
                    f'  Is Superuser: {user.is_superuser}\n'
                    f'  Is Staff: {user.is_staff}'
                )
            )

        except IntegrityError as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating user: {str(e)}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Unexpected error: {str(e)}')
            )

