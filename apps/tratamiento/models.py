"""Modelo de tratamiento de riesgos y controles."""
from django.db import models
from apps.riesgos.models import Riesgo


class ControlISO27001(models.Model):
    """Catálogo de controles de referencia ISO/IEC 27001:2022 (Anexo A)."""
    CATEGORIA_CHOICES = [
        ('Organizacional', 'Organizacional'),
        ('Personas', 'Personas'),
        ('Físico', 'Físico'),
        ('Tecnológico', 'Tecnológico'),
    ]

    codigo = models.CharField('Código ISO', max_length=10, unique=True)
    nombre = models.CharField('Nombre del control', max_length=300)
    categoria = models.CharField('Categoría', max_length=20, choices=CATEGORIA_CHOICES)
    descripcion = models.TextField('Descripción', blank=True)

    class Meta:
        verbose_name = 'Control ISO 27001'
        verbose_name_plural = 'Controles ISO 27001'
        ordering = ['codigo']

    def __str__(self):
        return f"{self.codigo} — {self.nombre}"


class Tratamiento(models.Model):
    ESTRATEGIA_CHOICES = [
        ('Mitigar', 'Mitigar'),
        ('Transferir', 'Transferir'),
        ('Evitar', 'Evitar'),
        ('Aceptar', 'Aceptar'),
    ]
    TIPO_CONTROL_CHOICES = [
        ('Técnico', 'Técnico'),
        ('Administrativo', 'Administrativo'),
        ('Físico', 'Físico'),
    ]
    FUNCION_CHOICES = [
        ('Preventivo', 'Preventivo'),
        ('Detectivo', 'Detectivo'),
        ('Correctivo', 'Correctivo'),
    ]
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('En progreso', 'En progreso'),
        ('Implementado', 'Implementado'),
    ]

    id_riesgo = models.ForeignKey(Riesgo, on_delete=models.CASCADE, verbose_name='Riesgo', related_name='tratamiento')
    estrategia = models.CharField('Estrategia', max_length=15, choices=ESTRATEGIA_CHOICES)
    nombre_control = models.CharField('Nombre del control', max_length=200)
    descripcion_ctrl = models.TextField('Descripción del control')
    tipo_control = models.CharField('Tipo de control', max_length=20, choices=TIPO_CONTROL_CHOICES)
    funcion_control = models.CharField('Función del control', max_length=15, choices=FUNCION_CHOICES)
    control_iso = models.ForeignKey(
        ControlISO27001, on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name='Control ISO 27001 de referencia', related_name='tratamientos'
    )
    responsable = models.CharField('Responsable', max_length=200)
    fecha_objetivo = models.DateField('Fecha objetivo')
    fecha_planificacion = models.DateField('Fecha de planificación', null=True, blank=True,
        help_text='Cuándo se planificó este tratamiento')
    fecha_inicio_ejecucion = models.DateField('Fecha de inicio de ejecución', null=True, blank=True,
        help_text='Cuándo se inició la implementación del control')
    fecha_finalizacion = models.DateField('Fecha de finalización', null=True, blank=True,
        help_text='Cuándo se completó la implementación')
    estado_control = models.CharField('Estado del control', max_length=15, choices=ESTADO_CHOICES, default='Pendiente')
    justificacion = models.TextField('Justificación', blank=True, help_text='Obligatoria si estrategia = Aceptar')
    fecha_registro = models.DateTimeField('Fecha de registro', auto_now_add=True)

    class Meta:
        verbose_name = 'Tratamiento'
        verbose_name_plural = 'Tratamientos'
        ordering = ['fecha_objetivo']

    def __str__(self):
        return f"{self.nombre_control} ({self.estrategia}) — R-{self.id_riesgo.pk:03d}"

    def esta_vencido(self):
        from django.utils import timezone
        return self.fecha_objetivo < timezone.now().date() and self.estado_control != 'Implementado'

    def dias_restantes(self):
        from django.utils import timezone
        if self.estado_control == 'Implementado':
            return None
        return (self.fecha_objetivo - timezone.now().date()).days

    def pct_avance_temporal(self):
        """Porcentaje transcurrido entre el inicio planificado y la fecha objetivo."""
        from django.utils import timezone
        inicio = self.fecha_inicio_ejecucion or self.fecha_planificacion or self.fecha_registro.date()
        total = (self.fecha_objetivo - inicio).days
        if total <= 0:
            return 100
        transcurrido = (timezone.now().date() - inicio).days
        return max(0, min(round(transcurrido / total * 100), 100))

    def get_semaforo(self):
        """Color de estado: verde a tiempo, amarillo próximo a vencer, rojo vencido."""
        if self.estado_control == 'Implementado':
            return 'success'
        dias = self.dias_restantes()
        if dias is None:
            return 'secondary'
        if dias < 0:
            return 'danger'
        if dias <= 5:
            return 'warning'
        return 'success'
