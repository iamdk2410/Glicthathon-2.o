"""
User management views for superadmin.
Allows creating users through web interface.
"""

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from apps.accounts.models import User
from apps.accounts.decorators import mongo_admin_required


@mongo_admin_required
@require_http_methods(["GET", "POST"])
def superadmin_create_user(request):
    """
    Create a new user through web interface.
    Only accessible to superadmin/platform_admin users.
    """
    if request.method == "GET":
        ctx = {
            'roles': User.ROLE_CHOICES
        }
        return render(request, 'admin/create_user.html', ctx)

    # POST - Create user
    username = request.POST.get('username', '').strip()
    email = request.POST.get('email', '').strip()
    password = request.POST.get('password', '').strip()
    confirm_password = request.POST.get('confirm_password', '').strip()
    role = request.POST.get('role', 'doctor').strip()
    first_name = request.POST.get('first_name', '').strip()
    last_name = request.POST.get('last_name', '').strip()

    # Validation
    errors = []

    if not username:
        errors.append("Username is required")
    elif len(username) < 3:
        errors.append("Username must be at least 3 characters")
    elif User.objects(username=username):
        errors.append("Username already exists")

    if not email:
        errors.append("Email is required")
    elif '@' not in email:
        errors.append("Invalid email format")
    elif User.objects(email=email):
        errors.append("Email already exists")

    if not password:
        errors.append("Password is required")
    elif len(password) < 8:
        errors.append("Password must be at least 8 characters")

    if password != confirm_password:
        errors.append("Passwords don't match")

    if errors:
        return JsonResponse({
            'status': 'error',
            'errors': errors
        }, status=400)

    # Create user
    try:
        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            role=role,
            is_active=True,
        )
        user.set_password(password)
        user.save()

        return JsonResponse({
            'status': 'success',
            'message': f'✓ User "{username}" created successfully!',
            'user': {
                'username': user.username,
                'email': user.email,
                'role': user.role
            }
        })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'errors': [f'Error creating user: {str(e)}']
        }, status=500)


@mongo_admin_required
def superadmin_users_list(request):
    """
    List all users. Only accessible to superadmin.
    """
    try:
        users = User.objects()
        users_data = [
            {
                'username': u.username,
                'email': u.email,
                'first_name': u.first_name,
                'last_name': u.last_name,
                'role': u.role,
                'is_superuser': u.is_superuser,
                'is_active': u.is_active,
                'date_joined': u.date_joined.strftime('%Y-%m-%d %H:%M') if u.date_joined else 'N/A'
            }
            for u in users
        ]

        return render(request, 'admin/users_list.html', {
            'users': users_data,
            'total_users': len(users_data)
        })

    except Exception as e:
        return JsonResponse({
            'error': f'Error fetching users: {str(e)}'
        }, status=500)
