from django.urls import path
from . import views

urlpatterns = [
    path('crear_adopcion', views.crear_adopcion, name='crear_adopcion'),
    path('adopciones', views.adopciones, name='adopciones'),
    path('contestar_adopcion/<int:usuario_id>/<int:adopcion_id>', views.contestar_adopcion, name='contestar_adopcion'),
    path('marcar_adopcion_resuelta/<int:nroAdopcion>', views.marcar_adopcion_resuelta, name='marcar_adopcion_resuelta'),
    path('campanias', views.campanias, name='campanias'),
]
