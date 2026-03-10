"""
Management command to create a superuser in MongoDB.
Usage: python manage.py createsuperuser_mongo
or: python manage.py createsuperuser_mongo --username admin --email admin@medisync.com --password securepass
"""

from django.core.management.base import BaseCommand, CommandError
from apps.accounts.models import User
from getpass import getpass
import sys


class Command(BaseCommand):
    help = 'Create a superuser in MongoDB'

    def add_arguments(self, parser):
        parser.add_argument('--username', help='Username for superuser')
        parser.add_argument('--email', help='Email for superuser')
        parser.add_argument('--password', help='Password for superuser')

    def handle(self, *args, **options):
        username = options.get('username')
        email = options.get('email')
        password = options.get('password')

        # Prompt for username if not provided
        if not username:
            username = input('Username: ').strip()
            if not username:
                raise CommandError('Username cannot be empty')

        # Check if user already exists (MongoEngine query)
        if User.objects(username=username):
            raise CommandError(f'User with username "{username}" already exists')

        # Prompt for email if not provided
        if not email:
            email = input('Email: ').strip()
            if not email:
                raise CommandError('Email cannot be empty')

        # Check if email already exists
        if User.objects(email=email):
            raise CommandError(f'User with email "{email}" already exists')

        # Prompt for password if not provided
        if not password:
            while True:
                password1 = getpass('Password: ')
                password2 = getpass('Password (again): ')
                if password1 != password2:
                    self.stdout.write(self.style.ERROR("Passwords don't match. Try again."))
                    continue
                if not password1:
                    self.stdout.write(self.style.ERROR("Password cannot be empty."))
                    continue
                password = password1
                break

        # Create superuser
        try:
            user = User(
                username=username,
                email=email,
                first_name='Super',
                last_name='Admin',
                is_superuser=True,
                is_staff=True,
                is_active=True,
                role='platform_admin'
            )
            user.set_password(password)
            user.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ Superuser "{username}" created successfully in MongoDB!'
                )
            )
            self.stdout.write(f'  Email: {email}')
            self.stdout.write(f'  Role: Platform Admin')

        except Exception as e:
            raise CommandError(f'Error creating superuser: {str(e)}')
