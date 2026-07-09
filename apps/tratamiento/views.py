from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from apps.auditoria.utils import registrar_log
from .models import Tratamiento
from .forms import TratamientoForm


@login_required
def lista_tratamientos(request):
    tratamientos = Tratamiento.objects.select_related('id_riesgo').all()
    estado = request.GET.get('estado', '')
    tipo = request.GET.get('tipo', '')
    if estado:
        tratamientos = tratamientos.filter(estado_control=estado)
    if tipo:
        tratamientos = tratamientos.filter(tipo_control=tipo)
    return render(request, 'tratamiento/lista.html', {
        'tratamientos': tratamientos,
        'filtros': {'estado': estado, 'tipo': tipo},
    })


@login_required
@login_required
def crear_tratamiento(request):
    if request.method == 'POST':
        form = TratamientoForm(request.POST)
        if form.is_valid():
            trat = form.save(commit=False)
            if not trat.fecha_planificacion:
                trat.fecha_planificacion = timezone.now().date()
            trat.save()
            # Actualizar estado del riesgo a "En tratamiento"
            riesgo = trat.id_riesgo
            if riesgo.estado_riesgo == 'Evaluado':
                riesgo.estado_riesgo = 'En tratamiento'
                riesgo.save()
            registrar_log(request.user, 'crear', 'Tratamiento', trat.pk, f'Tratamiento creado: {trat.nombre_control}')
            messages.success(request, f'Tratamiento "{trat.nombre_control}" registrado.')
            return redirect('/tratamiento/')
    else:
        form = TratamientoForm()
    return render(request, 'tratamiento/form.html', {'form': form, 'titulo': 'Nuevo Tratamiento'})


@login_required
@login_required
def editar_tratamiento(request, pk):
    trat = get_object_or_404(Tratamiento, pk=pk)
    if request.method == 'POST':
        estado_anterior = trat.estado_control
        form = TratamientoForm(request.POST, instance=trat)
        if form.is_valid():
            trat = form.save(commit=False)
            hoy = timezone.now().date()
            # Auto-registro de fechas según transición de estado
            if estado_anterior != 'En progreso' and trat.estado_control == 'En progreso' and not trat.fecha_inicio_ejecucion:
                trat.fecha_inicio_ejecucion = hoy
            if estado_anterior != 'Implementado' and trat.estado_control == 'Implementado' and not trat.fecha_finalizacion:
                trat.fecha_finalizacion = hoy
            trat.save()
            registrar_log(request.user, 'editar', 'Tratamiento', trat.pk, f'Tratamiento editado: {trat.nombre_control}')
            messages.success(request, 'Tratamiento actualizado.')
            return redirect('/tratamiento/')
    else:
        form = TratamientoForm(instance=trat)
    return render(request, 'tratamiento/form.html', {'form': form, 'titulo': 'Editar Tratamiento', 'objeto': trat})
