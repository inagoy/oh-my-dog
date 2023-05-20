from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date
from .managers import CustomUserManager

class Usuario(AbstractUser):
    username = None
    email = models.EmailField(unique=True) # lo defino como pk o dejo la automática y lo defino como unique?  dejo "email" porque así lo reconoce autom para EMAIL_FIELD
    dni = models.IntegerField()
    apellido = models.CharField(max_length=20)
    nombre = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField(verbose_name="Fecha de nacimiento", default=date.today)
    domicilio = models.CharField(max_length=30)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['dni', 'apellido', 'nombre', 'fecha_nacimiento']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Perro(models.Model):
    nombre = models.CharField(max_length=15)
    fecha_nacimiento = models.DateField(verbose_name="Fecha de nacimiento", default=date.today)
    color = models.CharField(max_length=20, blank=True)  # poner opciones?
    # foto = models.ImageField(upload_to="images")  # ver MEDIA_ROOT y MEDIA_URL en settings
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
    activo = models.BooleanField(default= True)

    class Raza(models.TextChoices):
        MESTIZO = "MEST", "Mestizo"
        LABRADOR = "LABR", "Labrador"
        BULLDOG = "BULL", "Bulldog"
        BEAGLE = "BEAG", "Beagle"
        BOXER = "BOXE", "Boxer"

    raza = models.CharField(  # incluir default?
        max_length=4,
        choices=Raza.choices,
    )

    def edad_en_meses(self, fecha):
        f_nac = self.fecha_nacimiento
        dias = -1 if (fecha.day - f_nac.day) < 0 else 0
        return (fecha.year - f_nac.year) * 12 + (fecha.month - f_nac.month) + dias

    def __str__(self) -> str:
        return self.nombre
