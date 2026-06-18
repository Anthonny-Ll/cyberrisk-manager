"""Vistas de evaluación de riesgos y matriz de riesgos."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.usuarios.decorators import analista_o_admin
from apps.auditoria.utils import registrar_log
from .models import Riesgo
from .forms import RiesgoForm


@login_required
def lista_riesgos(request):
    riesgos = Riesgo.objects.select_related('id_activo', 'id_amenaza', 'id_vulnerabilidad').all()
    nivel = request.GET.get('nivel', '')
    activo = request.GET.get('activo', '')
    departamento = request.GET.get('departamento', '')

    if nivel:
        riesgos = riesgos.filter(nivel_cualitativo=nivel)
    if activo:
        riesgos = riesgos.filter(id_activo__nombre__icontains=activo)
    if departamento:
        riesgos = riesgos.filter(id_activo__departamento__icontains=departamento)

    return render(request, 'riesgos/lista.html', {
        'riesgos': riesgos,
        'filtros': {'nivel': nivel, 'activo': activo, 'departamento': departamento},
    })


@login_required
@analista_o_admin
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
@analista_o_admin
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
@analista_o_admin
def cerrar_riesgo(request, pk):
    riesgo = get_object_or_404(Riesgo, pk=pk)
    if request.method == 'POST':
        riesgo.estado_riesgo = 'Cerrado'
        riesgo.save()
        registrar_log(request.user, 'editar', 'Riesgo', riesgo.pk, f'Riesgo cerrado: R-{riesgo.pk:03d}')
        messages.info(request, f'Riesgo R-{riesgo.pk:03d} cerrado.')
    return redirect('/riesgos/')
