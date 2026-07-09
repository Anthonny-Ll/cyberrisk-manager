"""Modelo de vulnerabilidades asociadas a activos."""
from django.db import models
from apps.activos.models import Activo
from apps.amenazas.models import Amenaza

class Vulnerabilidad(models.Model):
    SEVERIDAD_CHOICES = [
        ('Baja', 'Baja'),
        ('Media', 'Media'),
        ('Alta', 'Alta'),
        ('Crítica', 'Crítica'),
    ]
    ESTADO_CHOICES = [
        ('Identificada', 'Identificada'),
        ('En tratamiento', 'En tratamiento'),
        ('Resuelta', 'Resuelta'),
    ]

    nombre = models.CharField('Nombre', max_length=200)
    descripcion = models.TextField('Descripción', blank=True)
    cve_id = models.CharField('CVE ID', max_length=50, blank=True, help_text='Ej: CVE-2024-1234')
    id_activo = models.ForeignKey(Activo, on_delete=models.CASCADE, verbose_name='Activo', related_name='vulnerabilidades')
    amenaza_asociada = models.ForeignKey(Amenaza, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Amenaza asociada')
    cvss_score = models.FloatField('CVSS Score', null=True, blank=True, help_text='0.0 – 10.0')
    cvss_vector = models.CharField('Vector CVSS', max_length=60, blank=True,
        help_text='Cadena de vector CVSS v3.1 generada por la calculadora')
    severidad = models.CharField('Severidad', max_length=10, choices=SEVERIDAD_CHOICES)
    evidencia = models.TextField('Evidencia', blank=True)
    estado = models.CharField('Estado', max_length=20, choices=ESTADO_CHOICES, default='Identificada')
    observaciones = models.TextField('Observaciones', blank=True)
    fecha_creacion = models.DateTimeField('Fecha de creación', auto_now_add=True)

    class Meta:
        verbose_name = 'Vulnerabilidad'
        verbose_name_plural = 'Vulnerabilidades'
        ordering = ['-fecha_creacion']

    def save(self, *args, **kwargs):
        # Sugerencia automática de severidad desde CVSS si se proporciona
        if self.cvss_score is not None and not self.severidad:
            self.severidad = self._cvss_a_severidad(self.cvss_score)
        super().save(*args, **kwargs)

    @staticmethod
    def _cvss_a_severidad(score):
        if score < 4.0:
            return 'Baja'
        elif score < 7.0:
            return 'Media'
        elif score < 9.0:
            return 'Alta'
        return 'Crítica'

    def get_severidad_color(self):
        colores = {'Baja': 'success', 'Media': 'warning', 'Alta': 'orange', 'Crítica': 'danger'}
        return colores.get(self.severidad, 'secondary')

    def __str__(self):
        return f"{self.nombre} — {self.id_activo.nombre}"
