"""
URLs for user management
"""

from django.urls import path
from .views import superadmin_create_user, superadmin_users_list

app_name = 'accounts'

urlpatterns = [
    # ... existing URLs ...
    path('admin/users/', superadmin_users_list, name='users_list'),
    path('admin/create-user/', superadmin_create_user, name='create_user'),
]
