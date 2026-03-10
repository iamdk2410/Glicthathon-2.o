"""
Custom decorators for MongoDB user authentication.
"""

from functools import wraps
from django.shortcuts import redirect
from apps.accounts.models import User


def mongo_login_required(view_func):
    """
    Decorator to require MongoDB user login.
    Stores user object on request as request.user_obj.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('accounts:login')
        
        try:
            user = User.objects(id=user_id).first()
            if not user or not user.is_active:
                # Clear invalid session
                if 'user_id' in request.session:
                    del request.session['user_id']
                return redirect('accounts:login')
            
            # Attach user to request for use in view
            request.user_obj = user
            return view_func(request, *args, **kwargs)
        except Exception as e:
            print(f"Error in mongo_login_required: {e}")
            return redirect('accounts:login')
    
    return wrapper


def mongo_admin_required(view_func):
    """
    Decorator to require MongoDB admin/superuser login.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('accounts:login')
        
        try:
            user = User.objects(id=user_id).first()
            if not user or not (user.is_superuser or user.role == 'platform_admin'):
                return redirect('accounts:login')
            
            request.user_obj = user
            return view_func(request, *args, **kwargs)
        except Exception:
            return redirect('accounts:login')
    
    return wrapper
