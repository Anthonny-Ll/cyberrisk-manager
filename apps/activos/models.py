"""Modelo de activos de información con valoración C-I-D."""
from django.db import models
from django.conf import settings


class Activo(models.Model):
    TIPO_CHOICES = [
        ('Datos', 'Datos'),
        ('Software', 'Software'),
        ('Hardware', 'Hardware'),
        ('Red', 'Red'),
        ('Servicio', 'Servicio'),
        ('Instalación', 'Instalación'),
        ('Personas', 'Personas'),
    ]
    ESTADO_CHOICES = [('Activo', 'Activo'), ('Inactivo', 'Inactivo')]
    VALOR_CHOICES = [(1, '1 - Bajo'), (2, '2 - Medio'), (3, '3 - Alto'), (4, '4 - Crítico')]
    DEPARTAMENTO_CHOICES = [
        ('Tecnología', 'Tecnología'),
        ('Finanzas', 'Finanzas'),
        ('Recursos Humanos', 'Recursos Humanos'),
        ('Administración', 'Administración'),
        ('Operaciones', 'Operaciones'),
        ('Legal y Cumplimiento', 'Legal y Cumplimiento'),
        ('Ventas y Marketing', 'Ventas y Marketing'),
    ]

    nombre = models.CharField('Nombre', max_length=200)
    tipo = models.CharField('Tipo', max_length=20, choices=TIPO_CHOICES)
    descripcion = models.TextField('Descripción', blank=True)
    propietario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name='Propietario',
        related_name='activos_propietario'
    )
    departamento = models.CharField('Departamento', max_length=100, choices=DEPARTAMENTO_CHOICES)
    confidencialidad = models.IntegerField('Confidencialidad (C)', choices=VALOR_CHOICES)
    integridad = models.IntegerField('Integridad (I)', choices=VALOR_CHOICES)
    disponibilidad = models.IntegerField('Disponibilidad (D)', choices=VALOR_CHOICES)
    datos_sensibles = models.BooleanField('Datos sensibles (LOPDP)', default=False)
    nivel_criticidad = models.IntegerField('Nivel de criticidad', editable=False, default=1)
    estado = models.CharField('Estado', max_length=10, choices=ESTADO_CHOICES, default='Activo')
    observaciones = models.TextField('Observaciones', blank=True)
    fecha_creacion = models.DateTimeField('Fecha de creación', auto_now_add=True)

    class Meta:
        verbose_name = 'Activo'
        verbose_name_plural = 'Activos'
        ordering = ['-nivel_criticidad', 'nombre']

    def save(self, *args, **kwargs):
        # RN-06: Si datos_sensibles, confidencialidad fija en 4
        if self.datos_sensibles:
            self.confidencialidad = 4
        # Calcula criticidad como máximo de C, I, D
        self.nivel_criticidad = max(self.confidencialidad, self.integridad, self.disponibilidad)
        super().save(*args, **kwargs)

    def get_criticidad_display_color(self):
        colores = {1: 'success', 2: 'warning', 3: 'orange', 4: 'danger'}
        return colores.get(self.nivel_criticidad, 'secondary')

    def get_criticidad_label(self):
        labels = {1: 'Bajo', 2: 'Medio', 3: 'Alto', 4: 'Crítico'}
        return labels.get(self.nivel_criticidad, 'N/A')

    def __str__(self):
        return f"{self.nombre} ({self.tipo})"
