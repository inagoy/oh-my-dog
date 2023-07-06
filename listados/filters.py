import django_filters

from listados.models import Trabajador


class PaseadoresCuidadoresFilter(django_filters.FilterSet):
    tipo = django_filters.ChoiceFilter(choices=Trabajador.Tipo.choices, empty_label='Todos')