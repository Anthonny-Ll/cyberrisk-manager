"""Modelo de log de auditoría para registrar todos los cambios del sistema."""
from django.db import models
from django.conf import settings


class LogAuditoria(models.Model):
    ACCION_CHOICES = [
        ('crear', 'Crear'),
        ('editar', 'Editar'),
        ('desactivar', 'Desactivar'),
        ('login', 'Login'),
        ('eliminar', 'Eliminar'),
    ]

    id_usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Usuario'
    )
    accion = models.CharField('Acción', max_length=20, choices=ACCION_CHOICES)
    entidad_afectada = models.CharField('Entidad', max_length=100)
    id_entidad = models.IntegerField('ID Entidad', null=True, blank=True)
    descripcion = models.TextField('Descripción')
    fecha_hora = models.DateTimeField('Fecha y hora', auto_now_add=True)

    class Meta:
        verbose_name = 'Log de auditoría'
        verbose_name_plural = 'Logs de auditoría'
        ordering = ['-fecha_hora']

    def __str__(self):
        return f"{self.fecha_hora:%Y-%m-%d %H:%M} | {self.id_usuario} | {self.accion} | {self.entidad_afectada}"
