"""Modelo de evaluación de riesgo inherente (P × I)."""
from django.db import models
from django.conf import settings
from apps.activos.models import Activo
from apps.amenazas.models import Amenaza
from apps.vulnerabilidades.models import Vulnerabilidad


def calcular_nivel_cualitativo(valor):
    """Clasifica el riesgo según su valor numérico."""
    if valor <= 4:
        return 'Bajo'
    elif valor <= 8:
        return 'Medio'
    elif valor <= 12:
        return 'Alto'
    return 'Crítico'


class Riesgo(models.Model):
    PROBABILIDAD_CHOICES = [
        (1, '1 - Rara vez'),
        (2, '2 - Poco probable'),
        (3, '3 - Probable'),
        (4, '4 - Casi seguro'),
    ]
    IMPACTO_CHOICES = [
        (1, '1 - Insignificante'),
        (2, '2 - Menor'),
        (3, '3 - Moderado'),
        (4, '4 - Catastrófico'),
    ]
    ESTADO_CHOICES = [
        ('Evaluado', 'Evaluado'),
        ('En tratamiento', 'En tratamiento'),
        ('Con residual', 'Con residual'),
        ('Cerrado', 'Cerrado'),
    ]

    id_activo = models.ForeignKey(Activo, on_delete=models.CASCADE, verbose_name='Activo')
    id_amenaza = models.ForeignKey(Amenaza, on_delete=models.CASCADE, verbose_name='Amenaza')
    id_vulnerabilidad = models.ForeignKey(Vulnerabilidad, on_delete=models.CASCADE, verbose_name='Vulnerabilidad')
    probabilidad = models.IntegerField('Probabilidad', choices=PROBABILIDAD_CHOICES)
    impacto = models.IntegerField('Impacto', choices=IMPACTO_CHOICES)
    riesgo_inherente = models.IntegerField('Riesgo inherente', editable=False, default=0)
    nivel_cualitativo = models.CharField('Nivel cualitativo', max_length=10, editable=False)
    estado_riesgo = models.CharField('Estado', max_length=20, choices=ESTADO_CHOICES, default='Evaluado')
    observaciones = models.TextField('Observaciones', blank=True)
    id_usuario_registra = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Registrado por'
    )
    fecha_evaluacion = models.DateTimeField('Fecha de evaluación', auto_now_add=True)

    class Meta:
        verbose_name = 'Evaluación de riesgo'
        verbose_name_plural = 'Evaluaciones de riesgo'
        ordering = ['-riesgo_inherente', '-fecha_evaluacion']

    def save(self, *args, **kwargs):
        # Cálculo automático del riesgo inherente
        self.riesgo_inherente = self.probabilidad * self.impacto
        self.nivel_cualitativo = calcular_nivel_cualitativo(self.riesgo_inherente)
        super().save(*args, **kwargs)

    def get_nivel_color(self):
        colores = {'Bajo': 'success', 'Medio': 'warning', 'Alto': 'orange-custom', 'Crítico': 'danger'}
        return colores.get(self.nivel_cualitativo, 'secondary')

    def get_nivel_badge(self):
        badges = {'Bajo': 'bg-success', 'Medio': 'bg-warning text-dark', 'Alto': 'bg-orange', 'Crítico': 'bg-danger'}
        return badges.get(self.nivel_cualitativo, 'bg-secondary')

    def __str__(self):
        return f"R-{self.pk:03d} | {self.id_activo.nombre} | {self.nivel_cualitativo} ({self.riesgo_inherente})"
