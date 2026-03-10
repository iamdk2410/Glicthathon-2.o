"""
MongoDB-based authentication backend for Django.
Allows Django to authenticate users stored in MongoDB using MongoEngine.
"""

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from mongoengine import DoesNotExist
import hashlib
import hmac

User = get_user_model()


class MongoEngineBackend(ModelBackend):
    """
    Authenticates against MongoDB User model using MongoEngine.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate user by username/email and password.
        """
        if username is None or password is None:
            return None

        try:
            # Try to find user by username or email
            try:
                user = User.objects.get(username=username)
            except DoesNotExist:
                user = User.objects.get(email=username)

            # Check password
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        except DoesNotExist:
            return None
        except Exception:
            return None

    def get_user(self, user_id):
        """
        Get user by ID.
        """
        try:
            return User.objects.get(id=user_id)
        except DoesNotExist:
            return None

    def user_can_authenticate(self, user):
        """
        Check if user is active.
        """
        return user.is_active
