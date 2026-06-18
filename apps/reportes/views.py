"""Vistas de reportes con filtros y exportación PDF."""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone
from apps.activos.models import Activo
from apps.riesgos.models import Riesgo
from apps.tratamiento.models import Tratamiento
from apps.residual.models import RiesgoResidual


@login_required
def index_reportes(request):
    return render(request, 'reportes/index.html')


@login_required
def reporte_activos(request):
    """R1: Inventario de activos."""
    activos = Activo.objects.select_related('propietario').all()
    tipo = request.GET.get('tipo', '')
    departamento = request.GET.get('departamento', '')
    criticidad = request.GET.get('criticidad', '')
    if tipo:
        activos = activos.filter(tipo=tipo)
    if departamento:
        activos = activos.filter(departamento__icontains=departamento)
    if criticidad:
        activos = activos.filter(nivel_criticidad=criticidad)
    ctx = {'activos': activos, 'titulo': 'R1: Inventario de Activos', 'filtros': {'tipo': tipo, 'departamento': departamento, 'criticidad': criticidad}}
    if request.GET.get('pdf'):
        return generar_pdf_activos(activos, ctx['titulo'])
    return render(request, 'reportes/reporte_activos.html', ctx)


@login_required
def reporte_riesgos(request):
    """R3: Riesgos por nivel."""
    riesgos = Riesgo.objects.select_related('id_activo', 'id_amenaza').all()
    nivel = request.GET.get('nivel', '')
    departamento = request.GET.get('departamento', '')
    if nivel:
        riesgos = riesgos.filter(nivel_cualitativo=nivel)
    if departamento:
        riesgos = riesgos.filter(id_activo__departamento__icontains=departamento)
    ctx = {'riesgos': riesgos, 'titulo': 'R3: Riesgos por Nivel', 'filtros': {'nivel': nivel, 'departamento': departamento}}
    if request.GET.get('pdf'):
        return generar_pdf_riesgos(riesgos, ctx['titulo'])
    return render(request, 'reportes/reporte_riesgos.html', ctx)


@login_required
def reporte_criticos(request):
    """R4: Riesgos críticos sin tratamiento."""
    riesgos = Riesgo.objects.filter(nivel_cualitativo='Crítico', tratamiento__isnull=True).select_related('id_activo')
    return render(request, 'reportes/reporte_criticos.html', {
        'riesgos': riesgos,
        'titulo': 'R4: Riesgos Críticos sin Tratamiento',
    })


@login_required
def reporte_controles(request):
    """R5: Controles y su estado."""
    controles = Tratamiento.objects.select_related('id_riesgo').all()
    estado = request.GET.get('estado', '')
    tipo = request.GET.get('tipo', '')
    if estado:
        controles = controles.filter(estado_control=estado)
    if tipo:
        controles = controles.filter(tipo_control=tipo)
    return render(request, 'reportes/reporte_controles.html', {
        'controles': controles,
        'titulo': 'R5: Controles y su Estado',
        'filtros': {'estado': estado, 'tipo': tipo},
    })


@login_required
def reporte_ejecutivo(request):
    """R7: Reporte ejecutivo resumen."""
    activos_total = Activo.objects.filter(estado='Activo').count()
    riesgos = Riesgo.objects.all()
    controles = Tratamiento.objects.all()
    hoy = timezone.now().date()
    ctx = {
        'titulo': 'R7: Reporte Ejecutivo',
        'fecha': hoy,
        'activos_total': activos_total,
        'riesgos_bajo': riesgos.filter(nivel_cualitativo='Bajo').count(),
        'riesgos_medio': riesgos.filter(nivel_cualitativo='Medio').count(),
        'riesgos_alto': riesgos.filter(nivel_cualitativo='Alto').count(),
        'riesgos_critico': riesgos.filter(nivel_cualitativo='Crítico').count(),
        'controles_implementados': controles.filter(estado_control='Implementado').count(),
        'controles_pendientes': controles.filter(estado_control='Pendiente').count(),
        'controles_vencidos': controles.filter(fecha_objetivo__lt=hoy, estado_control__in=['Pendiente', 'En progreso']).count(),
        'residuales_aceptados': RiesgoResidual.objects.filter(aceptacion='Aceptado').count(),
        'residuales_pendientes': RiesgoResidual.objects.filter(aceptacion='Pendiente').count(),
    }
    if request.GET.get('pdf'):
        return generar_pdf_ejecutivo(ctx)
    return render(request, 'reportes/reporte_ejecutivo.html', ctx)


# ── Generación de PDF con ReportLab ──────────────────────────────────────────

def _pdf_header(canvas, doc, titulo):
    """Encabezado estándar para todos los PDFs."""
    from reportlab.lib.units import cm
    canvas.saveState()
    canvas.setFillColorRGB(0.1, 0.13, 0.49)  # azul oscuro #1a237e
    canvas.rect(0, doc.pagesize[1] - 2*cm, doc.pagesize[0], 2*cm, fill=True, stroke=False)
    canvas.setFillColorRGB(1, 1, 1)
    canvas.setFont('Helvetica-Bold', 14)
    canvas.drawString(1*cm, doc.pagesize[1] - 1.3*cm, 'CyberRisk Manager')
    canvas.setFont('Helvetica', 10)
    canvas.drawRightString(doc.pagesize[0] - 1*cm, doc.pagesize[1] - 1.3*cm, titulo)
    canvas.restoreState()


def generar_pdf_activos(activos, titulo):
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    import io

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4), topMargin=2.5*cm)
    styles = getSampleStyleSheet()
    elementos = [
        Paragraph(titulo, styles['Title']),
        Spacer(1, 0.5*cm),
    ]
    datos = [['ID', 'Nombre', 'Tipo', 'Departamento', 'C', 'I', 'D', 'Criticidad', 'Estado']]
    for a in activos:
        datos.append([
            str(a.pk), a.nombre[:40], a.tipo, a.departamento,
            str(a.confidencialidad), str(a.integridad), str(a.disponibilidad),
            a.get_criticidad_label(), a.estado,
        ])
    tabla = Table(datos, repeatRows=1)
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a237e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elementos.append(tabla)
    doc.build(elementos, onFirstPage=lambda c, d: _pdf_header(c, d, titulo),
              onLaterPages=lambda c, d: _pdf_header(c, d, titulo))
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf',
                        headers={'Content-Disposition': f'inline; filename="reporte_activos.pdf"'})


def generar_pdf_riesgos(riesgos, titulo):
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    import io

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4), topMargin=2.5*cm)
    styles = getSampleStyleSheet()
    nivel_colores = {
        'Bajo': colors.HexColor('#d4edda'),
        'Medio': colors.HexColor('#fff3cd'),
        'Alto': colors.HexColor('#ffe5b4'),
        'Crítico': colors.HexColor('#f8d7da'),
    }
    elementos = [Paragraph(titulo, styles['Title']), Spacer(1, 0.5*cm)]
    datos = [['ID', 'Activo', 'Amenaza', 'Probabilidad', 'Impacto', 'Inherente', 'Nivel', 'Estado']]
    filas_colores = [colors.HexColor('#1a237e')]  # encabezado
    for r in riesgos:
        datos.append([
            f'R-{r.pk:03d}', r.id_activo.nombre[:35], r.id_amenaza.nombre[:30],
            str(r.probabilidad), str(r.impacto), str(r.riesgo_inherente),
            r.nivel_cualitativo, r.estado_riesgo,
        ])
        filas_colores.append(nivel_colores.get(r.nivel_cualitativo, colors.white))

    tabla = Table(datos, repeatRows=1)
    estilos = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a237e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]
    for i, color in enumerate(filas_colores[1:], start=1):
        estilos.append(('BACKGROUND', (0, i), (-1, i), color))
    tabla.setStyle(TableStyle(estilos))
    elementos.append(tabla)
    doc.build(elementos, onFirstPage=lambda c, d: _pdf_header(c, d, titulo),
              onLaterPages=lambda c, d: _pdf_header(c, d, titulo))
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf',
                        headers={'Content-Disposition': f'inline; filename="reporte_riesgos.pdf"'})


def generar_pdf_ejecutivo(ctx):
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    import io

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=2.5*cm)
    styles = getSampleStyleSheet()
    titulo = ctx['titulo']
    elementos = [
        Paragraph('CyberRisk Manager', styles['Title']),
        Paragraph(titulo, styles['Heading2']),
        Paragraph(f"Fecha: {ctx['fecha']}", styles['Normal']),
        Spacer(1, 0.5*cm),
        Paragraph('Resumen de Activos y Riesgos', styles['Heading3']),
    ]
    resumen = [
        ['Indicador', 'Valor'],
        ['Total de activos activos', str(ctx['activos_total'])],
        ['Riesgos BAJOS', str(ctx['riesgos_bajo'])],
        ['Riesgos MEDIOS', str(ctx['riesgos_medio'])],
        ['Riesgos ALTOS', str(ctx['riesgos_alto'])],
        ['Riesgos CRÍTICOS', str(ctx['riesgos_critico'])],
        ['Controles implementados', str(ctx['controles_implementados'])],
        ['Controles pendientes', str(ctx['controles_pendientes'])],
        ['Controles vencidos', str(ctx['controles_vencidos'])],
        ['Residuales aceptados', str(ctx['residuales_aceptados'])],
        ['Residuales pendientes', str(ctx['residuales_pendientes'])],
    ]
    tabla = Table(resumen, colWidths=[10*cm, 5*cm])
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a237e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
    ]))
    elementos.append(tabla)
    doc.build(elementos, onFirstPage=lambda c, d: _pdf_header(c, d, titulo),
              onLaterPages=lambda c, d: _pdf_header(c, d, titulo))
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf',
                        headers={'Content-Disposition': 'inline; filename="reporte_ejecutivo.pdf"'})
