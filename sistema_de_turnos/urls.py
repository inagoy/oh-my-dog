from django.urls import path
from . import views

urlpatterns = [
    path('sacar_turno', views.sacar_turno, name='sacar_turno')
]