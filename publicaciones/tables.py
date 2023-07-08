import itertools

import django_tables2 as tables
from .models import CampaniaDonacion, Donacion


class CampaniaDonacionTable(tables.Table):
    class Meta:
        model = CampaniaDonacion
        attrs = {"class": "table table-hover table-bordered", "style": "font-size: 1.1rem"}


class DonacionTable(tables.Table):
    orden = tables.Column(empty_values=(), orderable=False, verbose_name='#', exclude_from_export=True)
    nombre_usuario = tables.Column(accessor='usuario.nombre', verbose_name='Usuario nombre', )
    campania = tables.Column(verbose_name='Campaña')
    usuario = tables.Column(verbose_name='Usuario email')

    def render_orden(self):
        self.row_orden = getattr(self, 'row_orden', itertools.count(self.page.start_index()))
        return next(self.row_orden)

    class Meta:
        model = Donacion
        # fields =
        exclude = ("id",)
        sequence = ('orden', 'campania', 'usuario', 'nombre_usuario', 'monto')
        attrs = {"class": "table table-hover table-bordered", "style": "font-size: 1.1rem"}
        empty_text = "No existen donaciones"


