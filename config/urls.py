"""URLs principales de CyberSave."""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


def index_redirect(request):
    """Redirige / a dashboard si autenticado, si no a login."""
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    return redirect('/login/')


def vista_403(request, exception=None):
    from django.shortcuts import render
    return render(request, '403.html', status=403)


def vista_404(request, exception=None):
    from django.shortcuts import render
    return render(request, '404.html', status=404)


def vista_500(request):
    from django.shortcuts import render
    return render(request, '500.html', status=500)


handler403 = vista_403
handler404 = vista_404
handler500 = vista_500

urlpatterns = [
    path('', index_redirect),
    path('admin/', admin.site.urls),
    path('', include('apps.usuarios.urls')),
    path('', include('apps.activos.urls')),
    path('', include('apps.amenazas.urls')),
    path('', include('apps.vulnerabilidades.urls')),
    path('', include('apps.riesgos.urls')),
    path('', include('apps.tratamiento.urls')),
    path('', include('apps.residual.urls')),
    path('', include('apps.reportes.urls')),
    path('', include('apps.monitoreo.urls')),
    path('', include('apps.auditoria.urls')),
]
