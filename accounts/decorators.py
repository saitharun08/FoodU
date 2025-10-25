from django.shortcuts import redirect
from functools import wraps

def role_required(allowed_roles=None):
    if allowed_roles is None:
        allowed_roles = []

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('mobile_login')
            if request.user.role not in allowed_roles:
                # unauthorized redirect
                return redirect('/unauthorized/')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
