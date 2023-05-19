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
