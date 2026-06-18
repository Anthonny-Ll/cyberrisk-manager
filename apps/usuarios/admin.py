from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ['username', 'nombre_completo', 'email', 'rol', 'estado']
    list_filter = ['rol', 'estado']
    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {'fields': ('nombre_completo', 'rol', 'estado')}),
    )
