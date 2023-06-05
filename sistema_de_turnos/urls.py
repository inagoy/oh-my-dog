from django.urls import path
from . import views

urlpatterns = [
    path('sacar_turno', views.sacar_turno, name='sacar_turno'),
    path('ver_turnos_solicitados', views.ver_turnos_solicitados,
         name='ver_turnos_solicitados'),
    path('aceptar_turno/<int:nroTurno>', views.aceptar_turno, name='aceptar_turno'),
    path('rechazar_turno/<int:nroTurno>', views.rechazar_turno, name='rechazar_turno'),
    path('ver_historia_clinica/<int:perro_id>',views.ver_historia_clinica, name='ver_historia_clinica'),
    path('ver_turnos',views.ver_turnos, name='ver_turnos'),
]
