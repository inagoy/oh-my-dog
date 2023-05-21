from django.urls import path
from . import views

urlpatterns = [
    path('cargar_perro/', views.cargar_perro, name='cargar_perro'),
    path('cargar_perro/<int:user_id>', views.cargar_perro, name='cargar_perro'),
    path('nuevo', views.registrar_usuario, name='registrar_usuario'),
    path('iniciar_sesion', views.iniciar_sesion, name="iniciar_sesion"),
    path('cerrar_sesion', views.cerrar_sesion, name='cerrar_sesion'),
    path('perro/<int:perro_id>/', views.perro, name='perro'),
]
