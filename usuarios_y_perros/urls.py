from django.urls import path
from . import views

urlpatterns = [
    path('cargar_perro/', views.cargar_perro, name='cargar_perro'),
    path('carga_exitosa/', views.carga_exitosa, name='carga_exitosa'),
    
]