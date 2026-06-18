from django.urls import path
from . import views

urlpatterns = [
    path('auditoria/', views.lista_auditoria, name='auditoria_lista'),
]
