"""Vistas de evaluación de riesgos y matriz de riesgos."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.auditoria.utils import registrar_log
from django.http import JsonResponse
from apps.amenazas.models import ActivoAmenaza
from apps.vulnerabilidades.models import Vulnerabilidad
from .models import Riesgo
from .forms import RiesgoForm


@login_required
def lista_riesgos(request):
    riesgos = Riesgo.objects.select_related('id_activo', 'id_amenaza', 'id_vulnerabilidad').all()
    nivel = request.GET.get('nivel', '')
    activo = request.GET.get('activo', '')
    departamento = request.GET.get('departamento', '')
    probabilidad = request.GET.get('probabilidad', '')
    impacto = request.GET.get('impacto', '')

    if nivel:
        riesgos = riesgos.filter(nivel_cualitativo=nivel)
    if activo:
        riesgos = riesgos.filter(id_activo__nombre__icontains=activo)
    if departamento:
        riesgos = riesgos.filter(id_activo__departamento__icontains=departamento)
    if probabilidad:
        riesgos = riesgos.filter(probabilidad=probabilidad)
    if impacto:
        riesgos = riesgos.filter(impacto=impacto)

    return render(request, 'riesgos/lista.html', {
        'riesgos': riesgos,
        'filtros': {'nivel': nivel, 'activo': activo, 'departamento': departamento,
                    'probabilidad': probabilidad, 'impacto': impacto},
    })


@login_required
@login_required
def crear_riesgo(request):
    if request.method == 'POST':
        form = RiesgoForm(request.POST)
        if form.is_valid():
            riesgo = form.save(commit=False)
            riesgo.id_usuario_registra = request.user
            riesgo.save()
            registrar_log(request.user, 'crear', 'Riesgo', riesgo.pk,
                         f'Riesgo creado: {riesgo.id_activo.nombre} — {riesgo.nivel_cualitativo}')
            messages.success(request, f'Riesgo registrado. Nivel: {riesgo.nivel_cualitativo} ({riesgo.riesgo_inherente})')
            return redirect('/riesgos/')
    else:
        form = RiesgoForm()
    return render(request, 'riesgos/form.html', {'form': form, 'titulo': 'Nueva Evaluación de Riesgo'})


@login_required
@login_required
def editar_riesgo(request, pk):
    riesgo = get_object_or_404(Riesgo, pk=pk)
    if request.method == 'POST':
        form = RiesgoForm(request.POST, instance=riesgo)
        if form.is_valid():
            form.save()
            registrar_log(request.user, 'editar', 'Riesgo', riesgo.pk, f'Riesgo editado: R-{riesgo.pk:03d}')
            messages.success(request, 'Evaluación de riesgo actualizada.')
            return redirect('/riesgos/')
    else:
        form = RiesgoForm(instance=riesgo)
    return render(request, 'riesgos/form.html', {'form': form, 'titulo': 'Editar Evaluación de Riesgo', 'objeto': riesgo})


@login_required
def detalle_riesgo(request, pk):
    """Vista consolidada: Activo -> Amenaza -> Vulnerabilidad -> Tratamiento -> Residual."""
    riesgo = get_object_or_404(
        Riesgo.objects.select_related('id_activo', 'id_amenaza', 'id_vulnerabilidad', 'id_usuario_registra'),
        pk=pk
    )
    tratamientos = riesgo.tratamiento.select_related('control_iso').all()
    residual = getattr(riesgo, 'residual', None)
    return render(request, 'riesgos/detalle.html', {
        'riesgo': riesgo,
        'tratamientos': tratamientos,
        'residual': residual,
    })


@login_required
def matriz_riesgos(request):
    """Genera la matriz de riesgos 4×4 con conteo por celda."""
    riesgos = Riesgo.objects.all()

    # Construir matriz [probabilidad][impacto] → lista de riesgos
    matriz = {}
    for p in range(1, 5):
        matriz[p] = {}
        for i in range(1, 5):
            riesgos_celda = riesgos.filter(probabilidad=p, impacto=i)
            valor = p * i
            if valor <= 4:
                nivel = 'Bajo'
                color = 'verde'
            elif valor <= 8:
                nivel = 'Medio'
                color = 'amarillo'
            elif valor <= 12:
                nivel = 'Alto'
                color = 'naranja'
            else:
                nivel = 'Crítico'
                color = 'rojo'
            matriz[p][i] = {
                'valor': valor,
                'nivel': nivel,
                'color': color,
                'riesgos': list(riesgos_celda),
                'count': riesgos_celda.count(),
            }

    return render(request, 'riesgos/matriz.html', {'matriz': matriz, 'rango': range(1, 5)})


@login_required
@login_required
def cerrar_riesgo(request, pk):
    riesgo = get_object_or_404(Riesgo, pk=pk)
    if request.method == 'POST':
        riesgo.estado_riesgo = 'Cerrado'
        riesgo.save()
        registrar_log(request.user, 'editar', 'Riesgo', riesgo.pk, f'Riesgo cerrado: R-{riesgo.pk:03d}')
        messages.info(request, f'Riesgo R-{riesgo.pk:03d} cerrado.')
    return redirect('/riesgos/')


@login_required
def api_datos_activo(request, activo_id):
    """Devuelve JSON con amenazas y vulnerabilidades de un activo."""
    # Amenazas (a través de ActivoAmenaza)
    amenazas_qs = ActivoAmenaza.objects.filter(id_activo_id=activo_id).select_related('id_amenaza')
    amenazas = [{'id': a.id_amenaza.id, 'nombre': a.id_amenaza.nombre} for a in amenazas_qs]
    
    # Vulnerabilidades (directas al activo)
    vulns_qs = Vulnerabilidad.objects.filter(id_activo_id=activo_id)
    vulnerabilidades = [{'id': v.id, 'nombre': v.nombre} for v in vulns_qs]
    
    return JsonResponse({
        'amenazas': amenazas,
        'vulnerabilidades': vulnerabilidades
    })

@login_required
def api_asesor_ia(request):
    """
    Simulador Heurístico de IA.
    Para garantizar que la presentación no falle por problemas de red o cuotas de API,
    esta función genera un análisis simulado idéntico al que entregaría Gemini,
    basado en los datos reales actuales de la base de datos.
    """
    import time
    
    # Obtener riesgos altos y críticos sin tratamiento implementado
    riesgos_criticos = Riesgo.objects.filter(
        nivel_cualitativo__in=['Alto', 'Crítico']
    ).exclude(estado_riesgo='Cerrado').select_related('id_activo')
    
    total_criticos = riesgos_criticos.filter(nivel_cualitativo='Crítico').count()
    total_altos = riesgos_criticos.filter(nivel_cualitativo='Alto').count()
    
    if total_criticos == 0 and total_altos == 0:
        markdown_resp = "### 🛡️ Análisis de IA\n\n**¡Felicidades!** No he detectado riesgos con nivel **Alto** o **Crítico** abiertos en tu sistema en este momento. La organización mantiene un perfil de riesgo saludable.\n\n_Recomendación:_ Continúa el monitoreo periódico y revisa los riesgos de nivel Medio."
    else:
        markdown_resp = f"### 📊 Análisis del Panorama Actual\n\nHe escaneado el inventario y detectado **{total_criticos} riesgos CRÍTICOS** y **{total_altos} riesgos ALTOS** que requieren atención inmediata.\n\n"
        markdown_resp += "### 💡 Recomendaciones Prioritarias (ISO/IEC 27002:2022)\n\n"
        
        for idx, r in enumerate(riesgos_criticos[:3]): # Top 3
            markdown_resp += f"**{idx+1}. R-{r.pk:03d}: {r.id_vulnerabilidad.nombre}**\n"
            markdown_resp += f"- **Activo Afectado:** {r.id_activo.nombre} (Criticidad: {r.id_activo.nivel_criticidad})\n"
            
            # Sugerencias heurísticas basadas en palabras clave
            vuln_nombre = r.id_vulnerabilidad.nombre.lower()
            if 'contraseña' in vuln_nombre or 'acceso' in vuln_nombre or 'mfa' in vuln_nombre:
                markdown_resp += "- **Control Recomendado:** `A.5.17` (Información de autenticación) o `A.8.5` (Autenticación segura).\n"
                markdown_resp += "- **Acción:** Implementar MFA obligatorio y políticas de contraseñas robustas (12+ caracteres).\n\n"
            elif 'parche' in vuln_nombre or 'cve' in vuln_nombre or 'desactualizado' in vuln_nombre:
                markdown_resp += "- **Control Recomendado:** `A.8.8` (Gestión de vulnerabilidades técnicas).\n"
                markdown_resp += "- **Acción:** Aplicar parches de seguridad críticos en la ventana de mantenimiento más próxima.\n\n"
            elif 'red' in vuln_nombre or 'segmentación' in vuln_nombre or 'firewall' in vuln_nombre:
                markdown_resp += "- **Control Recomendado:** `A.8.22` (Segregación de redes).\n"
                markdown_resp += "- **Acción:** Configurar VLANs para aislar el tráfico corporativo del tráfico de invitados.\n\n"
            else:
                markdown_resp += "- **Control Recomendado:** Revisar controles de la sección `A.8` (Tecnológicos).\n"
                markdown_resp += "- **Acción:** Mitigar la vulnerabilidad según las políticas internas.\n\n"
                
        markdown_resp += "### 📝 Resumen Ejecutivo para la Alta Dirección\n\n"
        markdown_resp += "> \"El nivel de riesgo global actual exige acción proactiva. Si no se tratan las vulnerabilidades críticas mencionadas, la organización se expone a interrupciones operativas severas y posibles multas normativas (ej: LOPDP). Se aconseja priorizar los parches de seguridad y los controles de acceso.\""
    
    # Simulamos un pequeño retraso para efecto IA
    time.sleep(1.5)
    
    return JsonResponse({
        'analisis': markdown_resp
    })
