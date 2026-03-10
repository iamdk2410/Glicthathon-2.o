from mongoengine import Document, StringField, BooleanField, DateTimeField
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime


class User(Document):
    """
    MongoDB-based User model for MediSync.
    Complete MongoDB-based authentication (no SQLite).
    """

    ROLE_CHOICES = [
        ('doctor', 'Doctor'),
        ('technician', 'Lab Technician'),
        ('hospital_admin', 'Hospital Admin'),
        ('platform_admin', 'Platform Admin'),
    ]

    # Authentication fields
    username = StringField(unique=True, required=True)
    email = StringField(unique=True, required=True)
    password = StringField(required=True)

    # User info fields
    first_name = StringField(default='')
    last_name = StringField(default='')

    # Role and permissions
    role = StringField(choices=ROLE_CHOICES, default='doctor')
    is_superuser = BooleanField(default=False)
    is_staff = BooleanField(default=False)
    is_active = BooleanField(default=True)

    # Timestamps
    date_joined = DateTimeField(default=datetime.utcnow)
    last_login = DateTimeField()

    # Organization reference
    organization_id = StringField()

    meta = {
        'collection': 'users',
        'indexes': ['username', 'email']
    }

    def set_password(self, raw_password):
        """Hash and set password."""
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """Check if provided password matches hashed password."""
        return check_password(raw_password, self.password)

    def get_full_name(self):
        """Return user's full name."""
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        """Return user's first name."""
        return self.first_name

    def get_role_display(self):
        """Return display name for role."""
        role_dict = dict(self.ROLE_CHOICES)
        return role_dict.get(self.role, self.role)

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
