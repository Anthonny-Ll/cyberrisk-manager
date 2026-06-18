"""Modelo de tratamiento de riesgos y controles."""
from django.db import models
from apps.riesgos.models import Riesgo


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
    responsable = models.CharField('Responsable', max_length=200)
    fecha_objetivo = models.DateField('Fecha objetivo')
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
