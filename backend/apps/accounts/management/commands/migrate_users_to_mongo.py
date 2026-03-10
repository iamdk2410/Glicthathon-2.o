"""
Migration script to move users from SQLite3 to MongoDB.
Run this after installing MongoEngine to migrate existing users.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User as DjangoUser
from apps.accounts.models import User
from mongoengine import DoesNotExist


class Command(BaseCommand):
    help = 'Migrate users from Django SQLite to MongoDB'

    def handle(self, *args, **options):
        try:
            # Get all Django users from SQLite
            django_users = DjangoUser.objects.all()
            migrated_count = 0

            if not django_users.exists():
                self.stdout.write(self.style.WARNING('No users found in SQLite database'))
                return

            self.stdout.write(f'Found {django_users.count()} users to migrate...')

            for django_user in django_users:
                # Check if user already exists in MongoDB
                if User.objects(username=django_user.username):
                    self.stdout.write(
                        self.style.WARNING(
                            f'  ⊘ Skipping "{django_user.username}" (already exists in MongoDB)'
                        )
                    )
                    continue

                try:
                    # Create MongoDB user with same data
                    mongo_user = User(
                        username=django_user.username,
                        email=django_user.email,
                        first_name=django_user.first_name,
                        last_name=django_user.last_name,
                        password=django_user.password,  # Hash is compatible
                        is_superuser=django_user.is_superuser,
                        is_staff=django_user.is_staff,
                        is_active=django_user.is_active,
                        date_joined=django_user.date_joined,
                        last_login=django_user.last_login,
                    )

                    # Try to get role from original User model if it exists
                    try:
                        original_user = django_user.accounts_user
                        mongo_user.role = original_user.role
                    except:
                        mongo_user.role = 'platform_admin' if django_user.is_superuser else 'doctor'

                    mongo_user.save()
                    migrated_count += 1

                    status = '✓ SUPERUSER' if django_user.is_superuser else '✓ User'
                    self.stdout.write(
                        self.style.SUCCESS(f'  {status}: {django_user.username}')
                    )

                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(
                            f'  ✗ Error migrating "{django_user.username}": {str(e)}'
                        )
                    )

            self.stdout.write(
                self.style.SUCCESS(
                    f'\n✓ Successfully migrated {migrated_count} users to MongoDB!'
                )
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Migration failed: {str(e)}')
            )
