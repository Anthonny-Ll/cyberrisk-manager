"""Modelo de amenazas con relación M:M a activos."""
from django.db import models
from apps.activos.models import Activo


class Amenaza(models.Model):
    TIPO_CHOICES = [
        ('Natural', 'Natural'),
        ('Humana deliberada', 'Humana deliberada'),
        ('Humana accidental', 'Humana accidental'),
        ('Tecnológica', 'Tecnológica'),
    ]
    FUENTE_CHOICES = [
        ('Externa', 'Externa'),
        ('Interna', 'Interna'),
        ('Mixta', 'Mixta'),
    ]
    ESTADO_CHOICES = [('Activo', 'Activo'), ('Inactivo', 'Inactivo')]

    nombre = models.CharField('Nombre', max_length=200)
    descripcion = models.TextField('Descripción', blank=True)
    tipo_amenaza = models.CharField('Tipo', max_length=30, choices=TIPO_CHOICES)
    fuente_amenaza = models.CharField('Fuente', max_length=10, choices=FUENTE_CHOICES)
    activos = models.ManyToManyField(Activo, through='ActivoAmenaza', verbose_name='Activos asociados', blank=True)
    estado = models.CharField('Estado', max_length=10, choices=ESTADO_CHOICES, default='Activo')
    observaciones = models.TextField('Observaciones', blank=True)
    fecha_creacion = models.DateTimeField('Fecha de creación', auto_now_add=True)

    class Meta:
        verbose_name = 'Amenaza'
        verbose_name_plural = 'Amenazas'
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.tipo_amenaza})"


class ActivoAmenaza(models.Model):
    """Tabla intermedia para la relación M:M entre Activo y Amenaza."""
    id_activo = models.ForeignKey(Activo, on_delete=models.CASCADE, verbose_name='Activo')
    id_amenaza = models.ForeignKey(Amenaza, on_delete=models.CASCADE, verbose_name='Amenaza')

    class Meta:
        unique_together = ('id_activo', 'id_amenaza')
        verbose_name = 'Activo-Amenaza'
