from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.auditoria.utils import registrar_log
import requests
from django.http import JsonResponse
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
def desactivar_vulnerabilidad(request, pk):
    vuln = get_object_or_404(Vulnerabilidad, pk=pk)
    if request.method == 'POST':
        vuln.estado = 'Resuelta'
        vuln.save()
        registrar_log(request.user, 'desactivar', 'Vulnerabilidad', vuln.pk, f'Vulnerabilidad resuelta: {vuln.nombre}')
        messages.warning(request, f'Vulnerabilidad "{vuln.nombre}" marcada como resuelta.')
    return redirect('/vulnerabilidades/')

@login_required
def api_buscar_cve(request):
    """Consulta la API pública del NIST NVD para un CVE específico."""
    cve_id = request.GET.get('cve_id', '').strip().upper()
    if not cve_id.startswith('CVE-'):
        return JsonResponse({'error': 'Formato inválido. Use CVE-YYYY-NNNNN'}, status=400)
    
    url = f'https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cve_id}'
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            return JsonResponse({'error': 'No se pudo conectar con NIST NVD'}, status=502)
        
        data = resp.json()
        vulnerabilities = data.get('vulnerabilities', [])
        if not vulnerabilities:
            return JsonResponse({'error': f'{cve_id} no encontrado en NIST'}, status=404)
        
        cve = vulnerabilities[0]['cve']
        
        # Extraer CVSS score V3.1
        cvss_data = cve.get('metrics', {}).get('cvssMetricV31', [{}])
        cvss_score = cvss_data[0].get('cvssData', {}).get('baseScore', 0) if cvss_data else 0
        
        # Descripción
        descriptions = cve.get('descriptions', [])
        desc_es = next((d['value'] for d in descriptions if d['lang'] == 'es'), None)
        desc_en = next((d['value'] for d in descriptions if d['lang'] == 'en'), '')
        
        return JsonResponse({
            'cve_id': cve_id,
            'descripcion': desc_es or desc_en,
            'cvss_score': cvss_score,
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
