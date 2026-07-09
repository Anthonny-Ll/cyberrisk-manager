from django.urls import path
from . import views

urlpatterns = [
    path('activos/', views.lista_activos, name='activos_lista'),
    path('activos/nuevo/', views.crear_activo, name='activos_crear'),
    path('activos/<int:pk>/', views.detalle_activo, name='activos_detalle'),
    path('activos/<int:pk>/editar/', views.editar_activo, name='activos_editar'),
    path('activos/<int:pk>/desactivar/', views.desactivar_activo, name='activos_desactivar'),
]
