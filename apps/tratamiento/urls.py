from django.urls import path
from . import views

urlpatterns = [
    path('tratamiento/', views.lista_tratamientos, name='tratamiento_lista'),
    path('tratamiento/nuevo/', views.crear_tratamiento, name='tratamiento_crear'),
    path('tratamiento/<int:pk>/editar/', views.editar_tratamiento, name='tratamiento_editar'),
]
