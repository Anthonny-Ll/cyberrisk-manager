from django.contrib import admin
from .models import Tratamiento

@admin.register(Tratamiento)
class TratamientoAdmin(admin.ModelAdmin):
    list_display = ['nombre_control', 'estrategia', 'tipo_control', 'responsable', 'fecha_objetivo', 'estado_control']
    list_filter = ['estrategia', 'tipo_control', 'estado_control']
