from django.urls import path
from . import views

urlpatterns = [
    path('residual/', views.lista_residual, name='residual_lista'),
    path('residual/nuevo/', views.crear_residual, name='residual_crear'),
    path('residual/<int:pk>/aceptar/', views.aceptar_residual, name='residual_aceptar'),
]
