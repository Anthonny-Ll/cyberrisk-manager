"""Vistas CRUD para activos de información."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.auditoria.utils import registrar_log
from .models import Activo
from .forms import ActivoForm


@login_required
def lista_activos(request):
    activos = Activo.objects.select_related('propietario').all()
    # Filtros GET
    tipo = request.GET.get('tipo', '')
    departamento = request.GET.get('departamento', '')
    criticidad = request.GET.get('criticidad', '')
    estado = request.GET.get('estado', '')

    if tipo:
        activos = activos.filter(tipo=tipo)
    if departamento:
        activos = activos.filter(departamento__icontains=departamento)
    if criticidad:
        activos = activos.filter(nivel_criticidad=criticidad)
    if estado:
        activos = activos.filter(estado=estado)

    return render(request, 'activos/lista.html', {
        'activos': activos,
        'filtros': {'tipo': tipo, 'departamento': departamento, 'criticidad': criticidad, 'estado': estado},
    })


@login_required
def detalle_activo(request, pk):
    activo = get_object_or_404(Activo, pk=pk)
    return render(request, 'activos/detalle.html', {'activo': activo})


@login_required
def crear_activo(request):
    if request.method == 'POST':
        form = ActivoForm(request.POST)
        if form.is_valid():
            activo = form.save()
            registrar_log(request.user, 'crear', 'Activo', activo.pk, f'Activo creado: {activo.nombre}')
            messages.success(request, f'Activo "{activo.nombre}" registrado correctamente.')
            return redirect('/activos/')
        else:
            messages.error(request, 'Error al guardar. Revisa los campos marcados en rojo.')
    else:
        form = ActivoForm()
        
    departamentos = Activo.objects.exclude(departamento='').values_list('departamento', flat=True).distinct()
    return render(request, 'activos/form.html', {'form': form, 'titulo': 'Nuevo Activo', 'departamentos': departamentos})


@login_required
def editar_activo(request, pk):
    activo = get_object_or_404(Activo, pk=pk)
    if request.method == 'POST':
        form = ActivoForm(request.POST, instance=activo)
        if form.is_valid():
            form.save()
            registrar_log(request.user, 'editar', 'Activo', activo.pk, f'Activo editado: {activo.nombre}')
            messages.success(request, 'Activo actualizado correctamente.')
            return redirect('/activos/')
        else:
            messages.error(request, 'Error al guardar. Revisa los campos marcados en rojo.')
    else:
        form = ActivoForm(instance=activo)
        
    departamentos = Activo.objects.exclude(departamento='').values_list('departamento', flat=True).distinct()
    return render(request, 'activos/form.html', {'form': form, 'titulo': 'Editar Activo', 'objeto': activo, 'departamentos': departamentos})


@login_required
def desactivar_activo(request, pk):
    """RN-08: Desactivación lógica, no eliminación física."""
    activo = get_object_or_404(Activo, pk=pk)
    if request.method == 'POST':
        activo.estado = 'Inactivo'
        activo.save()
        registrar_log(request.user, 'desactivar', 'Activo', activo.pk, f'Activo desactivado: {activo.nombre}')
        messages.warning(request, f'Activo "{activo.nombre}" desactivado.')
    return redirect('/activos/')
