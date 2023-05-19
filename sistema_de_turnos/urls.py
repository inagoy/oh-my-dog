from django.urls import path
from . import views

urlpatterns = [
    path('sacar_turno', views.sacar_turno, name='sacar_turno'),
    path('ver_turnos_solicitados', views.ver_turnos_solicitados,
         name='ver_turnos_solicitados')
]
