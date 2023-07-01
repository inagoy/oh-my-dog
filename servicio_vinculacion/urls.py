from django.urls import path
from . import views

urlpatterns = [
    path('ver_mensaje_concientizacion', views.ver_mensaje_concientizacion, name="ver_mensaje_concientizacion"),
    path('ingresar_servicio_vinculacion', views.ingresar_servicio_vinculacion, name="ingresar_servicio_vinculacion"),
    path('edit_perro_tinder/<int:perro_id>', views.edit_perro_tinder, name='edit_perro_tinder'),
    path('tinder_perro/<int:perro_id>', views.tinder_perro, name='tinder_perro'),
]