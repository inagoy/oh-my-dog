from django.urls import path
from . import views

urlpatterns = [
    path('sacar_turno', views.sacar_turno, name='sacar_turno'),
    path('ver_turnos_solicitados', views.ver_turnos_solicitados,
         name='ver_turnos_solicitados'),
    path('ver_proximos_turnos', views.ver_proximos_turnos, name='ver_proximos_turnos'),
    path('aceptar_turno/<int:nroTurno>', views.aceptar_turno, name='aceptar_turno'),
    path('rechazar_turno/<int:nroTurno>', views.rechazar_turno, name='rechazar_turno'),
    path('cancelar_turno/<int:nroTurno>', views.cancelar_turno, name='cancelar_turno'),
    path('completar_atencion/<int:nroTurno>', views.completar_atencion, name='completar_atencion'),
    path('llenar_libreta_sanitaria/<int:nroTurno>', views.llenar_libreta_sanitaria, name='llenar_libreta_sanitaria'),
    path('ver_historia_clinica/<int:perro_id>',views.ver_historia_clinica, name='ver_historia_clinica'),
    path('ver_libreta_sanitaria/<int:perro_id>',views.ver_libreta_sanitaria, name='ver_libreta_sanitaria'),
    path('ver_turnos',views.ver_turnos, name='ver_turnos'),
    path('turnos_del_dia', views.ver_turnos_del_dia, name='ver_turnos_del_dia'),
]
