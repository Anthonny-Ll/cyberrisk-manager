from django.urls import path
from . import views

urlpatterns = [
    path('riesgos/', views.lista_riesgos, name='riesgos_lista'),
    path('riesgos/nuevo/', views.crear_riesgo, name='riesgos_crear'),
    path('riesgos/matriz/', views.matriz_riesgos, name='riesgos_matriz'),
    path('riesgos/<int:pk>/editar/', views.editar_riesgo, name='riesgos_editar'),
    path('riesgos/<int:pk>/cerrar/', views.cerrar_riesgo, name='riesgos_cerrar'),
]
