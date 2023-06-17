import os
from django.shortcuts import render

def ver_mensaje_concientizacion(request):
    return render(request, 'servicio_vinculacion/concientizacion.html')

def ingresar_servicio_vinculacion(request):
    return render(request, 'servicio_vinculacion/vinculacion.html')