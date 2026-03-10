"""
Django admin configuration for accounts app.
MongoEngine User model is not registered with Django admin.
Use management commands (createsuperuser_mongo, manage_users_mongo) instead.
"""

from django.contrib import admin

# Don't register User model - it's a MongoEngine document, not a Django model
