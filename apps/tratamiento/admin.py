from django.contrib import admin
from .models import Tratamiento, ControlISO27001

@admin.register(Tratamiento)
class TratamientoAdmin(admin.ModelAdmin):
    list_display = ['nombre_control', 'estrategia', 'tipo_control', 'control_iso', 'responsable', 'fecha_objetivo', 'estado_control']
    list_filter = ['estrategia', 'tipo_control', 'estado_control']


@admin.register(ControlISO27001)
class ControlISO27001Admin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'categoria']
    list_filter = ['categoria']
    search_fields = ['codigo', 'nombre']
