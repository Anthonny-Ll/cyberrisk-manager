from django.urls import path
from . import views

urlpatterns = [
    path('vulnerabilidades/', views.lista_vulnerabilidades, name='vulnerabilidades_lista'),
    path('vulnerabilidades/nuevo/', views.crear_vulnerabilidad, name='vulnerabilidades_crear'),
    path('vulnerabilidades/<int:pk>/editar/', views.editar_vulnerabilidad, name='vulnerabilidades_editar'),
    path('vulnerabilidades/<int:pk>/resolver/', views.desactivar_vulnerabilidad, name='vulnerabilidades_resolver'),
]
