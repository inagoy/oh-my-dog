from django.db import models
from usuarios_y_perros.models import Perro

class Tinder(models.Model):
    class Estado(models.TextChoices):
        ACTIVO = "A", "Activo"
        INACTIVO = "I", "Inactivo"

    estado_tinder = models.CharField(
        max_length=4,
        choices=Estado.choices,
        default=Estado.ACTIVO,
    )
    perro = models.OneToOneField(Perro, on_delete=models.CASCADE)
