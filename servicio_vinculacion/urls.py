from django.urls import path
from . import views

urlpatterns = [
    path('ver_mensaje_concientizacion', views.ver_mensaje_concientizacion, name="ver_mensaje_concientizacion"),
    path('ingresar_servicio_vinculacion', views.ingresar_servicio_vinculacion, name="ingresar_servicio_vinculacion")
]