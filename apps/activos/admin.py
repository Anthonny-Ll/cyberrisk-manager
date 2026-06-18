from django.contrib import admin
from .models import Activo

@admin.register(Activo)
class ActivoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo', 'departamento', 'nivel_criticidad', 'estado']
    list_filter = ['tipo', 'estado', 'nivel_criticidad']
    search_fields = ['nombre', 'departamento']
