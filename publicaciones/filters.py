from distutils.util import strtobool

import django_filters

from publicaciones.models import CampaniaDonacion, Donacion, PerdidoEncontrado


class CampaniaDonacionFilter(django_filters.FilterSet):
    class Meta:
        model = CampaniaDonacion
        fields = {"nombre": ["exact", "contains"], "monto_recaudado": ["exact"]}
        attrs = {"class": "form-control"}


class DonacionFilter(django_filters.FilterSet):
    mail_usuario = django_filters.AllValuesFilter(field_name='usuario__email', label='Usuario email', )
    fecha = django_filters.DateRangeFilter(field_name='fecha')
    monto = django_filters.NumberFilter(field_name='monto', lookup_expr='gte')

    class Meta:
        model = Donacion
        # fields = {"campania": ["exact"], "usuario__nombre": ["exact"], "monto": ["exact"]}
        fields = {}
        attrs = {"class": "form-control"}


class PerdidoEncontradoFilter(django_filters.FilterSet):
    class OpcionesChoice:
        opciones = (('false', 'Perros encontrados'), ('true', 'Perros perdidos'), ('', 'Todas las publicaciones'))

    tipo = django_filters.TypedChoiceFilter(choices=OpcionesChoice.opciones, coerce=strtobool, field_name='esPerdido', label="Tipo de publicación")


