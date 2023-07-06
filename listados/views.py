from django.shortcuts import render

from listados.filters import PaseadoresCuidadoresFilter
from listados.models import Trabajador
from publicaciones.models import CampaniaDonacion


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