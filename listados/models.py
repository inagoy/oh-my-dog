from django.db import models


class Trabajador(models.Model):
    nombre_y_apellido = models.CharField(max_length=30, unique=True)
    
    class Zona(models.TextChoices):
        SAN_MARTIN = "San Martin" , "San Martin"
        ITALIA = "Italia" , "Italia"
        BELGRANO = "Belgrano" , "Belgrano"
        PASO = "Paso" , "Paso"
        ROCHA = "Rocha" , "Rocha"

    zona = models.CharField(
        max_length=10,
        choices=Zona.choices,
    )

    class Tipo(models.TextChoices):
        PASEADOR = "P" , "Paseador"
        CUIDADOR = "C" , "Cuidador"

    tipo = models.CharField(
        max_length=1,
        choices=Tipo.choices,
    )

    habilitado = models.BooleanField(default=True)

    fecha_fin_deshabilitacion = models.DateField(
        verbose_name="Deshabilitar hasta", blank=True, null=True
    )

    REQUIRED_FIELDS = ['zona','nombre_y_apellido',"tipo","habilitado"]