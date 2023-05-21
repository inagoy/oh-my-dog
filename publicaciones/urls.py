from django.urls import path
from . import views

urlpatterns = [
    path('crear_adopcion', views.crear_adopcion, name='crear_adopcion'),
    path('adopciones', views.adopciones, name='adopciones'),
]
