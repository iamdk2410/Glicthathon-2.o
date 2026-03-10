"""
Custom authentication for MongoDB users with Django sessions.
"""

import json
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password
from mongoengine import DoesNotExist
from apps.accounts.models import User


class MongoDBUserBackend:
    """
    Custom backend for authenticating MongoEngine User documents.
    Used with Django sessions but bypasses Django's User model system.
    """

    @staticmethod
    def authenticate(username, password):
        """
        Authenticate user by username/email and password.
        Returns User document if authenticated, None otherwise.
        """
        try:
            # Try to find user by username or email
            try:
                user = User.objects(username=username).first()
            except:
                user = User.objects(email=username).first()

            # Check if user exists and password is correct
            if user and user.check_password(password) and user.is_active:
                return user
        except Exception as e:
            print(f"Authentication error: {e}")
            return None

    @staticmethod
    def get_user(user_id):
        """
        Get user by MongoDB ObjectId.
        """
        try:
            return User.objects(id=user_id).first()
        except DoesNotExist:
            return None
        except Exception as e:
            print(f"Error getting user: {e}")
            return None


def serialize_user(user):
    """
    Serialize a User document to JSON for session storage.
    """
    if not user:
        return None
    return {
        'id': str(user.id),
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'is_superuser': user.is_superuser,
        'is_staff': user.is_staff,
        'is_active': user.is_active,
        'role': user.role,
    }


def deserialize_user(user_dict):
    """
    Deserialize user dict from session storage back to User document.
    """
    if not user_dict:
        return None
    try:
        return User.objects(id=user_dict['id']).first()
    except Exception:
        return None
