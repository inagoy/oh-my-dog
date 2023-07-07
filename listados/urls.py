from django.urls import path
from . import views

urlpatterns = [
    path('paseadores_cuidadores', views.paseadores_cuidadores, name='paseadores_cuidadores'),
    path('cargar_trabajador', views.cargar_trabajador, name='cargar_trabajador')
]