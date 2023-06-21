import django_tables2 as tables
from .models import CampaniaDonacion, Donacion
import django_filters


class CampaniaDonacionTable(tables.Table):
    class Meta:
        model = CampaniaDonacion
        attrs = {"class": "table table-hover table-bordered", "style": "font-size: 1.1rem"}


class CampaniaDonacionFilter(django_filters.FilterSet):
    class Meta:
        model = CampaniaDonacion
        fields = {"nombre": ["exact", "contains"], "monto_recaudado": ["exact"]}
        attrs = {"class": "form-control"}


class DonacionTable(tables.Table):
    nombre_usuario = tables.Column(accessor='usuario.nombre')
    nombre_campania = tables.Column(accessor='campania.nombre')

    class Meta:
        model = Donacion
        attrs = {"class": "table table-hover table-bordered", "style": "font-size: 1.1rem"}


class DonacionFilter(django_filters.FilterSet):
    nombre_usuario = django_filters.AllValuesFilter(field_name='usuario__nombre')
    nombre_campania = django_filters.AllValuesFilter(field_name='campania__nombre')
    nombre_us = django_filters.CharFilter(field_name='usuario__nombre', lookup_expr='contains', label='Nombre del usuario (contiene)')

    class Meta:
        model = Donacion
        fields = {"campania": ["exact"], "usuario__nombre": ["exact"], "monto": ["exact"]}
        attrs = {"class": "form-control"}
