from distutils.util import strtobool

import django_filters

from publicaciones.models import CampaniaDonacion, Donacion, PerdidoEncontrado


class CampaniaDonacionFilter(django_filters.FilterSet):
    class Meta:
        model = CampaniaDonacion
        fields = {"nombre": ["exact", "contains"], "monto_recaudado": ["exact"]}
        attrs = {"class": "form-control"}


class DonacionFilter(django_filters.FilterSet):
    nombre_campania = django_filters.AllValuesFilter(field_name='campania__nombre', label='Campaña')
    mail_usuario = django_filters.AllValuesFilter(field_name='usuario__email', label='Usuario email', )
    nombre_usuario = django_filters.AllValuesFilter(field_name='usuario__nombre')
    # nombre_us = django_filters.CharFilter(field_name='usuario__nombre', lookup_expr='contains', label='Usuario nombre (cont)')
    monto = django_filters.AllValuesFilter(field_name='monto', )

    class Meta:
        model = Donacion
        # fields = {"campania": ["exact"], "usuario__nombre": ["exact"], "monto": ["exact"]}
        fields = {}
        attrs = {"class": "form-control"}


BOOLEAN_CHOICES = (('false', 'Perros encontrados'), ('true', 'Perros perdidos'), ('', 'Todas las publicaciones'))


class PerdidoEncontradoFilter(django_filters.FilterSet):
    tipo = django_filters.TypedChoiceFilter(choices=BOOLEAN_CHOICES, coerce=strtobool, field_name='esPerdido', label="Tipo de publicación")
