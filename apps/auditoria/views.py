"""Vista del log de auditoría (solo administrador)."""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.usuarios.decorators import solo_administrador
from .models import LogAuditoria


@login_required
@solo_administrador
def lista_auditoria(request):
    logs = LogAuditoria.objects.select_related('id_usuario').order_by('-fecha_hora')[:500]
    return render(request, 'auditoria/lista.html', {'logs': logs})
