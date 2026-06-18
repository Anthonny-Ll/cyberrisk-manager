from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.vista_login, name='login'),
    path('logout/', views.vista_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('usuarios/', views.lista_usuarios, name='usuarios_lista'),
    path('usuarios/nuevo/', views.crear_usuario, name='usuarios_crear'),
    path('usuarios/<int:pk>/editar/', views.editar_usuario, name='usuarios_editar'),
    path('usuarios/<int:pk>/desactivar/', views.desactivar_usuario, name='usuarios_desactivar'),
]
