from django.contrib import admin
from .models import RiesgoResidual

@admin.register(RiesgoResidual)
class RiesgoResidualAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'prob_residual', 'impacto_residual', 'riesgo_residual', 'nivel_cualitativo', 'aceptacion']
