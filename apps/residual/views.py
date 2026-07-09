from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from apps.auditoria.utils import registrar_log
from .models import RiesgoResidual
from .forms import RiesgoResidualForm, AceptacionResidualForm


@login_required
def lista_residual(request):
    residuales = RiesgoResidual.objects.select_related('id_riesgo', 'id_tratamiento').all()
    nivel = request.GET.get('nivel', '')
    decision = request.GET.get('decision', '')
    if nivel:
        residuales = residuales.filter(nivel_cualitativo=nivel)
    if decision:
        residuales = residuales.filter(aceptacion=decision)
    return render(request, 'residual/lista.html', {
        'residuales': residuales,
        'filtros': {'nivel': nivel, 'decision': decision},
    })


@login_required
def crear_residual(request):
    if request.method == 'POST':
        form = RiesgoResidualForm(request.POST)
        if form.is_valid():
            residual = form.save()
            # Actualizar estado del riesgo a "Con residual"
            residual.id_riesgo.estado_riesgo = 'Con residual'
            residual.id_riesgo.save()
            registrar_log(request.user, 'crear', 'RiesgoResidual', residual.pk,
                         f'Riesgo residual creado: RR-{residual.pk:03d}')
            messages.success(request, f'Riesgo residual registrado. Nivel: {residual.nivel_cualitativo} ({residual.riesgo_residual})')
            return redirect('/residual/')
    else:
        form = RiesgoResidualForm()
    return render(request, 'residual/form.html', {'form': form, 'titulo': 'Nuevo Riesgo Residual'})


@login_required
def aceptar_residual(request, pk):
    """RN-07: Registra la decisión de aceptación del riesgo residual."""
    residual = get_object_or_404(RiesgoResidual, pk=pk)
    if request.method == 'POST':
        form = AceptacionResidualForm(request.POST, instance=residual)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.id_usuario_aprueba = request.user
            obj.fecha_decision = timezone.now()
            obj.save()
            registrar_log(request.user, 'editar', 'RiesgoResidual', residual.pk,
                         f'Decisión registrada: {residual.aceptacion} — RR-{residual.pk:03d}')
            messages.success(request, f'Decisión "{residual.aceptacion}" registrada correctamente.')
            return redirect('/residual/')
    else:
        form = AceptacionResidualForm(instance=residual)
    return render(request, 'residual/aceptacion.html', {'form': form, 'residual': residual})
