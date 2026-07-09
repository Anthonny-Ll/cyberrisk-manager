from django.urls import path
from . import views

urlpatterns = [
    path('riesgos/', views.lista_riesgos, name='riesgos_lista'),
    path('riesgos/nuevo/', views.crear_riesgo, name='riesgos_crear'),
    path('riesgos/matriz/', views.matriz_riesgos, name='riesgos_matriz'),
    path('riesgos/<int:pk>/', views.detalle_riesgo, name='riesgos_detalle'),
    path('riesgos/<int:pk>/editar/', views.editar_riesgo, name='riesgos_editar'),
    path('riesgos/<int:pk>/cerrar/', views.cerrar_riesgo, name='riesgos_cerrar'),
    path('riesgos/api/datos-activo/<int:activo_id>/', views.api_datos_activo, name='api_datos_activo'),
    path('riesgos/api/asesor-ia/', views.api_asesor_ia, name='api_asesor_ia'),
]
