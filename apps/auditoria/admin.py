from django.contrib import admin
from .models import LogAuditoria

@admin.register(LogAuditoria)
class LogAuditoriaAdmin(admin.ModelAdmin):
    list_display = ['fecha_hora', 'id_usuario', 'accion', 'entidad_afectada', 'id_entidad']
    list_filter = ['accion', 'entidad_afectada']
    search_fields = ['descripcion', 'entidad_afectada']
