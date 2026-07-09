from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.auditoria.utils import registrar_log
from .models import Vulnerabilidad
from .forms import VulnerabilidadForm


@login_required
def lista_vulnerabilidades(request):
    vulns = Vulnerabilidad.objects.select_related('id_activo').all()
    severidad = request.GET.get('severidad', '')
    estado = request.GET.get('estado', '')
    if severidad:
        vulns = vulns.filter(severidad=severidad)
    if estado:
        vulns = vulns.filter(estado=estado)
    return render(request, 'vulnerabilidades/lista.html', {
        'vulnerabilidades': vulns,
        'filtros': {'severidad': severidad, 'estado': estado},
    })


@login_required
@login_required
def crear_vulnerabilidad(request):
    if request.method == 'POST':
        form = VulnerabilidadForm(request.POST)
        if form.is_valid():
            vuln = form.save()
            registrar_log(request.user, 'crear', 'Vulnerabilidad', vuln.pk, f'Vulnerabilidad creada: {vuln.nombre}')
            messages.success(request, f'Vulnerabilidad "{vuln.nombre}" registrada.')
            return redirect('/vulnerabilidades/')
    else:
        form = VulnerabilidadForm()
    return render(request, 'vulnerabilidades/form.html', {'form': form, 'titulo': 'Nueva Vulnerabilidad'})


@login_required
@login_required
def editar_vulnerabilidad(request, pk):
    vuln = get_object_or_404(Vulnerabilidad, pk=pk)
    if request.method == 'POST':
        form = VulnerabilidadForm(request.POST, instance=vuln)
        if form.is_valid():
            form.save()
            registrar_log(request.user, 'editar', 'Vulnerabilidad', vuln.pk, f'Vulnerabilidad editada: {vuln.nombre}')
            messages.success(request, 'Vulnerabilidad actualizada.')
            return redirect('/vulnerabilidades/')
    else:
        form = VulnerabilidadForm(instance=vuln)
    return render(request, 'vulnerabilidades/form.html', {'form': form, 'titulo': 'Editar Vulnerabilidad', 'objeto': vuln})


@login_required
@login_required
def desactivar_vulnerabilidad(request, pk):
    vuln = get_object_or_404(Vulnerabilidad, pk=pk)
    if request.method == 'POST':
        vuln.estado = 'Resuelta'
        vuln.save()
        registrar_log(request.user, 'desactivar', 'Vulnerabilidad', vuln.pk, f'Vulnerabilidad resuelta: {vuln.nombre}')
        messages.warning(request, f'Vulnerabilidad "{vuln.nombre}" marcada como resuelta.')
    return redirect('/vulnerabilidades/')
