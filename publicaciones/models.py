from datetime import date
from django.db import models
from oh_my_dog import settings
from usuarios_y_perros.models import Perro


class Publicacion(models.Model):
    descripcion = models.CharField(
        verbose_name="Descripción", max_length=255, blank=True, null=True)
    nombre = models.CharField(max_length=255, blank=True, null=True)
    fecha_nacimiento = models.DateField(
        verbose_name="Fecha de nacimiento", blank=True, null=True)
    color = models.CharField(max_length=255, blank=True, null=True)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Estado(models.TextChoices):
        ACTIVA = "A", "Activa"
        INACTIVA = "I", "Inactiva"

    estado_publicacion = models.CharField(
        max_length=4,
        choices=Estado.choices,
        default=Estado.ACTIVA,
    )

    class Raza(models.TextChoices):
        MESTIZO = "MEST", "Mestizo"
        LABRADOR = "LABR", "Labrador"
        BULLDOG = "BULL", "Bulldog"
        BEAGLE = "BEAG", "Beagle"
        BOXER = "BOXE", "Boxer"

    raza = models.CharField(  # incluir default?
        max_length=4,
        choices=Raza.choices,
        blank=True,
    )

    def edad_meses(self):
        today = date.today()
        age_months = (today.year - self.fecha_nacimiento.year) * \
            12 + (today.month - self.fecha_nacimiento.month)
        if today.day < self.fecha_nacimiento.day:
            age_months -= 1
        return age_months


class Adopcion(Publicacion):
    perro = models.ForeignKey(Perro, on_delete=models.CASCADE, null=True)


""" 
    def descripcion(self):
        return self.perro.descipcion if self.perro else self.descripcion

    def nombre(self):
        return self.perro.nombre if self.perro else self.nombre

    def fechaNac(self):
        return self.perro.fechaNac if self.perro else self.fechaNac

    def color(self):
        return self.perro.color if self.perro else self.color

    def sexo(self):
        return self.perro.sexo if self.perro else self.sexo
 """
