from django.core.exceptions import ValidationError
from django.db import models, IntegrityError
from django.http import HttpResponse


class CampaniaDonacionManager(models.Manager):
    def create_campania(self, nombre, descripcion, fecha_limite,):
        try:
            campania = self.create(nombre=nombre, descripcion=descripcion, fecha_limite=fecha_limite, monto_recaudado=0.00)
        except IntegrityError:
            raise ValidationError(f'ERROR: {nombre} already exists!')
        campania.save()
        return campania
