from django.urls import path
from . import views

urlpatterns = [
    path('crear_adopcion', views.crear_adopcion, name='crear_adopcion'),
    path('adopciones', views.adopciones, name='adopciones'),
    path('contestar_adopcion/<int:usuario_id>/<int:adopcion_id>', views.contestar_adopcion, name='contestar_adopcion'),
    path('marcar_adopcion_resuelta/<int:nroAdopcion>', views.marcar_adopcion_resuelta, name='marcar_adopcion_resuelta'),
    path('campanias', views.campanias, name='campanias'),
    path('campanias/donar/<int:campania_id>', views.donar, name='donar'),
    path('crear_campania', views.crear_campania, name='crear_campania'),
    path('adopciones/<int:adopcion_id>', views.postulantes, name='postulantes'),
]
