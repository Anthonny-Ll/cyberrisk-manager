"""Modelo de riesgo residual tras la implementación de controles."""
from django.db import models
from django.conf import settings
from apps.riesgos.models import Riesgo, calcular_nivel_cualitativo
from apps.tratamiento.models import Tratamiento


class RiesgoResidual(models.Model):
    ACEPTACION_CHOICES = [
        ('Aceptado', 'Aceptado'),
        ('Rechazado', 'Rechazado'),
        ('Pendiente', 'Pendiente'),
    ]
    PROB_CHOICES = [
        (1, '1 - Rara vez'),
        (2, '2 - Poco probable'),
        (3, '3 - Probable'),
        (4, '4 - Casi seguro'),
    ]
    IMP_CHOICES = [
        (1, '1 - Insignificante'),
        (2, '2 - Menor'),
        (3, '3 - Moderado'),
        (4, '4 - Catastrófico'),
    ]

    id_riesgo = models.OneToOneField(Riesgo, on_delete=models.CASCADE, verbose_name='Riesgo', related_name='residual')
    id_tratamiento = models.ForeignKey(Tratamiento, on_delete=models.CASCADE, verbose_name='Tratamiento')
    prob_residual = models.IntegerField('Probabilidad residual', choices=PROB_CHOICES)
    impacto_residual = models.IntegerField('Impacto residual', choices=IMP_CHOICES)
    riesgo_residual = models.IntegerField('Riesgo residual', editable=False, default=0)
    nivel_cualitativo = models.CharField('Nivel cualitativo', max_length=10, editable=False)
    aceptacion = models.CharField('Decisión', max_length=10, choices=ACEPTACION_CHOICES, default='Pendiente')
    resp_aprobacion = models.CharField('Responsable de aprobación', max_length=200, blank=True)
    id_usuario_aprueba = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Usuario que aprueba'
    )
    fecha_decision = models.DateTimeField('Fecha de decisión', null=True, blank=True)
    observaciones = models.TextField('Observaciones', blank=True)

    class Meta:
        verbose_name = 'Riesgo residual'
        verbose_name_plural = 'Riesgos residuales'
        ordering = ['-riesgo_residual']

    def save(self, *args, **kwargs):
        self.riesgo_residual = self.prob_residual * self.impacto_residual
        self.nivel_cualitativo = calcular_nivel_cualitativo(self.riesgo_residual)
        super().save(*args, **kwargs)

    def get_nivel_badge(self):
        badges = {'Bajo': 'bg-success', 'Medio': 'bg-warning text-dark', 'Alto': 'bg-orange', 'Crítico': 'bg-danger'}
        return badges.get(self.nivel_cualitativo, 'bg-secondary')

    def __str__(self):
        return f"RR-{self.pk:03d} | R-{self.id_riesgo.pk:03d} | {self.nivel_cualitativo} ({self.riesgo_residual})"
