from django.contrib import admin
from .models import Riesgo

@admin.register(Riesgo)
class RiesgoAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'probabilidad', 'impacto', 'riesgo_inherente', 'nivel_cualitativo', 'estado_riesgo']
    list_filter = ['nivel_cualitativo', 'estado_riesgo']
