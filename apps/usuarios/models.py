"""Modelo de usuario personalizado con campo rol."""
from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    """Extiende AbstractUser añadiendo rol y estado para el sistema."""

    ROL_CHOICES = [
        ('administrador', 'Administrador'),
        ('analista', 'Analista de Riesgos'),
        ('responsable', 'Responsable de Activo'),
        ('auditor', 'Auditor / Alta Dirección'),
    ]

    ESTADO_CHOICES = [
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
    ]

    nombre_completo = models.CharField('Nombre completo', max_length=200, blank=True)
    rol = models.CharField('Rol', max_length=20, choices=ROL_CHOICES, default='analista')
    estado = models.CharField('Estado', max_length=10, choices=ESTADO_CHOICES, default='Activo')

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['username']

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_rol_display()})"

    def es_administrador(self):
        return self.rol == 'administrador'

    def es_analista(self):
        return self.rol in ('administrador', 'analista')

    def es_auditor(self):
        return self.rol in ('administrador', 'auditor')
