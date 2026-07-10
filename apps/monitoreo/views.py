"""Panel de monitoreo y alertas del sistema."""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from apps.riesgos.models import Riesgo
from apps.tratamiento.models import Tratamiento
from apps.residual.models import RiesgoResidual
from apps.activos.models import Activo
from apps.vulnerabilidades.models import Vulnerabilidad


@login_required
def panel_monitoreo(request):
    hoy = timezone.now().date()

    # Alertas rojas: riesgos críticos sin tratamiento
    criticos_sin_trat = Riesgo.objects.filter(
        nivel_cualitativo='Crítico',
        tratamiento__isnull=True
    ).select_related('id_activo')

    # Alertas naranja: controles vencidos
    controles_vencidos = Tratamiento.objects.filter(
        fecha_objetivo__lt=hoy,
        estado_control__in=['Pendiente', 'En progreso']
    ).select_related('id_riesgo')

    # Alertas amarillas: residuales sin aceptación
    residuales_pendientes = RiesgoResidual.objects.filter(
        aceptacion='Pendiente'
    ).select_related('id_riesgo', 'id_riesgo__id_activo')

    # Estadísticas de seguimiento
    total_controles = Tratamiento.objects.count()
    implementados = Tratamiento.objects.filter(estado_control='Implementado').count()
    pct_implementados = round((implementados / total_controles * 100) if total_controles > 0 else 0)

    vulns_abiertas = Vulnerabilidad.objects.filter(estado='Identificada').count()
    vulns_en_trat = Vulnerabilidad.objects.filter(estado='En tratamiento').count()
    vulns_resueltas = Vulnerabilidad.objects.filter(estado='Resuelta').count()

    return render(request, 'monitoreo/index.html', {
        'criticos_sin_trat': criticos_sin_trat,
        'controles_vencidos': controles_vencidos,
        'residuales_pendientes': residuales_pendientes,
        'total_controles': total_controles,
        'implementados': implementados,
        'pct_implementados': pct_implementados,
        'vulns_abiertas': vulns_abiertas,
        'vulns_en_trat': vulns_en_trat,
        'vulns_resueltas': vulns_resueltas,
        'hoy': hoy,
    })
