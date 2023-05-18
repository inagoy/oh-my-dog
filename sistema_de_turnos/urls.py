from django.urls import path
from . import views

urlpatterns = [
    path('solicitar_turno', views.solicitar_turno, name='solicitar_turno')
]