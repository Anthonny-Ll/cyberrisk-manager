from django.urls import path
from . import views

urlpatterns = [
    path('reportes/', views.index_reportes, name='reportes_index'),
    path('reportes/activos/', views.reporte_activos, name='reportes_activos'),
    path('reportes/riesgos/', views.reporte_riesgos, name='reportes_riesgos'),
    path('reportes/criticos/', views.reporte_criticos, name='reportes_criticos'),
    path('reportes/controles/', views.reporte_controles, name='reportes_controles'),
    path('reportes/ejecutivo/', views.reporte_ejecutivo, name='reportes_ejecutivo'),
]
