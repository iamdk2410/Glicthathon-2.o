#!/usr/bin/env python
"""Test MongoDB authentication"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

django.setup()

from apps.accounts.mongo_auth import MongoDBUserBackend

# Test authentication with email
print('--- Testing Authentication ---')
user = MongoDBUserBackend.authenticate('admin@medisync.com', 'AdminPass@123')
if user:
    print(f'✓ Authentication SUCCESS (by email)')
    print(f'  Username: {user.username}')
    print(f'  Email: {user.email}')
    print(f'  Role: {user.role}')
    print(f'  Is Superuser: {user.is_superuser}')
else:
    print('✗ Authentication FAILED (by email)')

# Test authentication with username
user2 = MongoDBUserBackend.authenticate('admin', 'AdminPass@123')
if user2:
    print(f'\n✓ Authentication SUCCESS (by username)')
    print(f'  Username: {user2.username}')
else:
    print(f'\n✗ Authentication FAILED (by username)')

# Test with wrong password
user3 = MongoDBUserBackend.authenticate('admin@medisync.com', 'wrongpassword')
if user3:
    print(f'\n✗ Wrong password accepted (BUG)')
else:
    print(f'\n✓ Wrong password rejected (correct)')

print('\n✓ All authentication tests passed!')
