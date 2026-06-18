"""Vistas de autenticación y gestión de usuarios."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Usuario
from .forms import UsuarioCrearForm, UsuarioEditarForm
from .decorators import solo_administrador
from apps.auditoria.utils import registrar_log


def vista_login(request):
    """Pantalla de inicio de sesión."""
    if request.user.is_authenticated:
        return redirect('/dashboard/')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.estado == 'Inactivo':
                messages.error(request, 'Tu cuenta está inactiva. Contacta al administrador.')
            else:
                login(request, user)
                registrar_log(user, 'login', 'Usuario', user.pk, f'Inicio de sesión: {user.username}')
                return redirect('/dashboard/')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'login.html')


@login_required
def vista_logout(request):
    """Cierra la sesión del usuario."""
    registrar_log(request.user, 'login', 'Usuario', request.user.pk, f'Cierre de sesión: {request.user.username}')
    logout(request)
    return redirect('/login/')


@login_required
def dashboard(request):
    """Dashboard principal con KPIs."""
    from apps.activos.models import Activo
    from apps.riesgos.models import Riesgo
    from apps.tratamiento.models import Tratamiento
    from apps.residual.models import RiesgoResidual
    from django.utils import timezone

    activos_total = Activo.objects.filter(estado='Activo').count()
    riesgos = Riesgo.objects.all()
    riesgos_total = riesgos.count()
    riesgos_bajo = riesgos.filter(nivel_cualitativo='Bajo').count()
    riesgos_medio = riesgos.filter(nivel_cualitativo='Medio').count()
    riesgos_alto = riesgos.filter(nivel_cualitativo='Alto').count()
    riesgos_critico = riesgos.filter(nivel_cualitativo='Crítico').count()

    # Riesgos sin tratamiento asignado
    riesgos_sin_tratamiento = riesgos.filter(tratamiento__isnull=True).count()

    # Controles pendientes y vencidos
    controles = Tratamiento.objects.all()
    controles_pendientes = controles.filter(estado_control='Pendiente').count()
    hoy = timezone.now().date()
    controles_vencidos = controles.filter(
        fecha_objetivo__lt=hoy,
        estado_control__in=['Pendiente', 'En progreso']
    ).count()

    # Riesgos residuales sin aceptación
    residuales_pendientes = RiesgoResidual.objects.filter(aceptacion='Pendiente').count()

    # Últimos 5 riesgos
    ultimos_riesgos = riesgos.order_by('-fecha_evaluacion')[:5]

    # Alertas
    alertas_rojas = riesgos.filter(nivel_cualitativo='Crítico', tratamiento__isnull=True)
    alertas_naranja = controles.filter(fecha_objetivo__lt=hoy, estado_control__in=['Pendiente', 'En progreso'])
    alertas_amarillo = RiesgoResidual.objects.filter(aceptacion='Pendiente')

    # Datos para gráfico de barras (Chart.js)
    datos_grafico = {
        'labels': ['Bajo', 'Medio', 'Alto', 'Crítico'],
        'datos': [riesgos_bajo, riesgos_medio, riesgos_alto, riesgos_critico],
        'colores': ['#28a745', '#ffc107', '#fd7e14', '#dc3545'],
    }

    contexto = {
        'activos_total': activos_total,
        'riesgos_total': riesgos_total,
        'riesgos_bajo': riesgos_bajo,
        'riesgos_medio': riesgos_medio,
        'riesgos_alto': riesgos_alto,
        'riesgos_critico': riesgos_critico,
        'riesgos_sin_tratamiento': riesgos_sin_tratamiento,
        'controles_pendientes': controles_pendientes,
        'controles_vencidos': controles_vencidos,
        'residuales_pendientes': residuales_pendientes,
        'ultimos_riesgos': ultimos_riesgos,
        'alertas_rojas': alertas_rojas,
        'alertas_naranja': alertas_naranja,
        'alertas_amarillo': alertas_amarillo,
        'datos_grafico': datos_grafico,
    }
    return render(request, 'dashboard.html', contexto)


@login_required
@solo_administrador
def lista_usuarios(request):
    usuarios = Usuario.objects.all().order_by('username')
    return render(request, 'usuarios/lista.html', {'usuarios': usuarios})


@login_required
@solo_administrador
def crear_usuario(request):
    if request.method == 'POST':
        form = UsuarioCrearForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.nombre_completo = form.cleaned_data.get('nombre_completo', '')
            usuario.save()
            registrar_log(request.user, 'crear', 'Usuario', usuario.pk, f'Usuario creado: {usuario.username}')
            messages.success(request, f'Usuario "{usuario.username}" creado correctamente.')
            return redirect('/usuarios/')
    else:
        form = UsuarioCrearForm()
    return render(request, 'usuarios/form.html', {'form': form, 'titulo': 'Nuevo Usuario'})


@login_required
@solo_administrador
def editar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        form = UsuarioEditarForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            registrar_log(request.user, 'editar', 'Usuario', usuario.pk, f'Usuario editado: {usuario.username}')
            messages.success(request, 'Usuario actualizado correctamente.')
            return redirect('/usuarios/')
    else:
        form = UsuarioEditarForm(instance=usuario)
    return render(request, 'usuarios/form.html', {'form': form, 'titulo': 'Editar Usuario', 'objeto': usuario})


@login_required
@solo_administrador
def desactivar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        usuario.estado = 'Inactivo'
        usuario.save()
        registrar_log(request.user, 'desactivar', 'Usuario', usuario.pk, f'Usuario desactivado: {usuario.username}')
        messages.warning(request, f'Usuario "{usuario.username}" desactivado.')
    return redirect('/usuarios/')
