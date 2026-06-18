from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.usuarios.decorators import analista_o_admin
from apps.auditoria.utils import registrar_log
from .models import Amenaza
from .forms import AmenazaForm


@login_required
def lista_amenazas(request):
    amenazas = Amenaza.objects.all()
    tipo = request.GET.get('tipo', '')
    fuente = request.GET.get('fuente', '')
    if tipo:
        amenazas = amenazas.filter(tipo_amenaza=tipo)
    if fuente:
        amenazas = amenazas.filter(fuente_amenaza=fuente)
    return render(request, 'amenazas/lista.html', {'amenazas': amenazas, 'filtros': {'tipo': tipo, 'fuente': fuente}})


@login_required
@analista_o_admin
def crear_amenaza(request):
    if request.method == 'POST':
        form = AmenazaForm(request.POST)
        if form.is_valid():
            amenaza = form.save()
            registrar_log(request.user, 'crear', 'Amenaza', amenaza.pk, f'Amenaza creada: {amenaza.nombre}')
            messages.success(request, f'Amenaza "{amenaza.nombre}" registrada.')
            return redirect('/amenazas/')
    else:
        form = AmenazaForm()
    return render(request, 'amenazas/form.html', {'form': form, 'titulo': 'Nueva Amenaza'})


@login_required
@analista_o_admin
def editar_amenaza(request, pk):
    amenaza = get_object_or_404(Amenaza, pk=pk)
    if request.method == 'POST':
        form = AmenazaForm(request.POST, instance=amenaza)
        if form.is_valid():
            form.save()
            registrar_log(request.user, 'editar', 'Amenaza', amenaza.pk, f'Amenaza editada: {amenaza.nombre}')
            messages.success(request, 'Amenaza actualizada.')
            return redirect('/amenazas/')
    else:
        form = AmenazaForm(instance=amenaza)
    return render(request, 'amenazas/form.html', {'form': form, 'titulo': 'Editar Amenaza', 'objeto': amenaza})


@login_required
@analista_o_admin
def desactivar_amenaza(request, pk):
    amenaza = get_object_or_404(Amenaza, pk=pk)
    if request.method == 'POST':
        amenaza.estado = 'Inactivo'
        amenaza.save()
        registrar_log(request.user, 'desactivar', 'Amenaza', amenaza.pk, f'Amenaza desactivada: {amenaza.nombre}')
        messages.warning(request, f'Amenaza "{amenaza.nombre}" desactivada.')
    return redirect('/amenazas/')
