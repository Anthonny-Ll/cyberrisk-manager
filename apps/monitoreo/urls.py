from django.urls import path
from . import views

urlpatterns = [
    path('monitoreo/', views.panel_monitoreo, name='monitoreo'),
]
