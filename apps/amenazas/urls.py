from django.urls import path
from . import views

urlpatterns = [
    path('amenazas/', views.lista_amenazas, name='amenazas_lista'),
    path('amenazas/nuevo/', views.crear_amenaza, name='amenazas_crear'),
    path('amenazas/<int:pk>/editar/', views.editar_amenaza, name='amenazas_editar'),
    path('amenazas/<int:pk>/desactivar/', views.desactivar_amenaza, name='amenazas_desactivar'),
]
