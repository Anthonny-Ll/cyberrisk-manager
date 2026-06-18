from django.contrib import admin
from .models import Amenaza, ActivoAmenaza

@admin.register(Amenaza)
class AmenazaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo_amenaza', 'fuente_amenaza', 'estado']

admin.site.register(ActivoAmenaza)
