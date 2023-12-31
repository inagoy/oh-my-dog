from datetime import date
from django.db import models
from oh_my_dog import settings
from usuarios_y_perros.models import Perro, Usuario, generate_unique_filename
from .managers import CampaniaDonacionManager
from django.templatetags.static import static

class CampaniaDonacion(models.Model):
    nombre = models.CharField(
        max_length=30, verbose_name="Nombre de la campaña", unique=True)
    descripcion = models.CharField(
        max_length=150, verbose_name="Descripcion", blank=True, null=True)
    fecha_limite = models.DateField(
        verbose_name="Fecha límite para donar", blank=True, null=True)
    monto_recaudado = models.DecimalField(max_digits=11, decimal_places=2, default=0.00,
                                          verbose_name="Monto recaudado hasta el momento", blank=True, null=True)

    objects = CampaniaDonacionManager()

    def activa(self):
        return self.fecha_limite is None or (self.fecha_limite is not None and self.fecha_limite >= date.today())

    def dias_restantes(self):
        if self.fecha_limite is not None:
            return (date(self.fecha_limite.year, self.fecha_limite.month, self.fecha_limite.day) - date.today()).days
        return 1.1

    def actualizar_monto_recaudado(self, donacion):
        self.monto_recaudado += donacion

    def __str__(self):
        return self.nombre


class Tarjeta(models.Model):
    numero = models.IntegerField(verbose_name="Número",)
    clave = models.CharField(max_length=15, verbose_name="Clave",)
    fecha_vencimiento = models.DateField(verbose_name="Fecha de vencimiento",)
    saldo = models.DecimalField(max_digits=11, decimal_places=2,)


class Donacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    campania = models.ForeignKey(CampaniaDonacion, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=11, decimal_places=2,)
    fecha = models.DateField(default=date.today, blank=True, null=True)

class Raza(models.TextChoices):
    MESTIZO = "MEST", "Mestizo"
    LABRADOR = "LABR", "Labrador"
    BULLDOG = "BULL", "Bulldog"
    BEAGLE = "BEAG", "Beagle"
    BOXER = "BOXE", "Boxer"

class Publicacion(models.Model):
    foto = models.ImageField(
        upload_to=generate_unique_filename, blank=True, null=True,)
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
    raza = models.CharField(  # incluir default?
        max_length=4,
        choices=Raza.choices,
        blank=True,
    )

    def foto_url(self):
        if self.foto:
            return self.foto.url
        else:
            return static('perro_default.png')
        
    def edad_meses(self):
        today = date.today()
        age_months = (today.year - self.fecha_nacimiento.year) * \
            12 + (today.month - self.fecha_nacimiento.month)
        if today.day < self.fecha_nacimiento.day:
            age_months -= 1
        return age_months

class PerdidoEncontrado(Publicacion):
    perro = models.ForeignKey(Perro, on_delete=models.CASCADE, null=True)
    esPerdido = models.BooleanField()
    donde = models.CharField(
        verbose_name="Dónde", max_length=255)
    cuando = models.DateField(
        verbose_name="Cuándo")
    edadAproximada = models.IntegerField(verbose_name='Edad Aproximada (en meses)',blank=True, null=True)
    caracteristica = models.CharField(
        verbose_name="Característica distintiva", max_length=255, blank=True, null=True)    

class Adopcion(Publicacion):
    perro = models.ForeignKey(Perro, on_delete=models.CASCADE, null=True)


class Postulante(models.Model):
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, blank=True, null=True)
    adopcion = models.ForeignKey(Adopcion, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=20, blank=True, null=True)


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
