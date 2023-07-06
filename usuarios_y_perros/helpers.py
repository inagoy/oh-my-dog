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
    #return get_random_string(8)
    return "1234"

def enviar_mail_bienvenida(usuario, contraseña):
    send_mail(
                    "Te damos la bienvenida a ¡Oh my dog!",
                    "Cada vez que quieras acceder al sitio, utilizá tu email: "+ usuario+ 
                    ". \nPara ingresar por primera vez, utilizá la contraseña: "+ contraseña,
                    settings.EMAIL_HOST_USER,
                    ["alive.soluciones.software@gmail.com"],
                    fail_silently=False,
                )