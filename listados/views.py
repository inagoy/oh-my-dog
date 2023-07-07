from django.shortcuts import render, redirect

from listados.filters import PaseadoresCuidadoresFilter
from listados.models import Trabajador
from .forms import CargarTrabajadorForm
from publicaciones.models import CampaniaDonacion
from django.contrib import messages

def paseadores_cuidadores(request):
    campanias_sin_limite = CampaniaDonacion.objects.filter(
        fecha_limite__isnull=True).order_by("id")
    campanias_con_limite = CampaniaDonacion.objects.filter(
        fecha_limite__isnull=False).order_by("-id")
    campanias_cumplen = [
        obj for obj in campanias_con_limite if obj.dias_restantes() >= 0]
    servicios = list(campanias_sin_limite) + list(campanias_cumplen)

    filtro = PaseadoresCuidadoresFilter(request.GET, queryset=Trabajador.objects.all())
    return render(request, 'listados/paseadores_cuidadores.html', {'servicios': servicios, 'filtro': filtro})


def cargar_trabajador(request):
    if request.method == "GET":
        form = CargarTrabajadorForm()
    else:
        form = CargarTrabajadorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "La carga del paseador o cuidador fue exitosa")
            return redirect('index')
    return render(request, 'listados/cargar_trabajador.html',{'form': form})