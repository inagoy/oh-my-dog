#funciones auxiliares

from datetime import date
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string

def es_menor_18(birth):
    now = date.today()
    return (
        now.year - birth.year < 18
        or now.year - birth.year == 18 and (
            now.month < birth.month 
            or now.month == birth.month and now.day <= birth.day
        )
    )

def generar_contraseña():
    return get_random_string(8)

def enviar_mail_bienvenida(contraseña):
    send_mail(
                    "Bienvenidx a ¡Oh my dog!",
                    "Para ingresar por primera vez al sitio, utilice la contraseña: "+ contraseña,
                    settings.EMAIL_HOST_USER,
                    ["alive.soluciones.software@gmail.com"],
                    fail_silently=False,
                )