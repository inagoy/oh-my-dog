from django.urls import path
from . import views

urlpatterns = [
    path('cargar_perro/', views.cargar_perro, name='cargar_perro'),
    path('carga_exitosa/', views.carga_exitosa, name='carga_exitosa'),
    path('nuevo',views.registrar_usuario, name='registrar_usuario'),
    path('iniciar_sesion', views.iniciar_sesion, name="iniciar_sesion"),
    path('cerrar_sesion', views.cerrar_sesion, name='cerrar_sesion')
]