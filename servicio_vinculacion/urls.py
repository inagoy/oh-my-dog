from django.urls import path
from . import views

urlpatterns = [
    path('ver_mensaje_concientizacion', views.ver_mensaje_concientizacion, name="ver_mensaje_concientizacion"),
    path('ingresar_servicio_vinculacion', views.ingresar_servicio_vinculacion, name="ingresar_servicio_vinculacion"),
    path('edit_perro_tinder/<int:perro_id>', views.edit_perro_tinder, name='edit_perro_tinder'),
    path('tinder_perro/<int:perro_id>', views.tinder_perro, name='tinder_perro'),
    path('contestar_tinder/<int:perroLiked_id>/<int:perroLiker_id>', views.contestar_tinder, name='contestar_tinder'),
    path('perros_asociados', views.perros_asociados, name='perros_asociados_tinder'),
    path('deshabilitar_perro_tinder/<int:tinder_id>', views.deshabilitar_perro_tinder, name='deshabilitar_perro_tinder'),
]