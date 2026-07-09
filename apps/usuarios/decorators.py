"""Decoradores de control de acceso por rol."""
from functools import wraps
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied


def rol_requerido(*roles):
    """Restringe acceso a usuarios con uno de los roles especificados."""
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('/login/')
            if request.user.rol not in roles and not request.user.is_superuser:
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator


def solo_administrador(view_func):
    return rol_requerido('administrador')(view_func)
