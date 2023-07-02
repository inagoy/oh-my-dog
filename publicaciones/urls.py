from django.urls import path
from . import views

urlpatterns = [
    path('crear_adopcion', views.crear_adopcion, name='crear_adopcion'),
    path('adopciones', views.adopciones, name='adopciones'),
    path('contestar_adopcion/<int:usuario_id>/<int:adopcion_id>', views.contestar_adopcion, name='contestar_adopcion'),
    path('marcar_adopcion_resuelta/<int:nroAdopcion>', views.marcar_adopcion_resuelta, name='marcar_adopcion_resuelta'),
    path('campañas', views.campanias, name='campañas'),
    path('campañas/donar/<int:campania_id>', views.donar, name='donar'),
    # path('crear_campania', views.crear_campania, name='crear_campania'),
    path('adopciones/<int:adopcion_id>', views.postulantes, name='postulantes'),
    path('agregar_campaña', views.agregar_campania, name='agregar_campaña'),
    path('campañas_tabla', views.FilteredCampaniasTabla.as_view(), name='campañas_tabla'),
    path('campañas/donaciones_tabla', views.FilteredDonacionesTabla.as_view(), name='donaciones_tabla'),
    path('perdidos_encontrados', views.perdidos_encontrados, name='perdidos_encontrados'),
    path('crear_perdido', views.crear_perdido, name='crear_perdido'),
    path('crear_encontrado', views.crear_encontrado, name='crear_encontrado'),
]
