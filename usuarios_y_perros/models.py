

import os
from decimal import Decimal

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date, datetime
from django.dispatch import receiver

from django.forms import ValidationError
from .managers import CustomUserManager
from django.templatetags.static import static


class Usuario(AbstractUser):
    username = None
    # lo defino como pk o dejo la automática y lo defino como unique?  dejo "email" porque así lo reconoce autom para EMAIL_FIELD
    email = models.EmailField(unique=True)
    dni = models.IntegerField()
    apellido = models.CharField(max_length=20)
    nombre = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField(
        verbose_name="Fecha de nacimiento", default=date.today)
    domicilio = models.CharField(max_length=30)
    descuento_atencion = models.DecimalField(max_digits=6, decimal_places=2, default=0.00, verbose_name="Descuento", blank=True, null=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['dni', 'apellido', 'nombre', 'fecha_nacimiento']

    objects = CustomUserManager()

    def aplicar_descuento(self, monto_donacion):
        descuento = monto_donacion * Decimal(0.2)
        if(self.descuento_atencion + descuento) >= 3000:
            self.descuento_atencion = 3000
        else:
            self.descuento_atencion += descuento

    def __str__(self):
        return self.email


def generate_unique_filename(instance, filename):
    base_filename, extension = os.path.splitext(filename)
    timestamp = datetime.now().strftime("%m%d%Y%H%M%S")
    unique_filename = f'{base_filename}_{timestamp}{extension}'
    return os.path.join('images/', unique_filename)


class Perro(models.Model):
    nombre = models.CharField(max_length=15)
    fecha_nacimiento = models.DateField(
        verbose_name="Fecha de nacimiento", default=date.today)
    color = models.CharField(max_length=20, blank=True)
    foto = models.ImageField(
        upload_to=generate_unique_filename, blank=True, null=True,)
    observaciones = models.TextField(blank=True)

    class Sexo(models.TextChoices):
        HEMBRA = "H", "Hembra"
        MACHO = "M", "Macho"

    sexo = models.CharField(  # incluir default?
        max_length=1,
        choices=Sexo.choices,
        blank=True, null=True,
    )

    fecha_ultimo_celo = models.DateField(blank=True, null=True)
    dueño = models.ForeignKey("Usuario", on_delete=models.CASCADE)
    activo = models.BooleanField(default=True)

    class Raza(models.TextChoices):
        MESTIZO = "MEST", "Mestizo"
        LABRADOR = "LABR", "Labrador"
        BULLDOG = "BULL", "Bulldog"
        BEAGLE = "BEAG", "Beagle"
        BOXER = "BOXE", "Boxer"
        GOLDEN = "GOLD", "Golden"

    raza = models.CharField(  # incluir default?
        max_length=4,
        choices=Raza.choices,
    )

    def clean(self):
        super().clean()
        self.validate_nombre()
        self.validate_fecha_nacimiento()

    def validate_nombre(self):
        if not any(char.isalpha() for char in self.nombre):
            raise ValidationError(
                "El nombre debe contener al menos una letra.")

    def validate_fecha_nacimiento(self):
        if self.fecha_nacimiento and self.fecha_nacimiento > date.today():
            raise ValidationError(
                "La fecha de nacimiento no puede estar en el futuro.")
    
    def edad_en_meses(self, fecha):
        f_nac = self.fecha_nacimiento
        dias = -1 if (fecha.day - f_nac.day) < 0 else 0
        return (fecha.year - f_nac.year) * 12 + (fecha.month - f_nac.month) + dias
    
    def edad_meses(self):
        today = date.today()
        age_months = (today.year - self.fecha_nacimiento.year) * \
            12 + (today.month - self.fecha_nacimiento.month)
        if today.day < self.fecha_nacimiento.day:
            age_months -= 1
        return age_months
    
    def sexo_opuesto(self):
        if self.sexo == self.Sexo.HEMBRA:
            return self.Sexo.MACHO
        elif self.sexo == self.Sexo.MACHO:
            return self.Sexo.HEMBRA
        else:
            return None
        
    def foto_url(self):
        if self.foto:
            return self.foto.url
        else:
            return static('perro_default.png')

    def __str__(self) -> str:
        return self.nombre
