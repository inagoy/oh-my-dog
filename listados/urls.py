from django.urls import path
from . import views

urlpatterns = [
    path('paseadores_cuidadores', views.paseadores_cuidadores, name='paseadores_cuidadores'),
]