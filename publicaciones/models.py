from datetime import date
from django.db import models
from oh_my_dog import settings
from usuarios_y_perros.models import Perro
from .managers import CampaniaDonacionManager


class CampaniaDonacion(models.Model):
    nombre = models.CharField(max_length=30, verbose_name="Nombre de la campaña", unique=True)
    descripcion = models.CharField(max_length=150, verbose_name="Descripcion", blank=True, null=True)
    fecha_limite = models.DateField(verbose_name="Fecha límite para donar", blank=True, null=True)
    monto_recaudado = models.DecimalField(max_digits=11, decimal_places=2, default=0.00, verbose_name="Monto recaudado hasta el momento", blank=True, null=True)

    objects = CampaniaDonacionManager()

    def activa(self):
        return self.fecha_limite is None or (self.fecha_limite is not None and self.fecha_limite >= date.today())

    def dias_restantes(self):
        if self.fecha_limite is not None:
            return (date(self.fecha_limite.year, self.fecha_limite.month, self.fecha_limite.day) - date.today()).days
        return -1

    def actualizar_monto_recaudado(self, donacion):
        self.monto_recaudado += donacion

    def __str__(self):
        return self.nombre


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
