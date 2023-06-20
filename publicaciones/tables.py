import django_tables2 as tables
from .models import CampaniaDonacion
from django_filters import FilterSet


class CampaniaDonacionTable(tables.Table):
    class Meta:
        model = CampaniaDonacion
        attrs = {"class": "table table-hover table-bordered", "style": "font-size: 1.1rem"}


class CampaniaDonacionFilter(FilterSet):
    class Meta:
        model = CampaniaDonacion
        fields = {"nombre": ["exact", "contains"], "monto_recaudado": ["exact"]}
        attrs = {"class": "form-control"}
