from django.contrib import admin
from .models import Vulnerabilidad

@admin.register(Vulnerabilidad)
class VulnerabilidadAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'id_activo', 'severidad', 'cvss_score', 'estado']
    list_filter = ['severidad', 'estado']
